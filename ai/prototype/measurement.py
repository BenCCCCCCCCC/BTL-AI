"""Structured JSONL-compatible measurement records for Batch 2A."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class RunMeasurement:
    run_id: str
    case_id: str
    component: str
    manifest_version: str
    contract_version: str
    adapter_identifier: str
    model_identifier: str | None
    prompt_version: str | None
    schema_version: str | None
    attempt_count: int
    first_pass_runtime_result: str
    final_runtime_result: str
    semantic_fidelity_result: str | None
    retry_used: bool
    fallback_used: bool
    fallback_type: str | None
    publication_ready: bool | None
    display_ready: bool | None
    input_tokens: int | None
    output_tokens: int | None
    model_call_latency_ms: float | None
    end_to_end_latency_ms: float
    estimated_cost: float | None
    hard_safety_gate_breach: bool
    reason_codes: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["reason_codes"] = list(self.reason_codes)
        return data


def append_jsonl(path: Path, record: RunMeasurement) -> None:
    with path.open("a", encoding="utf-8") as output_file:
        output_file.write(json.dumps(record.as_dict(), sort_keys=True) + "\n")
