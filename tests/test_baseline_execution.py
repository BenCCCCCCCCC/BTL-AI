from copy import deepcopy
import json

import pytest

from ai.prototype.adapters import AdapterOutcome, ScriptedAdapter
from ai.prototype.baseline import MANIFEST, SUPPORT, assemble_case, load_json, run_case


def records(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_three_components_receive_resolved_context_without_oracles(tmp_path):
    manifest, support = load_json(MANIFEST), load_json(SUPPORT)
    ids = ["dialogue-d18-valid", "headline-t10-single-claim", "npc-n01-valid-answer"]
    for case_id in ids:
        case = deepcopy(next(c for c in manifest["cases"] if c["case_id"] == case_id))
        case["model_facing_input"]["expected_result"] = "DO_NOT_SEND"
        case["model_facing_input"]["injected_candidate"] = "DO_NOT_SEND"
        assembled = assemble_case(manifest, case, support)
        encoded = json.dumps(assembled["model_input"])
        assert "DO_NOT_SEND" not in encoded
        assert "surface_candidate_example" not in encoded
        assert "runtime_catalogue_view_ref" not in encoded
        if case["component"] != "npc":
            assert set(assembled["catalogue"].targets) == set(assembled["model_input"]["runtime_catalogue_view"]["targets"])
            if case["component"] == "dialogue":
                assert set(assembled["model_input"]["tactic_descriptions"]) == {
                    "THREAT", "ACCUSATION", "INDIRECT_PROBE"}
        else:
            assert assembled["component"] == "npc_surface"
            assert assembled["model_input"]["response_plan"]["required_content"] == [
                {"relation": "payment_received", "payer_label": "Company A", "recipient": "speaker"}]
            assert "PAYER=COMPANY_A" not in encoded
            assert support["npc_fallbacks"]["NPC_N01"] not in encoded
        path = tmp_path / f"{case_id}.jsonl"
        result = run_case(manifest, case, support, run_id="offline", path=path)
        assert result["final_runtime_result"] == "PASS"
        assert records(path)[0]["execution_mode"] == "scripted"


def test_retry_retains_both_candidates_and_usage_and_redacts_trace_only(tmp_path):
    manifest, support = load_json(MANIFEST), load_json(SUPPORT)
    case = manifest["cases"][0]
    good = case["expected_result"]["candidate"]
    bad = {**good, "target_id": "sk-fake_secret_for_recording_123456"}
    adapter = ScriptedAdapter([
        AdapterOutcome.success(bad, input_tokens=10, output_tokens=5),
        AdapterOutcome.success(good, input_tokens=12, output_tokens=6),
    ])
    path = tmp_path / "retry.jsonl"
    result = run_case(manifest, case, support, run_id="retry", path=path, adapter=adapter)
    attempts = [r for r in records(path) if r["record_type"] == "attempt"]
    assert [r["attempt"] for r in attempts] == [1, 2]
    assert [r["runtime_result"] for r in attempts] == ["AI_SYSTEM_FAILURE", "PASS"]
    assert attempts[0]["output"]["target_id"] == "[REDACTED]"
    assert bad["target_id"].startswith("sk-")  # original candidate is unchanged
    assert result["input_tokens"] == 22 and result["output_tokens"] == 11
    assert result["final_output"] == good
    assert len(adapter.calls) == 2


@pytest.mark.parametrize("case_id,field,direction,count", [
    ("dialogue-d19-tactic-truncation", "tactics", "missing", 1),
    ("headline-f04-incomplete-claim-set", "claims", "missing", 1),
    ("headline-f05-invented-extra-claim", "claims", "extra", 1),
])
def test_fidelity_difference_is_recorded_without_retry(tmp_path, case_id, field, direction, count):
    manifest, support = load_json(MANIFEST), load_json(SUPPORT)
    case = next(c for c in manifest["cases"] if c["case_id"] == case_id)
    path = tmp_path / "fidelity.jsonl"
    result = run_case(manifest, case, support, run_id="fidelity", path=path)
    attempt = next(r for r in records(path) if r["record_type"] == "attempt")
    assert result["attempt_count"] == 1
    assert attempt["runtime_result"] == "PASS"
    assert attempt["semantic_fidelity"]["passed"] is False
    assert len(attempt["semantic_diff"][field][direction]) == count


def test_npc_failed_candidates_and_final_authored_fallback_are_distinct(tmp_path):
    manifest, support = load_json(MANIFEST), load_json(SUPPORT)
    case = next(c for c in manifest["cases"] if c["case_id"] == "npc-n12-missing-required")
    path = tmp_path / "npc.jsonl"
    result = run_case(manifest, case, support, run_id="npc", path=path)
    attempts = [r for r in records(path) if r["record_type"] == "attempt"]
    assert len(attempts) == 2
    assert all(r["runtime_reasons"] == ["MISSING_REQUIRED_CONTENT:VEHICLE_LEFT_WAREHOUSE"] for r in attempts)
    assert result["fallback_used"] and result["display_ready"]
    assert result["final_output"] == "I saw a vehicle. The vehicle left the warehouse."
