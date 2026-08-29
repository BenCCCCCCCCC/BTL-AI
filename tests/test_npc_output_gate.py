from __future__ import annotations

from ai.prototype.npc_output_gate import (
    LexicalRule,
    NPCFixtureValidationMetadata,
    metadata_from_mapping,
    validate_npc_surface_text,
)


def test_manifest_npc_faults_fail_with_the_expected_reason(
    manifest: dict, cases_by_id: dict
) -> None:
    metadata_by_id = manifest["npc_output_validation_metadata"]
    for case_id in (
        "npc-n12-missing-required",
        "npc-n13-forbidden-disclosure",
        "npc-n11-unauthorised-commitment",
        "npc-e06-invented-evidence-consequence",
        "npc-n14-canon-hallucination",
    ):
        case = cases_by_id[case_id]
        metadata = metadata_from_mapping(
            metadata_by_id[case["deterministic_context"]["validation_metadata_ref"]]
        )
        result = validate_npc_surface_text(
            case["model_facing_input"]["injected_surface_candidate"], metadata
        )
        assert not result.passed
        assert case["expected_result"]["reason"] in result.reasons


def test_valid_required_proposition_passes() -> None:
    metadata = NPCFixtureValidationMetadata(
        required_content=(LexicalRule("PAYER_COMPANY_A", (r"company\s+a\s+paid",)),),
        canon_lexemes={"COMPANY_A": (r"company\s+a",)},
        authorised_canon_ids=frozenset({"COMPANY_A"}),
    )
    assert validate_npc_surface_text("Company A paid me.", metadata).passed


def test_missing_required_proposition_fails() -> None:
    metadata = NPCFixtureValidationMetadata(
        required_content=(
            LexicalRule("SAW_VEHICLE", (r"saw\s+(?:a\s+)?vehicle",)),
            LexicalRule("VEHICLE_LEFT_WAREHOUSE", (r"vehicle.*left.*warehouse",)),
        )
    )
    result = validate_npc_surface_text("I saw a vehicle.", metadata)
    assert not result.passed
    assert "MISSING_REQUIRED_CONTENT:VEHICLE_LEFT_WAREHOUSE" in result.reasons


def test_forbidden_proposition_disclosure_fails() -> None:
    metadata = NPCFixtureValidationMetadata(
        required_content=(LexicalRule("SAW_VEHICLE", (r"saw\s+(?:a\s+)?vehicle",)),),
        forbidden_content=(LexicalRule("DRIVER_MAYOR_AIDE", (r"mayor(?:'s|s)\s+aide",)),),
    )
    result = validate_npc_surface_text(
        "I saw a vehicle driven by the mayor's aide.", metadata
    )
    assert not result.passed
    assert "FORBIDDEN_CONTENT:DRIVER_MAYOR_AIDE" in result.reasons


def test_unauthorised_promise_or_commitment_fails() -> None:
    metadata = NPCFixtureValidationMetadata(
        required_content=(LexicalRule("COMPANY_CONTACT", (r"company\s+a\s+contacted",)),),
        unauthorised_commitments=(
            LexicalRule("LEDGER_PROMISE", (r"i(?:'ll|\s+will)\s+give\s+you\s+the\s+ledger",)),
        ),
    )
    result = validate_npc_surface_text(
        "Company A contacted me. I'll give you the ledger tonight.", metadata
    )
    assert not result.passed
    assert "UNAUTHORISED_COMMITMENT:LEDGER_PROMISE" in result.reasons


def test_invented_canon_fails() -> None:
    metadata = NPCFixtureValidationMetadata(
        canon_lexemes={"MINISTER_SON": (r"minister(?:'s|s)\s+son",)},
        authorised_canon_ids=frozenset(),
    )
    result = validate_npc_surface_text("The minister's son was there.", metadata)
    assert not result.passed
    assert "INVENTED_OR_UNAUTHORISED_CANON:MINISTER_SON" in result.reasons


def test_invented_state_or_evidence_consequence_fails() -> None:
    metadata = NPCFixtureValidationMetadata(
        state_or_evidence_consequences=(
            LexicalRule(
                "EVIDENCE_CREATION",
                (r"(?:made|created)\s+a\s+new\s+recording", r"added.*evidence\s+inventory"),
            ),
        )
    )
    result = validate_npc_surface_text(
        "I made a new recording and added it to your evidence inventory.", metadata
    )
    assert not result.passed
    assert any(reason.startswith("INVENTED_STATE_OR_EVIDENCE_CONSEQUENCE") for reason in result.reasons)


def test_gate_returns_reasons_only_and_has_no_state_mutation_channel() -> None:
    metadata = NPCFixtureValidationMetadata(
        required_content=(LexicalRule("PAYER", (r"company\s+a\s+paid",)),)
    )
    result = validate_npc_surface_text("I refuse to say.", metadata)
    assert result.reasons == ("MISSING_REQUIRED_CONTENT:PAYER",)
    assert not hasattr(result, "state_delta")
