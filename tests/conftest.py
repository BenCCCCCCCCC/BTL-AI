from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai.prototype.validation import RuntimeCatalogue, TargetDefinition


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "ai" / "eval" / "p0_baseline_manifest.v0.1.1.json"


@pytest.fixture(scope="session")
def manifest() -> dict:
    with MANIFEST_PATH.open(encoding="utf-8") as manifest_file:
        return json.load(manifest_file)


@pytest.fixture(scope="session")
def cases_by_id(manifest: dict) -> dict[str, dict]:
    return {case["case_id"]: case for case in manifest["cases"]}


@pytest.fixture
def dialogue_catalogue() -> RuntimeCatalogue:
    all_tactics = frozenset({"THREAT", "ACCUSATION", "INDIRECT_PROBE"})
    return RuntimeCatalogue(
        targets={
            "PAYMENT_PAYER": TargetDefinition(
                allowed_acts=frozenset({"QUESTION", "ASSERTION"}),
                allowed_values=frozenset({"MAYOR_OFFICE", "COMPANY_A", "MILITIA"}),
                value_required_acts=frozenset({"ASSERTION"}),
                polarity_allowed_acts=frozenset({"ASSERTION"}),
                polarity_required_acts=frozenset({"ASSERTION"}),
                allowed_tactics=all_tactics,
                headline_eligible=False,
            ),
            "HAND_OVER_LEDGER": TargetDefinition(
                allowed_acts=frozenset({"REQUEST"}),
                allowed_tactics=frozenset({"THREAT"}),
                target_kind="REQUEST",
            ),
            "REVEAL_PAYMENT_PAYER": TargetDefinition(
                allowed_acts=frozenset({"REQUEST"}),
                allowed_tactics=all_tactics,
                target_kind="REQUEST",
            ),
            "DEAL_LEDGER_FOR_500": TargetDefinition(
                allowed_acts=frozenset({"OFFER"}),
                target_kind="DEAL",
            ),
        },
        visible_evidence_ids=frozenset({"PHOTO_01", "AUDIO_01"}),
        pending_interaction_ids=frozenset({"PENDING_01"}),
        pending_interaction_allowed_acts={
            "PENDING_01": frozenset({"ACCEPT", "REFUSE"})
        },
    )


@pytest.fixture
def headline_catalogue() -> RuntimeCatalogue:
    values = {
        "FIRE_FIRST": {"SECURITY_FORCES", "MILITIA"},
        "ORDERED_OPERATION": {"MAYOR_OFFICE", "MILITIA_COMMAND"},
        "FUNDED_OPERATION": {"COMPANY_A", "MAYOR_OFFICE"},
        "CIVILIAN_DEATH_CAUSE": {"SECURITY_FORCES", "MILITIA"},
    }
    return RuntimeCatalogue(
        targets={
            target_id: TargetDefinition(
                allowed_values=frozenset(allowed_values),
                headline_eligible=True,
                headline_value_required=True,
                headline_polarity_required=True,
            )
            for target_id, allowed_values in values.items()
        }
        | {
            "DIALOGUE_ONLY": TargetDefinition(
                allowed_acts=frozenset({"REQUEST"}),
                target_kind="REQUEST",
                headline_eligible=False,
            )
        },
        visible_source_ids=frozenset({"SRC_WITNESS_A", "SRC_POLICE", "SRC_MAYOR"}),
    )
