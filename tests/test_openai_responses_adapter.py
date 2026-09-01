from __future__ import annotations

from copy import deepcopy
import json
from types import SimpleNamespace

import pytest

from ai.prototype import openai_responses_adapter as adapter_module
from ai.prototype.openai_responses_adapter import (
    OpenAIResponsesAdapter,
    PaidSmokeGuardedAdapter,
    load_authorization_sheet,
    normalize_openai_transport,
    prepare_paid_smoke_execution,
    prepare_paid_smoke_execution_from_environment,
)
from ai.prototype.runner import BaselineRunner
from ai.prototype.validation import RuntimeCatalogue


class FakeInputTokens:
    def __init__(
        self,
        owner: FakeResponses,
        response=None,
        error: Exception | None = None,
    ) -> None:
        self.owner = owner
        self.response = (
            SimpleNamespace(input_tokens=8192) if response is None else response
        )
        self.error = error
        self.calls: list[dict] = []

    def count(self, **parameters):
        self.owner.call_order.append("input_tokens.count")
        self.calls.append(parameters)
        if self.error is not None:
            raise self.error
        return self.response


class FakeResponses:
    def __init__(
        self,
        response=None,
        error: Exception | None = None,
        *,
        count_response=None,
        count_error: Exception | None = None,
    ) -> None:
        self.response = response
        self.error = error
        self.calls: list[dict] = []
        self.call_order: list[str] = []
        self.input_tokens = FakeInputTokens(
            self, response=count_response, error=count_error
        )

    def create(self, **parameters):
        self.call_order.append("responses.create")
        self.calls.append(parameters)
        if self.error is not None:
            raise self.error
        return self.response


class FakeClient:
    def __init__(
        self,
        response=None,
        error: Exception | None = None,
        *,
        count_response=None,
        count_error: Exception | None = None,
    ) -> None:
        self.responses = FakeResponses(
            response,
            error,
            count_response=count_response,
            count_error=count_error,
        )


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


def _adapter(
    response=None,
    error: Exception | None = None,
    *,
    count_response=None,
    count_error: Exception | None = None,
):
    client = FakeClient(
        response,
        error,
        count_response=count_response,
        count_error=count_error,
    )
    return OpenAIResponsesAdapter(client), client


def _authorized_sheet() -> dict:
    sheet = deepcopy(load_authorization_sheet())
    sheet["authorization_status"] = "AUTHORIZED_FOR_PAID_SMOKE"
    sheet["execution_authorized"] = True
    return sheet


def _guarded_adapter(
    response=None,
    *,
    count_response=None,
    count_error: Exception | None = None,
) -> tuple[PaidSmokeGuardedAdapter, FakeClient]:
    adapter, client = _adapter(
        response,
        count_response=count_response,
        count_error=count_error,
    )
    decision = prepare_paid_smoke_execution(
        lambda: adapter,
        _authorized_sheet(),
    )
    assert decision.authorized
    assert decision.adapter is not None
    return decision.adapter, client


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


@pytest.mark.parametrize(
    ("authorization_status", "execution_authorized"),
    (
        ("PROPOSED_NOT_AUTHORIZED", False),
        ("UNRECOGNISED_AUTHORIZATION_STATE", True),
    ),
)
def test_paid_smoke_authorization_stops_before_adapter_construction_or_requests(
    authorization_status: str,
    execution_authorized: bool,
) -> None:
    sheet = deepcopy(load_authorization_sheet())
    sheet["authorization_status"] = authorization_status
    sheet["execution_authorized"] = execution_authorized
    factory_calls = 0

    def adapter_factory() -> OpenAIResponsesAdapter:
        nonlocal factory_calls
        factory_calls += 1
        raise AssertionError("unauthorized execution must not construct an adapter")

    decision = prepare_paid_smoke_execution(adapter_factory, sheet)

    assert decision.authorized is False
    assert decision.adapter is None
    assert decision.failure_reason == "PAID_SMOKE_NOT_AUTHORIZED"
    assert factory_calls == 0


