"""Experimental direct OpenAI Responses adapter for the Batch 2B.0 preflight.

The adapter produces non-authoritative candidates only. Dialogue and Headline
transport objects are mechanically normalised before the existing Frozen
candidate validators see them. No model call occurs unless ``invoke`` is
explicitly called by a runner.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import os
from functools import lru_cache
from pathlib import Path
from time import perf_counter
from typing import Any, Callable, Mapping

from jsonschema import Draft202012Validator
from openai import APIError, APITimeoutError, OpenAI

from .adapters import AdapterOutcome


ROOT = Path(__file__).resolve().parents[2]
AUTHORIZATION_SHEET_PATH = (
    ROOT / "ai" / "eval" / "paid_smoke_authorization.experimental.v0.1.json"
)


@dataclass(frozen=True)
class _ComponentConfig:
    prompt_path: Path
    prompt_version: str
    schema_path: Path | None
    schema_version: str | None
    max_output_tokens: int


@dataclass(frozen=True)
class _PreparedRequest:
    component: str
    config: _ComponentConfig
    generation_parameters: Mapping[str, Any]


@dataclass(frozen=True)
class PaidSmokeExecutionDecision:
    """Result of the mandatory pre-run paid-smoke authorization boundary."""

    adapter: PaidSmokeGuardedAdapter | None = field(default=None, repr=False)
    failure_reason: str | None = None

    @property
    def authorized(self) -> bool:
        return self.adapter is not None and self.failure_reason is None


def _read_field(value: Any, field_name: str, default: Any = None) -> Any:
    if isinstance(value, Mapping):
        return value.get(field_name, default)
    return getattr(value, field_name, default)


@lru_cache(maxsize=1)
def load_authorization_sheet() -> dict[str, Any]:
    return json.loads(AUTHORIZATION_SHEET_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=3)
def _component_config(component: str) -> _ComponentConfig:
    sheet = load_authorization_sheet()
    prompt = sheet["prompts"][component]
    schema = sheet["transport_schemas"].get(component)
    case = next(item for item in sheet["cases"] if item["component"] == component)
    return _ComponentConfig(
        prompt_path=ROOT / prompt["path"],
        prompt_version=prompt["version"],
        schema_path=None if schema is None else ROOT / schema["path"],
        schema_version=None if schema is None else schema["version"],
        max_output_tokens=case[
            "max_output_tokens_per_model_generation_attempt"
        ],
    )


@lru_cache(maxsize=2)
def _transport_schema(path: Path) -> dict[str, Any]:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def normalize_openai_transport(
    component: str, transport_output: Mapping[str, Any]
) -> dict[str, Any]:
    """Mechanically map provider wire nulls to optional Frozen field absence."""

    if component == "dialogue":
        return {
            field_name: value
            for field_name, value in transport_output.items()
            if value is not None
        }

    if component == "headline":
        candidate: dict[str, Any] = {"status": transport_output["status"]}
        if transport_output["reason"] is not None:
            candidate["reason"] = transport_output["reason"]
        claims = transport_output["claims"]
        if claims is not None:
            candidate["claims"] = [
                {
                    field_name: value
                    for field_name, value in claim.items()
                    if value is not None
                }
                for claim in claims
            ]
        return candidate

    raise ValueError(f"unsupported structured component: {component}")


class OpenAIResponsesAdapter:
    """Small Responses API adapter compatible with ``ModelAdapter``."""

    adapter_identifier = "openai-responses"
    prompt_version = "component-specific.experimental.v0.1"
    schema_version = "provider-transport.experimental.v0.1"

    def __init__(
        self,
        client: Any,
        *,
        model_identifier: str = "gpt-5.6-terra",
        reasoning_effort: str = "low",
        request_timeout_seconds: float = 30.0,
        input_price_usd_per_1m: float = 2.0,
        output_price_usd_per_1m: float = 12.0,
    ) -> None:
        self._client = client
        self.model_identifier = model_identifier
        self.reasoning_effort = reasoning_effort
        self.request_timeout_seconds = request_timeout_seconds
        self.input_price_usd_per_1m = input_price_usd_per_1m
        self.output_price_usd_per_1m = output_price_usd_per_1m

    @classmethod
    def _from_environment_after_authorization(cls) -> OpenAIResponsesAdapter:
        """Construct a provider client only after the paid-smoke boundary passes."""

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("API_CREDENTIALS_NOT_CONFIGURED")
        sheet = load_authorization_sheet()
        client = OpenAI(
            api_key=api_key,
            admin_api_key="",
            organization="",
            project="",
            webhook_secret="",
            base_url=sheet["base_url"],
            max_retries=sheet["sdk_internal_retries"],
            timeout=sheet["request_timeout_seconds"],
        )
        client.admin_api_key = None
        client.organization = None
        client.project = None
        client.webhook_secret = None
        return cls(
            client,
            model_identifier=sheet["model"],
            reasoning_effort=sheet["reasoning_effort"],
            request_timeout_seconds=sheet["request_timeout_seconds"],
            input_price_usd_per_1m=sheet["pricing_snapshot_usd_per_1m_tokens"][
                "input"
            ],
            output_price_usd_per_1m=sheet["pricing_snapshot_usd_per_1m_tokens"][
                "output"
            ],
        )

    def invoke(
        self, component: str, model_input: Mapping[str, Any]
    ) -> AdapterOutcome:
        if component not in {"dialogue", "headline", "npc_surface"}:
            return AdapterOutcome.system_failure("UNSUPPORTED_COMPONENT")

        prepared = self._prepare_request(component, model_input)
        return self._invoke_prepared(prepared)

    def _prepare_request(
        self, component: str, model_input: Mapping[str, Any]
    ) -> _PreparedRequest:
        config = _component_config(component)
        return _PreparedRequest(
            component=component,
            config=config,
            generation_parameters=self._request_parameters(
                component, model_input, config
            ),
        )

    def _invoke_prepared(self, prepared: _PreparedRequest) -> AdapterOutcome:
        component = prepared.component
        config = prepared.config
        started = perf_counter()
        try:
            response = self._client.responses.create(
                **prepared.generation_parameters
            )
        except (APITimeoutError, TimeoutError):
            return self._failure("TIMEOUT", config, started)
        except APIError:
            return self._failure("PROVIDER_API_ERROR", config, started)
        except Exception:
            return self._failure("PROVIDER_API_ERROR", config, started)

        latency_ms = (perf_counter() - started) * 1000
        metadata = self._response_metadata(response, config, latency_ms)
        if _has_refusal(response):
            return AdapterOutcome.system_failure("REFUSAL", **metadata)
        if _read_field(response, "status") != "completed":
            return AdapterOutcome.system_failure("INCOMPLETE_RESPONSE", **metadata)

        output_text = _read_field(response, "output_text")
        if not isinstance(output_text, str) or not output_text.strip():
            return AdapterOutcome.system_failure("MISSING_USABLE_OUTPUT", **metadata)

        if component == "npc_surface":
            return AdapterOutcome.success(output_text.strip(), **metadata)

        try:
            transport_output = json.loads(output_text)
        except (json.JSONDecodeError, TypeError):
            return AdapterOutcome.system_failure(
                "STRUCTURED_OUTPUT_PARSE_FAILURE", **metadata
            )

        if not isinstance(transport_output, Mapping):
            return AdapterOutcome.system_failure(
                "STRUCTURED_OUTPUT_PARSE_FAILURE", **metadata
            )
        assert config.schema_path is not None
        schema_errors = tuple(
            Draft202012Validator(_transport_schema(config.schema_path)).iter_errors(
                transport_output
            )
        )
        if schema_errors:
            return AdapterOutcome.system_failure(
                "TRANSPORT_SCHEMA_VALIDATION_FAILURE", **metadata
            )

        candidate = normalize_openai_transport(component, transport_output)
        return AdapterOutcome.success(candidate, **metadata)

    def _request_parameters(
        self,
        component: str,
        model_input: Mapping[str, Any],
        config: _ComponentConfig,
    ) -> dict[str, Any]:
        parameters: dict[str, Any] = {
            "model": self.model_identifier,
            "reasoning": {"effort": self.reasoning_effort},
            "instructions": config.prompt_path.read_text(encoding="utf-8"),
            "input": json.dumps(model_input, ensure_ascii=False, sort_keys=True),
            "max_output_tokens": config.max_output_tokens,
            "store": False,
            "timeout": self.request_timeout_seconds,
        }
        if config.schema_path is not None:
            parameters["text"] = {
                "format": {
                    "type": "json_schema",
                    "name": config.schema_path.stem.replace(".", "_").replace("-", "_"),
                    "strict": True,
                    "schema": _transport_schema(config.schema_path),
                }
            }
        return parameters

    def _failure(
        self, reason: str, config: _ComponentConfig, started: float
    ) -> AdapterOutcome:
        return AdapterOutcome.system_failure(
            reason,
            prompt_version=config.prompt_version,
            schema_version=config.schema_version,
            model_call_latency_ms=(perf_counter() - started) * 1000,
        )

    def _response_metadata(
        self, response: Any, config: _ComponentConfig, latency_ms: float
    ) -> dict[str, Any]:
        usage = _read_field(response, "usage")
        input_tokens = _read_field(usage, "input_tokens")
        output_tokens = _read_field(usage, "output_tokens")
        estimated_cost = None
        if isinstance(input_tokens, int) and isinstance(output_tokens, int):
            estimated_cost = (
                input_tokens * self.input_price_usd_per_1m
                + output_tokens * self.output_price_usd_per_1m
            ) / 1_000_000
        return {
            "model_identifier": _read_field(
                response, "model", self.model_identifier
            ),
            "prompt_version": config.prompt_version,
            "schema_version": config.schema_version,
            "input_tokens": input_tokens if isinstance(input_tokens, int) else None,
            "output_tokens": output_tokens if isinstance(output_tokens, int) else None,
            "model_call_latency_ms": latency_ms,
            "estimated_cost": estimated_cost,
        }


_INPUT_TOKEN_COUNT_PARAMETER_NAMES = frozenset(
    {
        "conversation",
        "input",
        "instructions",
        "model",
        "parallel_tool_calls",
        "previous_response_id",
        "reasoning",
        "text",
        "tool_choice",
        "tools",
        "truncation",
    }
)


class PaidSmokeGuardedAdapter:
    """OpenAI paid-smoke adapter with per-request and aggregate call guards."""

    adapter_identifier = "openai-responses-paid-smoke-guarded"

    def __init__(
        self,
        adapter: OpenAIResponsesAdapter,
        authorization_sheet: Mapping[str, Any],
    ) -> None:
        self._adapter = adapter
        self._authorization_sheet = dict(authorization_sheet)
        self.model_identifier = adapter.model_identifier
        self.prompt_version = adapter.prompt_version
        self.schema_version = adapter.schema_version
        self.input_token_count_requests = 0
        self.model_generation_calls = 0

    def invoke(
        self, component: str, model_input: Mapping[str, Any]
    ) -> AdapterOutcome:
        if not _paid_smoke_is_authorized(self._authorization_sheet):
            return AdapterOutcome.system_failure("PAID_SMOKE_NOT_AUTHORIZED")

        if self.model_generation_calls >= self._authorization_sheet[
            "max_model_generation_calls"
        ]:
            return AdapterOutcome.system_failure(
                "MODEL_GENERATION_CALL_LIMIT_EXCEEDED"
            )

        if self.input_token_count_requests >= self._authorization_sheet[
            "max_pre_send_input_token_count_requests"
        ]:
            return AdapterOutcome.system_failure(
                "INPUT_TOKEN_COUNT_REQUEST_LIMIT_EXCEEDED"
            )

        if component not in {"dialogue", "headline", "npc_surface"}:
            return AdapterOutcome.system_failure("UNSUPPORTED_COMPONENT")

        prepared = self._adapter._prepare_request(component, model_input)
        count_parameters = {
            name: value
            for name, value in prepared.generation_parameters.items()
            if name in _INPUT_TOKEN_COUNT_PARAMETER_NAMES
        }
        self.input_token_count_requests += 1
        try:
            count_response = self._adapter._client.responses.input_tokens.count(
                **count_parameters
            )
        except Exception:
            return self._guard_failure("INPUT_TOKEN_COUNT_FAILED", prepared)

        input_tokens = _read_field(count_response, "input_tokens")
        if type(input_tokens) is not int or input_tokens < 0:
            return self._guard_failure("INPUT_TOKEN_COUNT_FAILED", prepared)

        if input_tokens > self._authorization_sheet[
            "input_token_ceiling_per_model_generation_call"
        ]:
            return self._guard_failure(
                "EXPECTED_INPUT_TOKENS_EXCEED_8192", prepared
            )

        self.model_generation_calls += 1
        return self._adapter._invoke_prepared(prepared)

    @staticmethod
    def _guard_failure(
        reason: str, prepared: _PreparedRequest
    ) -> AdapterOutcome:
        return AdapterOutcome.system_failure(
            reason,
            prompt_version=prepared.config.prompt_version,
            schema_version=prepared.config.schema_version,
        )


def prepare_paid_smoke_execution(
    adapter_factory: Callable[[], OpenAIResponsesAdapter],
    authorization_sheet: Mapping[str, Any] | None = None,
) -> PaidSmokeExecutionDecision:
    """Authorize before constructing an adapter or entering BaselineRunner."""

    sheet = (
        load_authorization_sheet()
        if authorization_sheet is None
        else dict(authorization_sheet)
    )
    if not _paid_smoke_is_authorized(sheet):
        return PaidSmokeExecutionDecision(
            failure_reason="PAID_SMOKE_NOT_AUTHORIZED"
        )
    return PaidSmokeExecutionDecision(
        adapter=PaidSmokeGuardedAdapter(adapter_factory(), sheet)
    )


def prepare_paid_smoke_execution_from_environment() -> PaidSmokeExecutionDecision:
    """Future real-call boundary; current closed sheet stops before key access."""

    return prepare_paid_smoke_execution(
        OpenAIResponsesAdapter._from_environment_after_authorization,
    )


def _paid_smoke_is_authorized(sheet: Mapping[str, Any]) -> bool:
    governance = sheet.get("governance", {})
    return (
        sheet.get("execution_authorized") is True
        and sheet.get("authorization_status")
        == governance.get("recognised_execution_authorization_status")
        == "AUTHORIZED_FOR_PAID_SMOKE"
    )


def _has_refusal(response: Any) -> bool:
    for output_item in _read_field(response, "output", ()) or ():
        for content_item in _read_field(output_item, "content", ()) or ():
            if _read_field(content_item, "type") == "refusal":
                return True
    return False
