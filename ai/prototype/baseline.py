"""Thin manifest entry point. Scripted execution is the default; no live calls on import.

Attempt evaluation is an offline observer of adapter outputs. It never changes
the candidate or the runner's retry decision. JSONL retains attempts before a
later request can fail, followed by the existing runner summary per case.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Mapping
from uuid import uuid4

from .adapters import AdapterOutcome, ModelAdapter, ScriptedAdapter
from .npc_output_gate import metadata_from_mapping, validate_npc_surface_text
from .runner import AuthoredNPCFallback, BaselineRunner
from .validation import (
    RuntimeCatalogue, TargetDefinition, evaluate_dialogue_baseline,
    evaluate_headline_baseline, validate_dialogue_candidate, validate_headline_candidate,
)

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "ai/eval/p0_baseline_manifest.v0.1.1.json"
SUPPORT = ROOT / "ai/eval/baseline_execution.experimental.v0.3.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def catalogue_from_view(view: Mapping[str, Any]) -> RuntimeCatalogue:
    targets = {}
    for target_id, data in view["targets"].items():
        targets[target_id] = TargetDefinition(
            allowed_acts=frozenset(data.get("allowed_acts", ())),
            allowed_values=frozenset(data.get("allowed_value_ids", ())),
            value_required_acts=frozenset(data.get("value_required_acts", ())),
            polarity_allowed_acts=frozenset(data.get("polarity_allowed_acts", ())),
            polarity_required_acts=frozenset(data.get("polarity_required_acts", ())),
            allowed_tactics=frozenset(data.get("allowed_tactics", ())),
            target_kind=data.get("target_kind", "PROPOSITION"),
            headline_eligible=data.get("headline_eligible", False),
            headline_value_required=data.get("value_required", False),
            headline_polarity_required=data.get("polarity_required", False),
        )
    return RuntimeCatalogue(
        targets=targets,
        visible_evidence_ids=frozenset(view.get("visible_evidence_ids", ())),
        visible_source_ids=frozenset(view.get("visible_source_ids", ())),
        pending_interaction_ids=frozenset(view.get("pending_interaction_ids", ())),
        pending_interaction_allowed_acts={
            key: frozenset(value)
            for key, value in view.get("pending_interaction_allowed_acts", {}).items()
        },
    )


def assemble_case(manifest: dict, case: dict, support: dict) -> dict:
    """Project allowed input fields; evaluation answers stay outside model_input."""
    context = case["deterministic_context"]
    component = case["component"]
    source = case
    if "fixture_oracle_ref" in context:
        source = next(c for c in manifest["cases"] if c["case_id"] == context["fixture_oracle_ref"])
    if component == "npc":
        # Do not disclose forbidden hidden facts or regex/oracle metadata.
        model_input = {
            "response_plan": {
                "response_mode": context["response_mode"],
                "required_content": [deepcopy(support["npc_content_meanings"][item])
                                     for item in context.get("required_content", [])],
                "authorised_commitments": deepcopy(context.get("authorised_commitments", [])),
            },
            "speaker": {"role": "the NPC receiving the player's question", "perspective": "first person"},
            "voice_constraints": "Concise natural English dialogue; verbalise the authorised facts, never their field names or IDs.",
        }
        metadata_ref = context["validation_metadata_ref"]
        return {
            "component": "npc_surface", "model_input": model_input,
            "metadata": metadata_from_mapping(manifest["npc_output_validation_metadata"][metadata_ref]),
            "fallback": AuthoredNPCFallback(context["response_mode"], support["npc_fallbacks"][metadata_ref]),
        }
    ref = context["runtime_catalogue_view_ref"]
    view = deepcopy(manifest["runtime_catalogue_views"][ref])
    text_field = "player_text" if component == "dialogue" else "headline_text"
    model_input = {"runtime_catalogue_view": view}
    if text_field in source["model_facing_input"]:
        model_input[text_field] = source["model_facing_input"][text_field]
    # Explicitly allow only authored language context. No oracle/fault candidate.
    extra = support["catalogue_context"].get(ref, {})
    for key in ("target_descriptions", "tactic_descriptions", "visible_evidence", "visible_sources"):
        if key in extra:
            model_input[key] = deepcopy(extra[key])
    return {
        "component": component, "model_input": model_input,
        "catalogue": catalogue_from_view(view),
        "expected_candidate": source["expected_result"].get("candidate"),
    }


def semantic_diff(candidate: dict, expected: dict, component: str) -> dict:
    """Review details only, including multiplicity; not a runtime retry signal."""
    fields = ("claims",) if component == "headline" else ("tactics", "evidence_ref_ids")
    difference = {}
    for field in fields:
        encode = lambda value: json.dumps(value, sort_keys=True, ensure_ascii=False)
        actual = Counter(map(encode, candidate.get(field) or []))
        wanted = Counter(map(encode, expected.get(field) or []))
        difference[field] = {
            "missing": [json.loads(value) for value in (wanted - actual).elements()],
            "extra": [json.loads(value) for value in (actual - wanted).elements()],
        }
    difference["field_mismatches"] = {
        field: {"expected": expected.get(field), "actual": candidate.get(field)}
        for field in (set(candidate) | set(expected)) - set(fields)
        if candidate.get(field) != expected.get(field)
    }
    return difference


def describe_attempt(outcome: AdapterOutcome, assembled: dict) -> dict:
    details = asdict(outcome)
    component = assembled["component"]
    candidate = outcome.output
    fidelity = None
    differences = None
    if outcome.system_failure_reason:
        runtime, reasons = "AI_SYSTEM_FAILURE", [outcome.system_failure_reason]
    elif component == "npc_surface":
        gate = validate_npc_surface_text(candidate, assembled["metadata"]) if isinstance(candidate, str) else None
        runtime = "PASS" if gate and gate.passed else "AI_SYSTEM_FAILURE"
        reasons = list(gate.reasons) if gate else ["NPC_SURFACE_TEXT_REQUIRED"]
    else:
        validator = validate_dialogue_candidate if component == "dialogue" else validate_headline_candidate
        result = validator(candidate, assembled["catalogue"])
        runtime = "PASS" if result.can_proceed else result.failure_class
        reasons = list(result.reasons)
        expected = assembled["expected_candidate"]
        # Structurally bad candidates retain their raw output and runtime reason.
        if result.failure_class != "AI_SYSTEM_FAILURE" and expected is not None:
            evaluator = evaluate_dialogue_baseline if component == "dialogue" else evaluate_headline_baseline
            fidelity = asdict(evaluator(candidate, expected, assembled["catalogue"]).semantic_fidelity)
            differences = semantic_diff(candidate, expected, component)
    details.update(runtime_result=runtime, runtime_reasons=reasons,
                   semantic_fidelity=fidelity, semantic_diff=differences)
    return details


def sanitise(value: Any) -> Any:
    """Remove common secret strings from review artifacts, not from evaluation."""
    if isinstance(value, str):
        return re.sub(r"(?i)\b(?:sk-[a-z0-9_-]{8,}|gsk_[a-z0-9_-]{8,}|bearer\s+[^\s\"']+)", "[REDACTED]", value)
    if isinstance(value, dict):
        return {key: "[REDACTED]" if key.lower() in {"api_key", "authorization", "password", "secret"}
                else sanitise(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [sanitise(item) for item in value]
    return value


def append_record(path: Path, record: dict) -> None:
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(sanitise(record), ensure_ascii=False, sort_keys=True) + "\n")


class RecordingAdapter:
    def __init__(self, inner: ModelAdapter, assembled: dict, path: Path, run_id: str, case_id: str):
        self.inner, self.assembled, self.path = inner, assembled, path
        self.run_id, self.case_id, self.attempt = run_id, case_id, 0
        for field in ("adapter_identifier", "model_identifier", "prompt_version", "schema_version"):
            setattr(self, field, getattr(inner, field))

    def invoke(self, component: str, model_input: Mapping[str, Any]) -> AdapterOutcome:
        outcome = self.inner.invoke(component, model_input)
        self.attempt += 1
        append_record(self.path, {
            "record_type": "attempt", "run_id": self.run_id, "case_id": self.case_id,
            "attempt": self.attempt, "component": component,
            **describe_attempt(outcome, self.assembled),
        })
        return outcome


def scripted_adapter(case: dict, assembled: dict) -> ScriptedAdapter:
    source = case["model_facing_input"]
    if case["execution_path"] == "fault_injection":
        candidate = source.get("injected_candidate", source.get("injected_surface_candidate"))
    elif assembled["component"] == "npc_surface":
        candidate = assembled["fallback"].surface_text
    else:
        candidate = assembled["expected_candidate"]
    # Deliberately repeats invalid candidates to exercise exhaustion, offline only.
    return ScriptedAdapter([AdapterOutcome.success(deepcopy(candidate)) for _ in range(2)])


def run_case(manifest: dict, case: dict, support: dict, *, run_id: str, path: Path,
             adapter: ModelAdapter | None = None) -> dict:
    assembled = assemble_case(manifest, case, support)
    if adapter is not None and case["execution_path"] != "real_model":
        raise ValueError("fault injection is offline only")
    inner = adapter if adapter is not None else scripted_adapter(case, assembled)
    recording = RecordingAdapter(inner, assembled, path, run_id, case["case_id"])
    append_record(path, {"record_type": "case_input", "run_id": run_id,
                        "case_id": case["case_id"], "component": assembled["component"],
                        "execution_path": case["execution_path"],
                        "execution_mode": "scripted" if adapter is None else "live",
                        "model_input": assembled["model_input"]})
    runner = BaselineRunner(recording, manifest_version=manifest["manifest_version"],
                            contract_version=manifest["contract_version"])
    common = dict(run_id=run_id, case_id=case["case_id"], model_input=assembled["model_input"])
    if assembled["component"] == "npc_surface":
        result = runner.run_npc_surface(**common, response_mode=assembled["fallback"].response_mode,
            metadata=assembled["metadata"], authored_fallback=assembled["fallback"],
            expected_safety_disposition="ACCEPT" if case["expected_result"]["gate"] == "PASS" else "REJECT")
    else:
        run = runner.run_dialogue if assembled["component"] == "dialogue" else runner.run_headline
        result = run(**common, catalogue=assembled["catalogue"],
            expected_candidate=assembled["expected_candidate"],
            expected_safety_disposition="REJECT" if case["expected_result"]["runtime_contract"] == "REJECT" else "ACCEPT")
    summary = result.measurement.as_dict()
    summary.update(record_type="case_summary", final_output=result.validated_output,
                   draft_preserved=result.draft_preserved,
                   execution_mode="scripted" if adapter is None else "live")
    append_record(path, summary)
    return summary


def fingerprint() -> dict:
    files = [MANIFEST, SUPPORT, *sorted((ROOT / "ai/prototype").glob("*.py")),
             *sorted((ROOT / "ai/prompts").glob("*.txt")), *sorted((ROOT / "ai/schemas").glob("*.json"))]
    hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    return {"git_head": head, "python": sys.version, "sha256": hashes}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--adapter", choices=("scripted", "groq"), default="scripted")
    parser.add_argument("--authorization", type=Path, help="Explicit Groq batch sheet; must already be authorised.")
    parser.add_argument("--cases", choices=("real_model", "fault_injection", "all"), default="real_model")
    parser.add_argument("--case-id", action="append", help="Select specific existing cases; repeat as needed.")
    parser.add_argument("--output", type=Path, help="New JSONL file; existing results are never overwritten.")
    args = parser.parse_args(argv)
    if args.authorization is not None and args.adapter != "groq":
        parser.error("--authorization is only used with --adapter groq")
    manifest, support = load_json(MANIFEST), load_json(SUPPORT)
    selected = [c for c in manifest["cases"] if args.cases == "all" or c["execution_path"] == args.cases]
    sheet = None
    if args.adapter == "groq":
        from .groq_adapter import AUTHORIZATION, prepare_execution
        sheet = load_json(args.authorization or AUTHORIZATION)
        if args.case_id is None:
            selected = [c for c in selected if c["case_id"] in sheet["case_ids"]]
    if args.case_id:
        selected = [c for c in selected if c["case_id"] in args.case_id]
        if {c["case_id"] for c in selected} != set(args.case_id):
            parser.error("unknown case or case outside --cases selection")
    adapter = None
    if args.adapter == "groq":
        # Closed authorization is checked before credentials, directory writes or requests.
        try:
            adapter = prepare_execution(sheet, [c["case_id"] for c in selected])
        except (ValueError, RuntimeError) as error:
            parser.exit(2, f"{error}\n")
        run_id = sheet["batch_id"]
        path = ROOT / sheet["output_path"]
        if args.output is not None and args.output.resolve() != path.resolve():
            parser.error("live output is fixed by the authorised batch")
    else:
        run_id = "scripted-" + uuid4().hex[:12]
        path = args.output or ROOT / "ai/eval/output" / (run_id + ".jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8"):
            pass
    except FileExistsError:
        parser.exit(2, "Output already exists; preserve results and review missing cases before another live batch.\n")
    append_record(path, {"record_type": "run", "run_id": run_id, "case_ids": [c["case_id"] for c in selected],
                        "execution_mode": args.adapter, "reproducibility": fingerprint(),
                        "authorised_batch": sheet})
    summaries = [run_case(manifest, case, support, run_id=run_id, path=path, adapter=adapter) for case in selected]
    print(json.dumps({"run_id": run_id, "cases": len(summaries), "output": str(path),
                      "execution_mode": args.adapter, "actual_model_requests": 0 if adapter is None else adapter.calls}, ensure_ascii=False))
    return 1 if any(s["hard_safety_gate_breach"] for s in summaries) else 0


if __name__ == "__main__":
    raise SystemExit(main())