def test_guarded_adapter_defence_in_depth_blocks_closed_sheet_before_requests() -> None:
    adapter, client = _adapter(_response(json.dumps(_dialogue_transport())))
    guarded = PaidSmokeGuardedAdapter(adapter, load_authorization_sheet())

    outcome = guarded.invoke("dialogue", {"player_text": "fixture"})

    assert outcome.system_failure_reason == "PAID_SMOKE_NOT_AUTHORIZED"
    assert client.responses.input_tokens.calls == []
    assert client.responses.calls == []
    assert guarded.input_token_count_requests == 0
    assert guarded.model_generation_calls == 0


def test_real_environment_boundary_uses_closed_canonical_sheet_before_key_access(
    monkeypatch,
) -> None:
    constructor_calls = 0

    def forbidden_constructor(cls):
        nonlocal constructor_calls
        constructor_calls += 1
        raise AssertionError("closed authorization must stop before key access")

    monkeypatch.setattr(
        OpenAIResponsesAdapter,
        "_from_environment_after_authorization",
        classmethod(forbidden_constructor),
    )

    decision = prepare_paid_smoke_execution_from_environment()

    assert decision.authorized is False
    assert decision.failure_reason == "PAID_SMOKE_NOT_AUTHORIZED"
    assert constructor_calls == 0


def test_paid_smoke_counts_exact_prepared_input_before_generation_at_8192() -> None:
    guarded, client = _guarded_adapter(
        _response(json.dumps(_dialogue_transport())),
        count_response=SimpleNamespace(input_tokens=8192),
    )

    outcome = guarded.invoke("dialogue", {"player_text": "fixture"})

    assert outcome.system_failure_reason is None
    assert client.responses.call_order == [
        "input_tokens.count",
        "responses.create",
    ]
    count_request = client.responses.input_tokens.calls[0]
    generation_request = client.responses.calls[0]
    token_relevant_fields = {
        "model",
        "instructions",
        "input",
        "reasoning",
        "text",
    }
    assert set(count_request) == token_relevant_fields
    assert {
        field_name: generation_request[field_name]
        for field_name in token_relevant_fields
    } == count_request
    assert count_request["text"]["format"]["strict"] is True
    assert count_request["text"]["format"]["schema"] == (
        generation_request["text"]["format"]["schema"]
    )
    for generation_only_field in ("max_output_tokens", "store", "timeout"):
        assert generation_only_field not in count_request
    assert guarded.input_token_count_requests == 1
    assert guarded.model_generation_calls == 1


def test_paid_smoke_rejects_8193_before_generation_without_truncation() -> None:
    guarded, client = _guarded_adapter(
        _response(json.dumps(_dialogue_transport())),
        count_response=SimpleNamespace(input_tokens=8193),
    )

    outcome = guarded.invoke("dialogue", {"player_text": "fixture"})

    assert outcome.system_failure_reason == "EXPECTED_INPUT_TOKENS_EXCEED_8192"
    assert len(client.responses.input_tokens.calls) == 1
    assert client.responses.calls == []
    assert guarded.input_token_count_requests == 1
    assert guarded.model_generation_calls == 0


@pytest.mark.parametrize(
    ("count_response", "count_error"),
    (
        (None, TimeoutError("provider timeout details must not leak")),
        (None, RuntimeError("provider API details must not leak")),
        (SimpleNamespace(input_tokens=None), None),
        (SimpleNamespace(input_tokens="8192"), None),
    ),
)
def test_paid_smoke_token_count_failure_fails_closed_without_generation(
    count_response,
    count_error: Exception | None,
) -> None:
    guarded, client = _guarded_adapter(
        _response(json.dumps(_dialogue_transport())),
        count_response=count_response,
        count_error=count_error,
    )

    outcome = guarded.invoke("dialogue", {"player_text": "fixture"})

    assert outcome.system_failure_reason == "INPUT_TOKEN_COUNT_FAILED"
    assert client.responses.calls == []
    assert guarded.input_token_count_requests == 1
    assert guarded.model_generation_calls == 0
    if count_error is not None:
        assert str(count_error) not in repr(outcome)


