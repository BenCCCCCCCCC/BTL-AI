from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from ai.prototype import openai_responses_adapter as adapter_module
from ai.prototype.openai_responses_adapter import (
    OpenAIResponsesAdapter,
    normalize_openai_transport,
)
from ai.prototype.runner import BaselineRunner
from ai.prototype.validation import RuntimeCatalogue


class FakeResponses:
    def __init__(self, response=None, error: Exception | None = None) -> None:
        self.response = response
        self.error = error
        self.calls: list[dict] = []

    def create(self, **parameters):
        self.calls.append(parameters)
        if self.error is not None:
            raise self.error
        return self.response


class FakeClient:
    def __init__(self, response=None, error: Exception | None = None) -> None:
        self.responses = FakeResponses(response, error)


def _response(
    output_text: str | None,
    *,
    status: str = "completed",
    model: str = "gpt-5.6-terra",
    input_tokens: int | None = None,
    output_tokens: int | None = None,
    output=(),
):
    usage = None
    if input_tokens is not None or output_tokens is not None:
        usage = SimpleNamespace(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )
    return SimpleNamespace(
        status=status,
        model=model,
        output_text=output_text,
        output=output,
        usage=usage,
    )


def _adapter(response=None, error: Exception | None = None):
    client = FakeClient(response, error)
    return OpenAIResponsesAdapter(client), client


def _dialogue_transport() -> dict:
    return {
        "status": "RESOLVED",
        "reason": None,
        "act": "REQUEST",
        "target_id": "REVEAL_PAYMENT_PAYER",
        "value_id": None,
        "polarity": None,
        "tactics": ["INDIRECT_PROBE", "ACCUSATION", "THREAT"],
        "evidence_ref_ids": ["PHOTO_01"],
    }


def _headline_transport(claims) -> dict:
    return {"status": "RESOLVED", "reason": None, "claims": claims}


def test_dialogue_structured_output_success_and_direct_request_configuration() -> None:
    adapter, client = _adapter(_response(json.dumps(_dialogue_transport())))

    outcome = adapter.invoke("dialogue", {"player_text": "fixture"})

    assert outcome.system_failure_reason is None
    assert outcome.output == {
        "status": "RESOLVED",
        "act": "REQUEST",
        "target_id": "REVEAL_PAYMENT_PAYER",
        "tactics": ["INDIRECT_PROBE", "ACCUSATION", "THREAT"],
        "evidence_ref_ids": ["PHOTO_01"],
    }
    request = client.responses.calls[0]
    assert request["model"] == "gpt-5.6-terra"
    assert request["reasoning"] == {"effort": "low"}
    assert request["store"] is False
    assert request["max_output_tokens"] == 1024
    assert request["text"]["format"]["type"] == "json_schema"
    assert request["text"]["format"]["strict"] is True
    for forbidden in (
        "tools",
        "tool_choice",
        "parallel_tool_calls",
        "web_search",
        "file_search",
    ):
        assert forbidden not in request


def test_openai_adapter_is_compatible_with_existing_runner_and_measurement(
    dialogue_catalogue: RuntimeCatalogue,
) -> None:
    adapter, _ = _adapter(
        _response(
            json.dumps(_dialogue_transport()),
            input_tokens=100,
            output_tokens=20,
        )
    )
    runner = BaselineRunner(
        adapter,
        manifest_version="0.1.1",
        contract_version="0.1.1",
    )

    result = runner.run_dialogue(
        run_id="OPENAI-FAKE",
        case_id="dialogue-d18-valid",
        model_input={"player_text": "fixture"},
        catalogue=dialogue_catalogue,
        expected_safety_disposition="ACCEPT",
    )

    assert result.validated_output is not None
    assert result.final_runtime_result == "PASS"
    assert result.measurement.adapter_identifier == "openai-responses"
    assert result.measurement.model_identifier == "gpt-5.6-terra"
    assert result.measurement.prompt_version == "dialogue-parser.experimental.v0.1"
    assert result.measurement.schema_version == (
        "openai-dialogue-transport.experimental.v0.1"
    )
    assert result.measurement.input_tokens == 100
    assert result.measurement.output_tokens == 20


def test_headline_structured_output_success() -> None:
    claims = [
        {
            "target_id": "FIRE_FIRST",
            "value_id": "SECURITY_FORCES",
            "polarity": "AFFIRM",
            "commitment_mode": "ASSERTED",
            "source_ref_id": None,
        }
    ]
    adapter, _ = _adapter(_response(json.dumps(_headline_transport(claims))))

    outcome = adapter.invoke("headline", {"headline_text": "fixture"})

    assert outcome.system_failure_reason is None
    assert outcome.output == {
        "status": "RESOLVED",
        "claims": [
            {
                "target_id": "FIRE_FIRST",
                "value_id": "SECURITY_FORCES",
                "polarity": "AFFIRM",
                "commitment_mode": "ASSERTED",
            }
        ],
    }


def test_valid_zero_claims_survive_transport_normalization() -> None:
    adapter, _ = _adapter(_response(json.dumps(_headline_transport([]))))

    outcome = adapter.invoke("headline", {"headline_text": "A city waits."})

    assert outcome.system_failure_reason is None
    assert outcome.output == {"status": "RESOLVED", "claims": []}
    assert "claims" in outcome.output


