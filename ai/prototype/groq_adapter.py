"""One bounded Groq free-tier experiment; no provider calls or key reads on import."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from time import monotonic, perf_counter, sleep
from typing import Any, Mapping

from jsonschema import Draft202012Validator
from openai import APIError, APITimeoutError, OpenAI

from .adapters import AdapterOutcome
from .openai_responses_adapter import normalize_openai_transport

ROOT = Path(__file__).resolve().parents[2]
AUTHORIZATION = ROOT / "ai/eval/free_baseline_authorization.experimental.v0.1.json"
MODEL = "openai/gpt-oss-20b"
BASE_URL = "https://api.groq.com/openai/v1"
PROMPTS = {
    "dialogue": "dialogue_parser.groq.experimental.v0.3.txt",
    "headline": "headline_analyzer.groq.experimental.v0.2.txt",
    "npc_surface": "npc_surface_generator.groq.experimental.v0.2.txt",
}


@dataclass(frozen=True)
class GroqOutcome(AdapterOutcome):
    # Observer-only details: never interpreted as canonical state or retry advice.
    raw_transport: Any = None
    provider_error: dict | None = None


def prepare_execution(sheet: dict, case_ids: list[str]) -> GroqAdapter:
    # This boundary precedes any environment/credential access.
    if sheet.get("execution_authorized") is not True or sheet.get("authorization_status") != "AUTHORIZED":
        raise ValueError("LIVE_EXECUTION_NOT_AUTHORIZED")
    if sheet.get("free_tier_confirmed") is not True or sheet.get("budget_usd") != 0 or sheet.get("paid_fallback_allowed") is not False:
        raise ValueError("CONFIRMED_FREE_TIER_REQUIRED")
    if sheet.get("model") != MODEL or sheet.get("base_url") != BASE_URL:
        raise ValueError("MODEL_OR_ENDPOINT_OUTSIDE_BATCH")
    if not case_ids or len(case_ids) != len(set(case_ids)) or set(case_ids) != set(sheet["case_ids"]):
        raise ValueError("CASE_SELECTION_OUTSIDE_AUTHORISED_BATCH")
    if not (type(sheet.get("max_generation_requests")) is int and 1 <= sheet["max_generation_requests"] <= 10
            and type(sheet.get("max_completion_tokens_per_request")) is int
            and 1 <= sheet["max_completion_tokens_per_request"] <= 2048):
        raise ValueError("LIMITS_OUTSIDE_PROPOSED_BATCH")
    if (ROOT / sheet["output_path"]).exists():
        raise ValueError("BATCH_OUTPUT_ALREADY_EXISTS")
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY_NOT_CONFIGURED")
    client = OpenAI(api_key=key, base_url=BASE_URL, max_retries=0, timeout=45)
    return GroqAdapter(client, max_calls=sheet["max_generation_requests"],
                       max_tokens=sheet["max_completion_tokens_per_request"],
                       interval=sheet["minimum_request_interval_seconds"])


class GroqAdapter:
    adapter_identifier = "groq-chat-free-experimental"
    model_identifier = MODEL
    prompt_version = "component-specific.groq.experimental.v0.2"
    schema_version = "groq-transport.experimental.v0.2"

    def __init__(self, client: Any, *, max_calls: int = 10, max_tokens: int = 2048,
                 interval: float = 30):
        self.client, self.max_calls, self.max_tokens, self.interval = client, max_calls, max_tokens, interval
        self.calls = 0
        self._last_request: float | None = None

    def invoke(self, component: str, model_input: Mapping[str, Any]) -> AdapterOutcome:
        if self.calls >= self.max_calls:
            return AdapterOutcome.system_failure("BATCH_CALL_LIMIT")
        prompt = (ROOT / "ai/prompts" / PROMPTS[component]).read_text(encoding="utf-8")
        metadata = {"model_identifier": MODEL, "prompt_version": prompt.splitlines()[0].split(": ", 1)[1],
                    "schema_version": None if component == "npc_surface" else self.schema_version}
        parameters = {
            "model": MODEL,
            "messages": [{"role": "system", "content": prompt},
                         {"role": "user", "content": json.dumps(model_input, ensure_ascii=False, sort_keys=True)}],
            "max_completion_tokens": self.max_tokens,
            "reasoning_effort": "low",
            "temperature": 0,
        }
        schema = None
        if component != "npc_surface":
            schema = json.loads((ROOT / f"ai/schemas/groq_{component}_transport.experimental.v0.2.schema.json").read_text(encoding="utf-8"))
            parameters["response_format"] = {"type": "json_schema", "json_schema": {
                "name": f"btl_{component}", "strict": True, "schema": schema,
            }}
        if self._last_request is not None:
            sleep(max(0, self.interval - (monotonic() - self._last_request)))
        self._last_request = monotonic()
        self.calls += 1
        started = perf_counter()
        try:
            response = self.client.chat.completions.create(**parameters)
        except APITimeoutError:
            return AdapterOutcome.system_failure("TIMEOUT", model_call_latency_ms=(perf_counter() - started) * 1000, **metadata)
        except APIError as error:
            # Keep bounded diagnostic fields, not full exceptions/headers/requests.
            # The JSONL recorder redacts secret strings from these fields too.
            status = getattr(error, "status_code", None)
            reason = f"HTTP_{status}" if status else "API_ERROR"
            body = getattr(error, "body", None)
            detail = body.get("error", body) if isinstance(body, dict) else {}
            diagnostic = {key: value[:512] for key in ("type", "code", "param", "message")
                          if isinstance(detail, dict) and isinstance(value := detail.get(key), str)}
            return GroqOutcome(system_failure_reason=reason, provider_error=diagnostic,
                               model_call_latency_ms=(perf_counter() - started) * 1000, **metadata)
        metadata["model_call_latency_ms"] = (perf_counter() - started) * 1000
        metadata["model_identifier"] = response.model
        if response.usage is not None:
            metadata.update(input_tokens=response.usage.prompt_tokens, output_tokens=response.usage.completion_tokens)
        # Cost is conditional on the confirmed Free tier, never inferred from usage absence.
        metadata["estimated_cost"] = 0.0
        if not response.choices:
            return AdapterOutcome.system_failure("MISSING_OUTPUT", **metadata)
        choice = response.choices[0]
        raw = choice.message.content
        if choice.finish_reason != "stop" or not isinstance(raw, str) or not raw.strip():
            return AdapterOutcome(output=raw, system_failure_reason="INCOMPLETE_OR_MISSING_OUTPUT", **metadata)
        if getattr(choice.message, "refusal", None):
            return AdapterOutcome.system_failure("REFUSAL", **metadata)
        if schema is None:
            return AdapterOutcome.success(raw, **metadata)
        try:
            transport = json.loads(raw)
        except json.JSONDecodeError:
            return AdapterOutcome(output=raw, system_failure_reason="MALFORMED_JSON", **metadata)
        if not Draft202012Validator(schema).is_valid(transport):
            return GroqOutcome(output=transport, raw_transport=transport,
                               system_failure_reason="TRANSPORT_SCHEMA_FAILURE", **metadata)
        inner = transport["result"] if component == "headline" else transport
        # Wire uniqueness is a compatibility hypothesis, not a relaxed local gate.
        local_schema = json.loads((ROOT / f"ai/schemas/openai_{component}_transport.experimental.v0.1.schema.json").read_text(encoding="utf-8"))
        if not Draft202012Validator(local_schema).is_valid(inner):
            return GroqOutcome(output=inner, raw_transport=transport,
                               system_failure_reason="TRANSPORT_SCHEMA_FAILURE", **metadata)
        return GroqOutcome(output=normalize_openai_transport(component, inner), raw_transport=transport, **metadata)
