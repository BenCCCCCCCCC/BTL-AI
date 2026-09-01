from __future__ import annotations

import inspect
import json

import pytest

from ai.prototype import runner as runner_module
from ai.prototype.adapters import AdapterOutcome, ScriptedAdapter
from ai.prototype.npc_output_gate import LexicalRule, NPCFixtureValidationMetadata
from ai.prototype.runner import AuthoredNPCFallback, BaselineRunner
from ai.prototype.validation import RuntimeCatalogue


DIALOGUE_VALID = {
    "status": "RESOLVED",
    "act": "REQUEST",
    "target_id": "REVEAL_PAYMENT_PAYER",
    "tactics": ["INDIRECT_PROBE", "ACCUSATION", "THREAT"],
    "evidence_ref_ids": ["PHOTO_01"],
}
DIALOGUE_INVALID = {
    "status": "RESOLVED",
    "act": "INTIMIDATE",
    "target_id": "REVEAL_PAYMENT_PAYER",
}
HEADLINE_VALID = {
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
HEADLINE_INVALID = {
    "status": "RESOLVED",
    "claims": [
        {
            "target_id": "FIRE_FIRST",
            "value_id": "SECURITY_FORCES",
            "polarity": "AFFIRM",
            "commitment_mode": "CERTAIN_TRUE",
        }
    ],
}
HEADLINE_ZERO_CLAIMS = {"status": "RESOLVED", "claims": []}


def _runner(*outcomes: AdapterOutcome) -> tuple[BaselineRunner, ScriptedAdapter]:
    adapter = ScriptedAdapter(outcomes)
    return (
        BaselineRunner(
            adapter,
            manifest_version="0.1.1",
            contract_version="0.1.1",
        ),
        adapter,
    )


def _npc_metadata() -> NPCFixtureValidationMetadata:
    return NPCFixtureValidationMetadata(
        required_content=(
            LexicalRule("PAYER_COMPANY_A", (r"company\s+a\s+paid",)),
        ),
        canon_lexemes={"COMPANY_A": (r"company\s+a",)},
        authorised_canon_ids=frozenset({"COMPANY_A"}),
        unauthorised_commitments=(
            LexicalRule(
                "LEDGER_PROMISE",
                (r"i(?:'ll|\s+will)\s+give\s+you\s+the\s+ledger",),
            ),
        ),
    )


def _run_dialogue(
    runner: BaselineRunner,
    catalogue: RuntimeCatalogue,
    expected_candidate: dict | None = None,
):
    return runner.run_dialogue(
        run_id="RUN-DIALOGUE",
        case_id="CASE-DIALOGUE",
        model_input={"player_text": "fixture input"},
        catalogue=catalogue,
        expected_candidate=expected_candidate,
    )


def _run_headline(
    runner: BaselineRunner,
    catalogue: RuntimeCatalogue,
    expected_candidate: dict | None = None,
):
    return runner.run_headline(
        run_id="RUN-HEADLINE",
        case_id="CASE-HEADLINE",
        model_input={"headline_text": "fixture input"},
        catalogue=catalogue,
        expected_candidate=expected_candidate,
    )


def _run_npc(
    runner: BaselineRunner,
    fallback: AuthoredNPCFallback | None = None,
):
    if fallback is None:
        fallback = AuthoredNPCFallback("ANSWER", "Company A paid me.")
    return runner.run_npc_surface(
        run_id="RUN-NPC",
        case_id="CASE-NPC",
        model_input={"response_mode": "ANSWER"},
        response_mode="ANSWER",
        metadata=_npc_metadata(),
        authored_fallback=fallback,
    )


def test_dialogue_first_candidate_valid_uses_no_retry(
    dialogue_catalogue: RuntimeCatalogue,
) -> None:
    runner, adapter = _runner(AdapterOutcome.success(DIALOGUE_VALID))

    result = _run_dialogue(runner, dialogue_catalogue)

    assert result.validated_output == DIALOGUE_VALID
    assert result.first_pass_runtime_result == "PASS"
    assert result.final_runtime_result == "PASS"
    assert result.attempt_count == 1
    assert not result.retry_used
    assert len(adapter.calls) == 1


def test_dialogue_system_invalid_then_valid_retries_once(
    dialogue_catalogue: RuntimeCatalogue,
) -> None:
    runner, _ = _runner(
        AdapterOutcome.system_failure("TIMEOUT"),
        AdapterOutcome.success(DIALOGUE_VALID),
    )

    result = _run_dialogue(runner, dialogue_catalogue)

    assert result.validated_output == DIALOGUE_VALID
    assert result.first_pass_runtime_result == "AI_SYSTEM_FAILURE"
    assert result.final_runtime_result == "PASS"
    assert result.attempt_count == 2
    assert result.retry_used


def test_dialogue_retry_exhaustion_is_safe_and_fabricates_no_action(
    dialogue_catalogue: RuntimeCatalogue,
) -> None:
    runner, _ = _runner(
        AdapterOutcome.success(DIALOGUE_INVALID),
        AdapterOutcome.system_failure("TIMEOUT"),
    )

    result = _run_dialogue(runner, dialogue_catalogue)

    assert result.validated_output is None
    assert result.final_runtime_result == "AI_SYSTEM_FAILURE"
    assert result.attempt_count == 2
    assert result.retry_used
    assert result.safe_non_consequential
    assert "RETRY_EXHAUSTED" in result.reasons
    assert not result.hard_safety_gate_breach


@pytest.mark.parametrize("status", ["AMBIGUOUS", "UNSUPPORTED"])
def test_dialogue_semantic_failure_does_not_retry(
    status: str, dialogue_catalogue: RuntimeCatalogue
) -> None:
    runner, adapter = _runner(AdapterOutcome.success({"status": status}))

    result = _run_dialogue(runner, dialogue_catalogue)

    assert result.validated_output is None
    assert result.final_runtime_result == "SEMANTIC_FAILURE"
    assert result.attempt_count == 1
    assert not result.retry_used
    assert len(adapter.calls) == 1


def test_dialogue_fidelity_failure_is_recorded_without_runtime_retry(
    dialogue_catalogue: RuntimeCatalogue,
) -> None:
    truncated = DIALOGUE_VALID | {"tactics": ["ACCUSATION", "THREAT"]}
    runner, adapter = _runner(AdapterOutcome.success(truncated))

    result = _run_dialogue(runner, dialogue_catalogue, DIALOGUE_VALID)

    assert result.final_runtime_result == "PASS"
    assert result.validated_output == truncated
    assert result.semantic_fidelity is not None
    assert not result.semantic_fidelity.passed
    assert not result.retry_used
    assert len(adapter.calls) == 1


def test_headline_first_candidate_valid_may_continue(
    headline_catalogue: RuntimeCatalogue,
) -> None:
    runner, _ = _runner(AdapterOutcome.success(HEADLINE_VALID))

    result = _run_headline(runner, headline_catalogue)

    assert result.validated_output == HEADLINE_VALID
    assert result.publication_ready is True
    assert result.attempt_count == 1
    assert not result.retry_used


def test_headline_invalid_then_valid_retries_once(
    headline_catalogue: RuntimeCatalogue,
) -> None:
    runner, _ = _runner(
        AdapterOutcome.success(HEADLINE_INVALID),
        AdapterOutcome.success(HEADLINE_VALID),
    )

    result = _run_headline(runner, headline_catalogue)

    assert result.validated_output == HEADLINE_VALID
    assert result.first_pass_runtime_result == "AI_SYSTEM_FAILURE"
    assert result.final_runtime_result == "PASS"
    assert result.attempt_count == 2
    assert result.retry_used


def test_headline_retry_exhaustion_blocks_publication_and_fabricates_no_claim_set(
    headline_catalogue: RuntimeCatalogue,
) -> None:
    runner, _ = _runner(
        AdapterOutcome.success(HEADLINE_INVALID),
        AdapterOutcome.system_failure("TIMEOUT"),
    )

    result = _run_headline(runner, headline_catalogue)

    assert result.validated_output is None
    assert result.publication_ready is False
    assert result.draft_preserved is True
    assert result.safe_non_consequential
    assert result.validated_output != HEADLINE_ZERO_CLAIMS
    assert "RETRY_EXHAUSTED" in result.reasons
    assert not result.hard_safety_gate_breach


@pytest.mark.parametrize("status", ["AMBIGUOUS", "UNSUPPORTED"])
def test_headline_semantic_failure_blocks_publication_without_retry(
    status: str, headline_catalogue: RuntimeCatalogue
) -> None:
    runner, adapter = _runner(AdapterOutcome.success({"status": status}))

    result = _run_headline(runner, headline_catalogue)

    assert result.validated_output is None
    assert result.publication_ready is False
    assert result.final_runtime_result == "SEMANTIC_FAILURE"
    assert not result.retry_used
    assert len(adapter.calls) == 1


def test_headline_fidelity_failure_is_evaluation_only(
    headline_catalogue: RuntimeCatalogue,
) -> None:
    extra_claim = HEADLINE_VALID["claims"][0] | {
        "target_id": "ORDERED_OPERATION",
        "value_id": "MAYOR_OFFICE",
    }
    candidate = {
        "status": "RESOLVED",
        "claims": [HEADLINE_VALID["claims"][0], extra_claim],
    }
    runner, adapter = _runner(AdapterOutcome.success(candidate))

    result = _run_headline(runner, headline_catalogue, HEADLINE_VALID)

    assert result.final_runtime_result == "PASS"
    assert result.publication_ready is True
    assert result.semantic_fidelity is not None
    assert not result.semantic_fidelity.passed
    assert not result.retry_used
    assert len(adapter.calls) == 1


def test_headline_measurement_distinguishes_zero_claims_semantic_and_exhaustion(
    headline_catalogue: RuntimeCatalogue,
) -> None:
    zero_runner, _ = _runner(AdapterOutcome.success(HEADLINE_ZERO_CLAIMS))
    exhausted_runner, _ = _runner(
        AdapterOutcome.success(HEADLINE_INVALID),
        AdapterOutcome.system_failure("TIMEOUT"),
    )
    semantic_runner, _ = _runner(AdapterOutcome.success({"status": "AMBIGUOUS"}))

    zero_claims = _run_headline(
        zero_runner, headline_catalogue, HEADLINE_ZERO_CLAIMS
    )
    exhausted = _run_headline(exhausted_runner, headline_catalogue)
    semantic = _run_headline(semantic_runner, headline_catalogue)

    assert zero_claims.validated_output == HEADLINE_ZERO_CLAIMS
    assert zero_claims.measurement.final_runtime_result == "PASS"
    assert zero_claims.measurement.semantic_fidelity_result == "PASS"
    assert zero_claims.measurement.publication_ready is True

    assert exhausted.validated_output is None
    assert exhausted.measurement.final_runtime_result == "AI_SYSTEM_FAILURE"
    assert exhausted.measurement.semantic_fidelity_result is None
    assert exhausted.measurement.publication_ready is False
    assert "RETRY_EXHAUSTED" in exhausted.measurement.reason_codes

    assert semantic.validated_output is None
    assert semantic.measurement.final_runtime_result == "SEMANTIC_FAILURE"
    assert semantic.measurement.semantic_fidelity_result is None
    assert semantic.measurement.publication_ready is False
    assert "AMBIGUOUS" in semantic.measurement.reason_codes


def test_npc_first_surface_valid_is_displayed_without_retry() -> None:
    runner, _ = _runner(AdapterOutcome.success("Company A paid me."))

    result = _run_npc(runner)

    assert result.validated_output == "Company A paid me."
    assert result.display_ready is True
    assert result.attempt_count == 1
    assert not result.retry_used


def test_npc_first_gate_failure_is_never_displayed_and_second_passes() -> None:
    runner, _ = _runner(
        AdapterOutcome.success("I refuse to say."),
        AdapterOutcome.success("Company A paid me."),
    )

    result = _run_npc(runner)

    assert result.validated_output == "Company A paid me."
    assert result.display_ready is True
    assert result.attempt_count == 2
    assert result.retry_used
    assert "I refuse to say." not in str(result)


def test_npc_two_gate_failures_use_authored_validated_fallback() -> None:
    runner, _ = _runner(
        AdapterOutcome.success("I refuse to say."),
        AdapterOutcome.success("Still refusing."),
    )
    fallback = AuthoredNPCFallback("ANSWER", "Company A paid me.")

    result = _run_npc(runner, fallback)

    assert result.validated_output == fallback.surface_text
    assert result.display_ready is True
    assert result.fallback_used
    assert result.fallback_type == "AUTHORED_TEMPLATE"
    assert result.final_runtime_result == "PASS"


def test_npc_fallback_cannot_change_response_mode() -> None:
    runner, _ = _runner(
        AdapterOutcome.success("I refuse to say."),
        AdapterOutcome.success("Still refusing."),
    )
    wrong_mode = AuthoredNPCFallback("REFUSE", "Company A paid me.")

    result = _run_npc(runner, wrong_mode)

    assert result.validated_output is None
    assert result.display_ready is False
    assert "FALLBACK_RESPONSE_MODE_MISMATCH" in result.reasons
    assert not result.hard_safety_gate_breach


def test_npc_fallback_must_pass_gate_before_display() -> None:
    runner, _ = _runner(
        AdapterOutcome.success("I refuse to say."),
        AdapterOutcome.success("Still refusing."),
    )
    invalid_fallback = AuthoredNPCFallback("ANSWER", "I refuse to say.")

    result = _run_npc(runner, invalid_fallback)

    assert result.validated_output is None
    assert result.display_ready is False
    assert result.fallback_used
    assert "MISSING_REQUIRED_CONTENT:PAYER_COMPANY_A" in result.reasons
    assert not result.hard_safety_gate_breach


def test_unauthorised_npc_commitment_is_never_displayed() -> None:
    runner, _ = _runner(
        AdapterOutcome.success("Company A paid me. I'll give you the ledger."),
        AdapterOutcome.success("Company A paid me."),
    )

    result = _run_npc(runner)

    assert result.validated_output == "Company A paid me."
    assert result.display_ready is True
    assert "ledger" not in result.validated_output.lower()
    assert "UNAUTHORISED_COMMITMENT:LEDGER_PROMISE" in result.reasons


def test_measurement_record_is_jsonl_compatible_and_does_not_invent_usage(
    tmp_path, dialogue_catalogue: RuntimeCatalogue
) -> None:
    output_path = tmp_path / "runs.jsonl"
    runner, _ = _runner(AdapterOutcome.success(DIALOGUE_VALID))

    result = runner.run_dialogue(
        run_id="RUN-JSONL",
        case_id="dialogue-d18-valid",
        model_input={"player_text": "fixture input"},
        catalogue=dialogue_catalogue,
        expected_candidate=DIALOGUE_VALID,
        measurement_path=output_path,
    )

    record = json.loads(output_path.read_text(encoding="utf-8"))
    assert record == result.measurement.as_dict()
    assert record["component"] == "dialogue"
    assert record["manifest_version"] == "0.1.1"
    assert record["contract_version"] == "0.1.1"
    assert record["adapter_identifier"] == "scripted"
    assert record["attempt_count"] == 1
    assert record["first_pass_runtime_result"] == "PASS"
    assert record["final_runtime_result"] == "PASS"
    assert record["expected_safety_disposition"] is None
    assert record["actual_safety_disposition"] == "ACCEPT"
    assert record["semantic_fidelity_result"] == "PASS"
    assert record["model_identifier"] is None
    assert record["input_tokens"] is None
    assert record["output_tokens"] is None
    assert record["model_call_latency_ms"] is None
    assert record["estimated_cost"] is None
    assert record["hard_safety_gate_breach"] is False


def test_expected_reject_and_actual_accept_is_explicit_hard_safety_breach(
    dialogue_catalogue: RuntimeCatalogue,
) -> None:
    runner, _ = _runner(AdapterOutcome.success(DIALOGUE_VALID))

    result = runner.run_dialogue(
        run_id="RUN-SAFETY",
        case_id="FAULT-INJECTION",
        model_input={"injected_candidate": DIALOGUE_VALID},
        catalogue=dialogue_catalogue,
        expected_safety_disposition="REJECT",
    )

    assert result.expected_safety_disposition == "REJECT"
    assert result.actual_safety_disposition == "ACCEPT"
    assert result.measurement.expected_safety_disposition == "REJECT"
    assert result.measurement.actual_safety_disposition == "ACCEPT"
    assert result.hard_safety_gate_breach is True


def test_expected_reject_is_compared_with_first_attempt_not_retry_result(
    dialogue_catalogue: RuntimeCatalogue,
) -> None:
    runner, _ = _runner(
        AdapterOutcome.success(DIALOGUE_INVALID),
        AdapterOutcome.success(DIALOGUE_VALID),
    )

    result = runner.run_dialogue(
        run_id="RUN-SAFETY-RETRY",
        case_id="FAULT-INJECTION",
        model_input={"injected_candidate": DIALOGUE_INVALID},
        catalogue=dialogue_catalogue,
        expected_safety_disposition="REJECT",
    )

    assert result.actual_safety_disposition == "REJECT"
    assert result.final_runtime_result == "PASS"
    assert result.hard_safety_gate_breach is False


def test_runner_has_no_game_state_or_consequence_authority(
    dialogue_catalogue: RuntimeCatalogue,
) -> None:
    authority_attempt = DIALOGUE_VALID | {
        "branch_id": "BRANCH_99",
        "state_delta": {"Reputation": 99},
        "evidence": ["SECRET_EVIDENCE"],
    }
    runner, _ = _runner(
        AdapterOutcome.success(authority_attempt),
        AdapterOutcome.success(DIALOGUE_VALID),
    )

    result = _run_dialogue(runner, dialogue_catalogue)

    assert result.validated_output == DIALOGUE_VALID
    assert result.retry_used
    assert not result.hard_safety_gate_breach
    assert "consequence_stub" not in inspect.getsource(runner_module)
    for authority_field in ("state_delta", "evidence", "branch_id", "consequence_event"):
        assert not hasattr(result, authority_field)
