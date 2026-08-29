from __future__ import annotations

import pytest

from ai.prototype.validation import (
    RuntimeCatalogue,
    evaluate_headline_baseline,
    validate_headline_candidate,
)


def _candidate(case: dict) -> dict:
    return case["model_facing_input"]["injected_candidate"]


@pytest.mark.parametrize("case_id", ["headline-t01-four-claims", "headline-t02-zero-claims"])
def test_resolved_headline_cases_are_publication_ready(
    case_id: str, cases_by_id: dict, headline_catalogue: RuntimeCatalogue
) -> None:
    candidate = cases_by_id[case_id]["expected_result"]["candidate"]
    result = validate_headline_candidate(candidate, headline_catalogue)
    baseline = evaluate_headline_baseline(candidate, candidate, headline_catalogue)
    assert result.can_proceed
    assert baseline.runtime_contract.can_proceed
    assert baseline.semantic_fidelity.passed


@pytest.mark.parametrize("case_id", ["headline-f02-illegal-commitment", "headline-f03-invalid-target"])
def test_structural_and_catalogue_headline_faults_are_rejected(
    case_id: str, cases_by_id: dict, headline_catalogue: RuntimeCatalogue
) -> None:
    result = validate_headline_candidate(_candidate(cases_by_id[case_id]), headline_catalogue)
    assert not result.can_proceed
    assert result.failure_class == "AI_SYSTEM_FAILURE"


def test_f04_incomplete_claim_set_is_caught_by_fixture_oracle(
    cases_by_id: dict, headline_catalogue: RuntimeCatalogue
) -> None:
    candidate = _candidate(cases_by_id["headline-f04-incomplete-claim-set"])
    expected = cases_by_id["headline-t01-four-claims"]["expected_result"]["candidate"]
    baseline = evaluate_headline_baseline(candidate, expected, headline_catalogue)
    assert baseline.runtime_contract.can_proceed
    assert not baseline.semantic_fidelity.passed
    assert baseline.semantic_fidelity.reasons == ("FIXTURE_CLAIM_SET_MISMATCH",)


def test_f05_extra_claim_is_caught_by_fixture_oracle(
    cases_by_id: dict, headline_catalogue: RuntimeCatalogue
) -> None:
    candidate = _candidate(cases_by_id["headline-f05-invented-extra-claim"])
    expected = cases_by_id["headline-t10-single-claim"]["expected_result"]["candidate"]
    baseline = evaluate_headline_baseline(candidate, expected, headline_catalogue)
    assert baseline.runtime_contract.can_proceed
    assert not baseline.semantic_fidelity.passed


@pytest.mark.parametrize(
    ("claim", "reason"),
    [
        (
            {"target_id": "FIRE_FIRST", "polarity": "AFFIRM", "commitment_mode": "ASSERTED"},
            "CLAIM_0:VALUE_REQUIRED",
        ),
        (
            {
                "target_id": "FIRE_FIRST",
                "value_id": "COMPANY_A",
                "polarity": "AFFIRM",
                "commitment_mode": "ASSERTED",
            },
            "CLAIM_0:VALUE_NOT_ALLOWED_FOR_TARGET",
        ),
        (
            {
                "target_id": "FIRE_FIRST",
                "value_id": "MILITIA",
                "commitment_mode": "ASSERTED",
            },
            "CLAIM_0:POLARITY_REQUIRED",
        ),
        (
            {
                "target_id": "DIALOGUE_ONLY",
                "commitment_mode": "ASSERTED",
            },
            "CLAIM_0:TARGET_NOT_HEADLINE_ELIGIBLE",
        ),
        (
            {
                "target_id": "FIRE_FIRST",
                "value_id": "MILITIA",
                "polarity": "AFFIRM",
                "commitment_mode": "ASSERTED",
                "source_ref_id": "SRC_SECRET_99",
            },
            "CLAIM_0:SOURCE_UNAVAILABLE_OR_NONEXISTENT",
        ),
    ],
)
def test_headline_conditional_and_visibility_rules(
    claim: dict, reason: str, headline_catalogue: RuntimeCatalogue
) -> None:
    result = validate_headline_candidate(
        {"status": "RESOLVED", "claims": [claim]}, headline_catalogue
    )
    assert not result.can_proceed
    assert reason in result.reasons


@pytest.mark.parametrize("status", ["AMBIGUOUS", "UNSUPPORTED"])
def test_unresolved_headline_is_never_publication_ready(
    status: str, headline_catalogue: RuntimeCatalogue
) -> None:
    result = validate_headline_candidate({"status": status}, headline_catalogue)
    assert not result.can_proceed
    assert result.failure_class == "SEMANTIC_FAILURE"


def test_publication_support_label_is_not_a_claim_atom_field(
    headline_catalogue: RuntimeCatalogue,
) -> None:
    result = validate_headline_candidate(
        {
            "status": "RESOLVED",
            "claims": [{
                "target_id": "FIRE_FIRST",
                "value_id": "MILITIA",
                "polarity": "AFFIRM",
                "commitment_mode": "ASSERTED",
                "publication_support": "SUPPORTED",
            }],
        },
        headline_catalogue,
    )
    assert not result.can_proceed
    assert result.failure_class == "AI_SYSTEM_FAILURE"
