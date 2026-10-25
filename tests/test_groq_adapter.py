import json
from types import SimpleNamespace
from unittest.mock import Mock

import httpx2
from openai import APITimeoutError, BadRequestError
import pytest

from ai.prototype import groq_adapter
from ai.prototype.baseline import load_json, MANIFEST, SUPPORT, run_case
from ai.prototype.groq_adapter import AUTHORIZATION, GroqAdapter, prepare_execution


def response(content, *, finish="stop"):
    return SimpleNamespace(model="openai/gpt-oss-20b", usage=SimpleNamespace(prompt_tokens=30, completion_tokens=20),
        choices=[SimpleNamespace(finish_reason=finish, message=SimpleNamespace(content=content, refusal=None))])


@pytest.mark.parametrize("component,wire,expected", [
    ("dialogue", {"status": "RESOLVED", "reason": None, "act": "REQUEST", "target_id": "REVEAL_PAYMENT_PAYER",
                  "value_id": None, "polarity": None, "tactics": [], "evidence_ref_ids": []}, "REQUEST"),
    ("headline", {"result": {"status": "RESOLVED", "reason": None, "claims": []}}, []),
    ("npc_surface", "Company A paid me.", "Company A paid me."),
])
def test_groq_request_and_normalisation_reuse_existing_contract(component, wire, expected):
    client = Mock()
    client.chat.completions.create.return_value = response(wire if isinstance(wire, str) else json.dumps(wire))
    adapter = GroqAdapter(client, interval=0)
    result = adapter.invoke(component, {"player_text": "fixture"})
    assert result.system_failure_reason is None
    assert result.input_tokens == 30 and result.output_tokens == 20
    request = client.chat.completions.create.call_args.kwargs
    assert request["max_completion_tokens"] == 2048
    assert request["reasoning_effort"] == "low"
    if component == "npc_surface":
        assert result.output == expected and "response_format" not in request
    else:
        assert request["response_format"]["json_schema"]["strict"] is True
        assert "reason" not in result.output
        assert result.output["act" if component == "dialogue" else "claims"] == expected
        assert result.raw_transport == wire


def test_zero_claim_null_is_rejected_without_fabricating_empty_claim_set():
    client = Mock()
    client.chat.completions.create.return_value = response(json.dumps(
        {"result": {"status": "RESOLVED", "reason": None, "claims": None}}))
    outcome = GroqAdapter(client, interval=0).invoke("headline", {})
    assert outcome.system_failure_reason == "TRANSPORT_SCHEMA_FAILURE"
    assert outcome.raw_transport["result"]["claims"] is None


def test_groq_wire_compatibility_keeps_local_duplicate_gate():
    client = Mock()
    wire = {"status": "RESOLVED", "reason": None, "act": "REQUEST", "target_id": "REVEAL_PAYMENT_PAYER",
            "value_id": None, "polarity": None, "tactics": ["THREAT", "THREAT"], "evidence_ref_ids": []}
    client.chat.completions.create.return_value = response(json.dumps(wire))
    outcome = GroqAdapter(client, interval=0).invoke("dialogue", {})
    assert outcome.system_failure_reason == "TRANSPORT_SCHEMA_FAILURE"
    sent = client.chat.completions.create.call_args.kwargs["response_format"]["json_schema"]["schema"]
    assert "uniqueItems" not in sent["properties"]["tactics"]


def test_http400_records_useful_diagnostic_without_headers_or_secret(tmp_path):
    client = Mock()
    client.chat.completions.create.side_effect = BadRequestError("bad schema", response=httpx2.Response(
        400, request=httpx2.Request("POST", "https://api.groq.com")), body={"error": {
            "code": "invalid_request_error", "param": "response_format",
            "message": "Unsupported schema keyword uniqueItems sk-fake_secret_for_recording_123456",
            "headers": {"authorization": "DO_NOT_KEEP"}, "failed_generation": "DO_NOT_KEEP"}})
    manifest = load_json(MANIFEST)
    case = next(c for c in manifest["cases"] if c["case_id"] == "dialogue-d18-valid")
    path = tmp_path / "diagnostic.jsonl"
    result = run_case(manifest, case, load_json(SUPPORT), run_id="mock-error", path=path,
                      adapter=GroqAdapter(client, interval=0))
    text = path.read_text(encoding="utf-8")
    assert "Unsupported schema keyword uniqueItems" in text
    assert "sk-fake" not in text and "DO_NOT_KEEP" not in text
    assert result["final_runtime_result"] == "AI_SYSTEM_FAILURE"


