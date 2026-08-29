from __future__ import annotations

import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
BASELINE_SHA = "aa87d39959e6a4b2f6cad31883528cb8e8d1cc42"
REQUIRED_MARKERS = {"Experimental", "Validation-only", "Non-canonical"}


def test_manifest_is_versioned_and_traces_every_case_to_a_fixture(manifest: dict) -> None:
    assert manifest["manifest_version"] == "0.1"
    assert manifest["contract_version"] == "Frozen v0.1"
    assert manifest["source_repository_baseline_sha"] == BASELINE_SHA
    assert set(manifest["scope_marker"]) == REQUIRED_MARKERS

    required_case_fields = {
        "case_id",
        "component",
        "source_fixture",
        "source_case_id",
        "execution_path",
        "deterministic_context",
        "model_facing_input",
        "expected_result",
        "marker",
    }
    case_ids = [case["case_id"] for case in manifest["cases"]]
    assert len(case_ids) == len(set(case_ids))

    for case in manifest["cases"]:
        assert required_case_fields.issubset(case)
        assert case["execution_path"] in {"real_model", "fault_injection"}
        assert set(case["marker"]) == REQUIRED_MARKERS
        fixture_path = ROOT / case["source_fixture"]
        fixture_text = fixture_path.read_text(encoding="utf-8")
        assert re.search(rf"\b{re.escape(case['source_case_id'])}\b", fixture_text)


def test_manifest_contains_the_required_batch_one_faults(manifest: dict) -> None:
    source_cases = {
        (case["component"], case["source_case_id"])
        for case in manifest["cases"]
        if case["execution_path"] == "fault_injection"
    }
    assert {
        ("dialogue", "D19"),
        ("dialogue", "D20"),
        ("dialogue", "D30"),
        ("dialogue", "D31"),
        ("headline", "F02"),
        ("headline", "F03"),
        ("headline", "F04"),
        ("headline", "F05"),
        ("npc", "N12"),
        ("npc", "N13"),
        ("npc", "N11"),
        ("npc", "E06"),
        ("npc", "N14"),
    }.issubset(source_cases)


def test_npc_cases_reference_machine_readable_fixture_metadata(manifest: dict) -> None:
    metadata = manifest["npc_output_validation_metadata"]
    for case in manifest["cases"]:
        if case["component"] != "npc":
            continue
        metadata_ref = case["deterministic_context"]["validation_metadata_ref"]
        assert metadata_ref in metadata


def test_frozen_structural_schemas_are_valid_and_have_only_contract_fields() -> None:
    schema_expectations = {
        "dialogue_candidate.v0.1.schema.json": {
            "status",
            "reason",
            "act",
            "target_id",
            "value_id",
            "polarity",
            "tactics",
            "evidence_ref_ids",
        },
        "headline_candidate.v0.1.schema.json": {"status", "reason", "claims"},
    }
    for filename, expected_fields in schema_expectations.items():
        path = ROOT / "ai" / "schemas" / filename
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        assert set(schema["properties"]) == expected_fields
        assert schema["additionalProperties"] is False

    headline = json.loads(
        (ROOT / "ai" / "schemas" / "headline_candidate.v0.1.schema.json").read_text(
            encoding="utf-8"
        )
    )
    assert set(headline["$defs"]["claim_atom"]["properties"]) == {
        "target_id",
        "value_id",
        "polarity",
        "commitment_mode",
        "source_ref_id",
    }