def test_paid_smoke_refuses_ninth_model_generation_call_before_count_or_create() -> None:
    guarded, client = _guarded_adapter(
        _response(json.dumps(_dialogue_transport())),
        count_response=SimpleNamespace(input_tokens=100),
    )

    for _ in range(8):
        assert guarded.invoke(
            "dialogue", {"player_text": "fixture"}
        ).system_failure_reason is None
    ninth = guarded.invoke("dialogue", {"player_text": "fixture"})

    assert ninth.system_failure_reason == "MODEL_GENERATION_CALL_LIMIT_EXCEEDED"
    assert len(client.responses.input_tokens.calls) == 8
    assert len(client.responses.calls) == 8
    assert guarded.input_token_count_requests == 8
    assert guarded.model_generation_calls == 8


def test_paid_smoke_enforces_separate_input_token_count_request_ceiling() -> None:
    guarded, client = _guarded_adapter(
        _response(json.dumps(_dialogue_transport())),
        count_error=TimeoutError("do not expose"),
    )

    for _ in range(8):
        assert guarded.invoke(
            "dialogue", {"player_text": "fixture"}
        ).system_failure_reason == "INPUT_TOKEN_COUNT_FAILED"
    ninth = guarded.invoke("dialogue", {"player_text": "fixture"})

    assert ninth.system_failure_reason == (
        "INPUT_TOKEN_COUNT_REQUEST_LIMIT_EXCEEDED"
    )
    assert len(client.responses.input_tokens.calls) == 8
    assert client.responses.calls == []
    assert guarded.input_token_count_requests == 8
    assert guarded.model_generation_calls == 0


def test_existing_runner_with_guarded_execution_never_creates_third_model_attempt(
    dialogue_catalogue: RuntimeCatalogue,
) -> None:
    guarded, client = _guarded_adapter(
        _response("not-json"),
        count_response=SimpleNamespace(input_tokens=100),
    )
    runner = BaselineRunner(
        guarded,
        manifest_version="0.1.1",
        contract_version="0.1.1",
    )

    result = runner.run_dialogue(
        run_id="GUARDED-RETRY",
        case_id="dialogue-d18-valid",
        model_input={"player_text": "fixture"},
        catalogue=dialogue_catalogue,
    )

    assert result.attempt_count == 2
    assert result.retry_used is True
    assert len(client.responses.input_tokens.calls) == 2
    assert len(client.responses.calls) == 2
    assert guarded.input_token_count_requests == 2
    assert guarded.model_generation_calls == 2


def test_fake_secret_never_reaches_guard_result_log_or_measurement(
    monkeypatch,
    capsys,
    dialogue_catalogue: RuntimeCatalogue,
) -> None:
    secret = "test-only-openai-" + "secret-must-not-appear"
    monkeypatch.setenv("OPENAI_API_KEY", secret)
    guarded, _ = _guarded_adapter(
        _response(
            json.dumps(_dialogue_transport()),
            input_tokens=100,
            output_tokens=20,
        ),
        count_response=SimpleNamespace(input_tokens=100),
    )
    runner = BaselineRunner(
        guarded,
        manifest_version="0.1.1",
        contract_version="0.1.1",
    )

    result = runner.run_dialogue(
        run_id="NO-SECRET",
        case_id="dialogue-d18-valid",
        model_input={"player_text": "fixture"},
        catalogue=dialogue_catalogue,
    )

    assert secret not in repr(result)
    assert secret not in json.dumps(result.measurement.as_dict())
    assert secret not in capsys.readouterr().out


def test_authorized_environment_boundary_disables_sdk_retries_without_request(
    monkeypatch,
) -> None:
    captured: dict = {}

    class ClientWithoutRequests:
        def __init__(self, **kwargs) -> None:
            captured.update(kwargs)

    monkeypatch.setenv("OPENAI_API_KEY", "test-key-parts-never-logged")
    monkeypatch.setattr(adapter_module, "OpenAI", ClientWithoutRequests)

    decision = prepare_paid_smoke_execution(
        OpenAIResponsesAdapter._from_environment_after_authorization,
        _authorized_sheet(),
    )

    assert decision.authorized
    assert decision.adapter is not None
    adapter = decision.adapter
    assert adapter.model_identifier == "gpt-5.6-terra"
    assert "api_key" in captured
    assert captured["admin_api_key"] == ""
    assert captured["organization"] == ""
    assert captured["project"] == ""
    assert captured["webhook_secret"] == ""
    assert captured["base_url"] == "https://api.openai.com/v1"
    assert captured["max_retries"] == 0
    assert captured["timeout"] == 30.0