def test_groq_timeout_consumes_one_request_and_has_no_hidden_retry():
    client = Mock()
    client.chat.completions.create.side_effect = APITimeoutError(request=httpx2.Request("POST", "https://api.groq.com"))
    adapter = GroqAdapter(client, interval=0, max_calls=1)
    assert adapter.invoke("headline", {}).system_failure_reason == "TIMEOUT"
    assert adapter.invoke("headline", {}).system_failure_reason == "BATCH_CALL_LIMIT"
    assert client.chat.completions.create.call_count == 1


def test_malformed_candidate_retained_for_review_without_becoming_valid_output():
    client = Mock()
    client.chat.completions.create.return_value = response("{broken")
    result = GroqAdapter(client, interval=0).invoke("headline", {})
    assert result.system_failure_reason == "MALFORMED_JSON"
    assert result.output == "{broken" and result.output_tokens == 20


def test_closed_batch_stops_before_credentials_or_client(monkeypatch):
    environment = Mock()
    environment.get.side_effect = AssertionError("credential access before authorization")
    monkeypatch.setattr(groq_adapter, "os", SimpleNamespace(environ=environment))
    constructor = Mock(side_effect=AssertionError("client created before authorization"))
    monkeypatch.setattr(groq_adapter, "OpenAI", constructor)
    sheet = load_json(AUTHORIZATION)
    sheet.update(execution_authorized=False, authorization_status="PROPOSED_NOT_AUTHORIZED", free_tier_confirmed=False)
    with pytest.raises(ValueError, match="LIVE_EXECUTION_NOT_AUTHORIZED"):
        prepare_execution(sheet, sheet["case_ids"])
    sheet.update(execution_authorized=True, authorization_status="AUTHORIZED")
    with pytest.raises(ValueError, match="CONFIRMED_FREE_TIER_REQUIRED"):
        prepare_execution(sheet, sheet["case_ids"])


def test_narrow_recheck_has_its_own_limits_and_case_selection(monkeypatch, tmp_path):
    sheet = load_json(AUTHORIZATION.with_name("free_recheck_authorization.experimental.v0.2.json"))
    sheet.update(execution_authorized=True, authorization_status="AUTHORIZED", free_tier_confirmed=True)
    monkeypatch.setattr(groq_adapter, "ROOT", tmp_path)
    environment = {"GROQ_API_KEY": "mock-key-no-network"}
    monkeypatch.setattr(groq_adapter, "os", SimpleNamespace(environ=environment))
    constructor = Mock()
    monkeypatch.setattr(groq_adapter, "OpenAI", constructor)
    adapter = prepare_execution(sheet, sheet["case_ids"])
    assert adapter.max_calls == 6 and adapter.max_tokens == 2048
    assert len(sheet["case_ids"]) == 3
    with pytest.raises(ValueError, match="CASE_SELECTION_OUTSIDE_AUTHORISED_BATCH"):
        prepare_execution(sheet, sheet["case_ids"] + ["headline-t01-four-claims"])
    sheet["max_generation_requests"] = 11
    with pytest.raises(ValueError, match="LIMITS_OUTSIDE_PROPOSED_BATCH"):
        prepare_execution(sheet, sheet["case_ids"])


def test_cli_recheck_stops_before_client_while_not_approved(monkeypatch):
    from ai.prototype import baseline
    from ai.prototype.baseline import main
    auth_path = AUTHORIZATION.with_name("free_recheck_authorization.experimental.v0.2.json")
    proposed = load_json(auth_path)
    proposed.update(execution_authorized=False, authorization_status="PROPOSED_NOT_AUTHORIZED")
    monkeypatch.setattr(baseline, "load_json", lambda path: proposed if path == auth_path else load_json(path))
    constructor = Mock(side_effect=AssertionError("unapproved request"))
    monkeypatch.setattr(groq_adapter, "OpenAI", constructor)
    with pytest.raises(SystemExit) as stopped:
        main(["--adapter", "groq", "--authorization", str(auth_path)])
    assert stopped.value.code == 2
    constructor.assert_not_called()
