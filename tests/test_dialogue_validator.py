from __future__ import annotations

import pytest

from ai.prototype.validation import (
    RuntimeCatalogue,
    evaluate_dialogue_baseline,
    validate_dialogue_candidate,
)


def _candidate(case: dict) -> dict:
    return case["model_facing_input"]["injected_candidate"]


def test_d18_valid_candidate_and_exact_fixture_oracle(
    cases_by_id: dict, dialogue_catalogue: RuntimeCatalogue
) -> None:
    expected = cases_by_id["dialogue-d18-valid"]["expected_result"]["candidate"]
    result = validate_dialogue_candidate(expected, dialogue_catalogue)
    baseline = evaluate_dialogue_baseline(expected, expected, dialogue_catalogue)
    assert result.can_proceed
    assert result.failure_class == "NONE"
    assert baseline.runtime_contract.can_proceed
    assert baseline.semantic_fidelity.passed


def test_d19_tactic_truncation_is_caught_only_by_fixture_oracle(
    cases_by_id: dict, dialogue_catalogue: RuntimeCatalogue
) -> None:
    candidate = _candidate(cases_by_id["dialogue-d19-tactic-truncation"])
    expected = cases_by_id["dialogue-d18-valid"]["expected_result"]["candidate"]
    baseline = evaluate_dialogue_baseline(candidate, expected, dialogue_catalogue)
    assert baseline.runtime_contract.can_proceed
    assert not baseline.semantic_fidelity.passed
    assert baseline.semantic_fidelity.reasons == ("FIXTURE_SEMANTIC_MISMATCH",)


@pytest.mark.parametrize(
    "case_id",
    [
        "dialogue-d20-duplicate-tactic",
        "dialogue-d30-illegal-act",
        "dialogue-d31-invalid-target",
    ],
)
def test_dialogue_fault_injections_are_system_failures(
    case_id: str, cases_by_id: dict, dialogue_catalogue: RuntimeCatalogue
) -> None:
    result = validate_dialogue_candidate(_candidate(cases_by_id[case_id]), dialogue_catalogue)
    assert not result.can_proceed
    assert result.failure_class == "AI_SYSTEM_FAILURE"


def test_semantic_failure_stays_distinct_from_system_failure(
    dialogue_catalogue: RuntimeCatalogue,
) -> None:
    semantic = validate_dialogue_candidate(
        {"status": "UNSUPPORTED", "reason": "OUT_OF_CATALOGUE"}, dialogue_catalogue
    )
    system = validate_dialogue_candidate(
        {"status": "RESOLVED", "act": "QUESTION", "target_id": "SECRET_TARGET_99"},
        dialogue_catalogue,
    )
    assert semantic.failure_class == "SEMANTIC_FAILURE"
    assert system.failure_class == "AI_SYSTEM_FAILURE"
    assert not semantic.can_proceed and not system.can_proceed


@pytest.mark.parametrize(
    ("candidate", "reason"),
    [
        (
            {"status": "RESOLVED", "act": "ASSERTION", "target_id": "PAYMENT_PAYER"},
            "VALUE_REQUIRED",
        ),
        (
            {
                "status": "RESOLVED",
                "act": "ASSERTION",
                "target_id": "PAYMENT_PAYER",
                "value_id": "WAREHOUSE",
                "polarity": "AFFIRM",
            },
            "VALUE_NOT_ALLOWED_FOR_TARGET",
        ),
        (
            {
                "status": "RESOLVED",
                "act": "ASSERTION",
                "target_id": "PAYMENT_PAYER",
                "value_id": "COMPANY_A",
            },
            "POLARITY_REQUIRED",
        ),
        (
            {
                "status": "RESOLVED",
                "act": "REQUEST",
                "target_id": "HAND_OVER_LEDGER",
                "evidence_ref_ids": ["SECRET_PHOTO_99"],
            },
            "EVIDENCE_UNAVAILABLE_OR_NONEXISTENT",
        ),
        (
            {"status": "RESOLVED", "act": "OFFER", "target_id": "HAND_OVER_LEDGER"},
            "ACT_NOT_ALLOWED_FOR_TARGET",
        ),
    ],
)
def test_dialogue_conditional_catalogue_rules(
    candidate: dict, reason: str, dialogue_catalogue: RuntimeCatalogue
) -> None:
    result = validate_dialogue_candidate(candidate, dialogue_catalogue)
    assert not result.can_proceed
    assert reason in result.reasons


def test_accept_refuse_requires_one_deterministic_pending_interaction(
    dialogue_catalogue: RuntimeCatalogue,
) -> None:
    assert validate_dialogue_candidate(
        {"status": "RESOLVED", "act": "ACCEPT"}, dialogue_catalogue
    ).can_proceed

    no_pending = RuntimeCatalogue(
        targets=dialogue_catalogue.targets,
        visible_evidence_ids=dialogue_catalogue.visible_evidence_ids,
    )
    result = validate_dialogue_candidate({"status": "RESOLVED", "act": "REFUSE"}, no_pending)
    assert not result.can_proceed
    assert result.reasons == ("PENDING_INTERACTION_NOT_UNIQUE",)


def test_model_cannot_select_pending_interaction_context(
    dialogue_catalogue: RuntimeCatalogue,
) -> None:
    result = validate_dialogue_candidate(
        {"status": "RESOLVED", "act": "ACCEPT", "target_id": "DEAL_LEDGER_FOR_500"},
        dialogue_catalogue,
    )
    assert not result.can_proceed
    assert result.reasons == ("MODEL_SELECTED_PENDING_INTERACTION_CONTEXT",)


def test_pending_interaction_must_allow_the_selected_act(
    dialogue_catalogue: RuntimeCatalogue,
) -> None:
    accept_only = RuntimeCatalogue(
        targets=dialogue_catalogue.targets,
        visible_evidence_ids=dialogue_catalogue.visible_evidence_ids,
        pending_interaction_ids=frozenset({"PENDING_01"}),
        pending_interaction_allowed_acts={"PENDING_01": frozenset({"ACCEPT"})},
    )
    result = validate_dialogue_candidate(
        {"status": "RESOLVED", "act": "REFUSE"}, accept_only
    )
    assert not result.can_proceed
    assert result.reasons == ("PENDING_INTERACTION_NOT_VALID_FOR_ACT",)
