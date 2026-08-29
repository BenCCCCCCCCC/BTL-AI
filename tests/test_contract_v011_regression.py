from __future__ import annotations

import pytest

from ai.prototype.validation import (
    RuntimeCatalogue,
    evaluate_dialogue_baseline,
    evaluate_headline_baseline,
    validate_dialogue_candidate,
    validate_headline_candidate,
)


MATRIX = (
    ("D18", "dialogue-d18-valid", "dialogue-d18-valid", "dialogue", True),
    ("D19", "dialogue-d19-tactic-truncation", "dialogue-d18-valid", "dialogue", False),
    ("T01", "headline-t01-four-claims", "headline-t01-four-claims", "headline", True),
    ("F04", "headline-f04-incomplete-claim-set", "headline-t01-four-claims", "headline", False),
    ("T10", "headline-t10-single-claim", "headline-t10-single-claim", "headline", True),
    ("F05", "headline-f05-invented-extra-claim", "headline-t10-single-claim", "headline", False),
)


def _candidate(case: dict) -> dict:
    return case["model_facing_input"].get(
        "injected_candidate", case["expected_result"].get("candidate")
    )


@pytest.mark.parametrize(
    ("source_case_id", "case_id", "expected_case_id", "component", "fidelity_passes"),
    MATRIX,
    ids=[row[0] for row in MATRIX],
)
def test_v011_runtime_contract_and_semantic_fidelity_matrix(
    source_case_id: str,
    case_id: str,
    expected_case_id: str,
    component: str,
    fidelity_passes: bool,
    cases_by_id: dict,
    dialogue_catalogue: RuntimeCatalogue,
    headline_catalogue: RuntimeCatalogue,
) -> None:
    del source_case_id
    candidate = _candidate(cases_by_id[case_id])
    expected = cases_by_id[expected_case_id]["expected_result"]["candidate"]
    if component == "dialogue":
        evaluation = evaluate_dialogue_baseline(candidate, expected, dialogue_catalogue)
    else:
        evaluation = evaluate_headline_baseline(candidate, expected, headline_catalogue)

    manifest_expectation = cases_by_id[case_id]["expected_result"]
    assert manifest_expectation["runtime_contract"] == "PASS"
    assert manifest_expectation["semantic_fidelity"] == (
        "PASS" if fidelity_passes else "FAIL"
    )
    assert evaluation.runtime_contract.can_proceed
    assert evaluation.runtime_contract.failure_class == "NONE"
    assert evaluation.semantic_fidelity.passed is fidelity_passes


@pytest.mark.parametrize(
    ("case_id", "component"),
    (
        ("dialogue-d20-duplicate-tactic", "dialogue"),
        ("dialogue-d30-illegal-act", "dialogue"),
        ("dialogue-d31-invalid-target", "dialogue"),
        ("headline-f02-illegal-commitment", "headline"),
    ),
    ids=("duplicate-tactics", "illegal-dialogue-enum", "invalid-id", "illegal-commitment-mode"),
)
def test_v011_representative_runtime_contract_rejections(
    case_id: str,
    component: str,
    cases_by_id: dict,
    dialogue_catalogue: RuntimeCatalogue,
    headline_catalogue: RuntimeCatalogue,
) -> None:
    candidate = _candidate(cases_by_id[case_id])
    if component == "dialogue":
        result = validate_dialogue_candidate(candidate, dialogue_catalogue)
    else:
        result = validate_headline_candidate(candidate, headline_catalogue)
    assert not result.can_proceed
    assert result.failure_class == "AI_SYSTEM_FAILURE"


def test_v011_unresolved_headline_cannot_become_publication_ready(
    headline_catalogue: RuntimeCatalogue,
) -> None:
    result = validate_headline_candidate(
        {"status": "UNSUPPORTED", "reason": "OUT_OF_CATALOGUE"},
        headline_catalogue,
    )
    assert not result.can_proceed
    assert result.failure_class == "SEMANTIC_FAILURE"


def test_v011_unauthorised_structured_output_is_rejected(
    headline_catalogue: RuntimeCatalogue,
) -> None:
    result = validate_headline_candidate(
        {
            "status": "RESOLVED",
            "claims": [
                {
                    "target_id": "FIRE_FIRST",
                    "value_id": "MILITIA",
                    "polarity": "AFFIRM",
                    "commitment_mode": "ASSERTED",
                    "publication_support": "SUPPORTED",
                }
            ],
        },
        headline_catalogue,
    )
    assert not result.can_proceed
    assert result.failure_class == "AI_SYSTEM_FAILURE"


def test_v011_manifest_declares_fidelity_as_evaluation_only(manifest: dict) -> None:
    fidelity = manifest["assurance_layers"]["semantic_fidelity"]
    assert fidelity["scope"] == "Evaluation-only comparison with authored fixture ground truth"
    assert fidelity["production_runtime_retry_trigger"] is False