def test_null_claim_set_is_absent_and_never_normalized_to_empty_claims() -> None:
    transport = _headline_transport(None)

    candidate = normalize_openai_transport("headline", transport)

    assert candidate == {"status": "RESOLVED"}
    assert "claims" not in candidate
    assert candidate != {"status": "RESOLVED", "claims": []}


def test_nullable_claim_fields_are_only_removed_mechanically() -> None:
    transport = _headline_transport(
        [
            {
                "target_id": "FIRE_FIRST",
                "value_id": None,
                "polarity": None,
                "commitment_mode": "QUESTIONED",
                "source_ref_id": None,
            }
        ]
    )

    candidate = normalize_openai_transport("headline", transport)

    assert candidate == {
        "status": "RESOLVED",
        "claims": [
            {"target_id": "FIRE_FIRST", "commitment_mode": "QUESTIONED"}
        ],
    }


def test_npc_plain_text_success() -> None:
    adapter, client = _adapter(_response("  Company A paid me.  "))

    outcome = adapter.invoke("npc_surface", {"response_mode": "ANSWER"})

    assert outcome.output == "Company A paid me."
    assert "text" not in client.responses.calls[0]


def test_refusal_maps_to_ai_system_failure_without_exposing_refusal_text() -> None:
    refusal = SimpleNamespace(type="refusal", refusal="sensitive refusal text")
    output = [SimpleNamespace(content=[refusal])]
    adapter, _ = _adapter(_response("", output=output))

    outcome = adapter.invoke("dialogue", {"player_text": "fixture"})

    assert outcome.system_failure_reason == "REFUSAL"
    assert "sensitive refusal text" not in repr(outcome)


@pytest.mark.parametrize(
    ("response", "reason"),
    (
        (_response(None), "MISSING_USABLE_OUTPUT"),
        (_response("", status="incomplete"), "INCOMPLETE_RESPONSE"),
    ),
)
def test_incomplete_or_missing_output_maps_to_ai_system_failure(
    response, reason: str
) -> None:
    adapter, _ = _adapter(response)

    outcome = adapter.invoke("headline", {"headline_text": "fixture"})

    assert outcome.system_failure_reason == reason


@pytest.mark.parametrize(
    ("error", "reason"),
    (
        (TimeoutError("do not log this"), "TIMEOUT"),
        (RuntimeError("provider details must not leak"), "PROVIDER_API_ERROR"),
    ),
)
def test_timeout_and_api_exception_map_without_exception_text(
    error: Exception, reason: str
) -> None:
    adapter, _ = _adapter(error=error)

    outcome = adapter.invoke("dialogue", {"player_text": "fixture"})

    assert outcome.system_failure_reason == reason
    assert str(error) not in repr(outcome)


def test_malformed_structured_output_maps_to_ai_system_failure() -> None:
    adapter, _ = _adapter(_response("not-json"))

    outcome = adapter.invoke("dialogue", {"player_text": "fixture"})

    assert outcome.system_failure_reason == "STRUCTURED_OUTPUT_PARSE_FAILURE"


def test_transport_schema_failure_maps_to_ai_system_failure() -> None:
    transport = _dialogue_transport()
    del transport["act"]
    adapter, _ = _adapter(_response(json.dumps(transport)))

    outcome = adapter.invoke("dialogue", {"player_text": "fixture"})

    assert outcome.system_failure_reason == "TRANSPORT_SCHEMA_VALIDATION_FAILURE"


def test_usage_model_metadata_latency_and_estimated_cost_are_captured() -> None:
    adapter, _ = _adapter(
        _response(
            json.dumps(_dialogue_transport()),
            input_tokens=125,
            output_tokens=25,
        )
    )

    outcome = adapter.invoke("dialogue", {"player_text": "fixture"})

    assert outcome.model_identifier == "gpt-5.6-terra"
    assert outcome.input_tokens == 125
    assert outcome.output_tokens == 25
    assert outcome.model_call_latency_ms is not None
    assert outcome.estimated_cost == pytest.approx(0.00055)
    assert outcome.prompt_version == "dialogue-parser.experimental.v0.1"
    assert outcome.schema_version == "openai-dialogue-transport.experimental.v0.1"


def test_environment_factory_disables_sdk_retries_without_making_a_request(
    monkeypatch,
) -> None:
    captured: dict = {}

    class ClientWithoutRequests:
        def __init__(self, **kwargs) -> None:
            captured.update(kwargs)

    monkeypatch.setenv("OPENAI_API_KEY", "test-key-parts-never-logged")
    monkeypatch.setattr(adapter_module, "OpenAI", ClientWithoutRequests)

    adapter = OpenAIResponsesAdapter.from_environment()

    assert adapter.model_identifier == "gpt-5.6-terra"
    assert adapter.reasoning_effort == "low"
    assert "api_key" in captured
    assert captured["admin_api_key"] == ""
    assert captured["organization"] == ""
    assert captured["project"] == ""
    assert captured["webhook_secret"] == ""
    assert captured["base_url"] == "https://api.openai.com/v1"
    assert captured["max_retries"] == 0
    assert captured["timeout"] == 30.0
