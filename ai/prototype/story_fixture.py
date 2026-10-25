"""Offline authored railyard branch walkthrough; not a Unity client or free-text parser."""

from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import dataclass
import json
from pathlib import Path

from .consequence_stub import (
    AuthoredConsequenceEvent, DeterministicallyResolvedGameplayResult,
    ExperimentalAuthoritativeTestState, ExperimentalVariableEffect, GlobalVariable,
    apply_authored_consequence_event,
)
from .validation import RuntimeCatalogue, TargetDefinition, validate_headline_candidate

STORY = Path(__file__).resolve().parents[2] / "tests/fixtures/railyard_story.experimental.v0.1.json"


@dataclass(frozen=True)
class PublicationSnapshot:
    headline: str
    claims_json: str
    evidence_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    evaluation_json: str
    ruleset_version: str


def evaluate_publication(story: dict, claims: list[dict], evidence: set[str]) -> list[dict]:
    """Only this fixture's positive ASSERTED atoms; no truth lookup or generic rule engine."""
    results = []
    for claim in claims:
        if claim["polarity"] != "AFFIRM" or claim["commitment_mode"] != "ASSERTED":
            raise ValueError("story fixture supports authored positive assertions only")
        rows = [r for r in story["relationships"] if r["evidence"] in evidence
                and r["target_id"] == claim["target_id"] and r["value_id"] == claim["value_id"]]
        supporting = [r["id"] for r in rows if r["dimension"] == "UNDERLYING" and r["effect"] == "SUPPORTS"]
        contradicting = [r["id"] for r in rows if r["dimension"] == "UNDERLYING" and r["effect"] == "CONTRADICTS"]
        underlying = "INSUFFICIENT" if bool(supporting) == bool(contradicting) else "SUPPORTED" if supporting else "CONTRADICTED"
        attribution_rows = [r["id"] for r in rows if r["dimension"] == "ATTRIBUTION"
                            and r.get("source_ref_id") == claim.get("source_ref_id")]
        attribution = "NOT_APPLICABLE" if "source_ref_id" not in claim else "SUPPORTED" if attribution_rows else "INSUFFICIENT"
        results.append({"underlying": underlying, "attribution": attribution,
                        "supporting_relationships": supporting, "contradicting_relationships": contradicting,
                        "attribution_relationships": attribution_rows})
    return results


class StorySession:
    def __init__(self, story: dict | None = None):
        self.story = deepcopy(story) if story is not None else json.loads(STORY.read_text(encoding="utf-8"))
        self.node = "interview"
        self.evidence: set[str] = set()
        self.sources: set[str] = set()
        self.state = ExperimentalAuthoritativeTestState(money=self.story["initial_money"])
        self.draft: str | None = None
        self.publication: PublicationSnapshot | None = None
        self.ending: str | None = None
        self.history: list[str] = []

    def choices(self) -> list[dict]:
        if self.ending:
            return []
        return [c for c in self.story["nodes"][self.node]["choices"]
                if set(c.get("requires_evidence", ())).issubset(self.evidence)]

    def _event(self, event_id: str) -> None:
        result_id = f"{self.story['event_id']}:{len(self.history)}:{event_id}"
        result = DeterministicallyResolvedGameplayResult(result_id)
        event = AuthoredConsequenceEvent(event_id, result_id, tuple(
            ExperimentalVariableEffect(GlobalVariable(variable), delta)
            for variable, delta in self.story["events"][event_id].items()))
        self.state = apply_authored_consequence_event(self.state, result, event)

    def choose(self, choice_id: str) -> str:
        choice = next((c for c in self.choices() if c["id"] == choice_id), None)
        if choice is None:
            raise ValueError(f"choice {choice_id!r} is unavailable at {self.node}")
        self.history.append(choice_id)
        self.evidence.update(choice.get("grant_evidence", ()))
        self.sources.update(choice.get("grant_sources", ()))
        if "event" in choice:
            self._event(choice["event"])
        if "headline_id" in choice:
            self.draft = choice["headline_id"]
        if choice.get("publish"):
            self._publish()
        elif "ending" in choice:
            self.ending = choice["ending"]
            self._event(self.ending)
        else:
            self.node = choice["next"]
        return self.story["endings"][self.ending] if self.ending else choice.get("response", "")

    def _publish(self) -> None:
        headline = self.story["headlines"][self.draft]
        catalogue = RuntimeCatalogue(targets={
            "PROP_FIRE_FIRST": TargetDefinition(allowed_values=frozenset({"MILITIA", "SECURITY_FORCES"}), headline_eligible=True, headline_value_required=True, headline_polarity_required=True),
            "PROP_FUNDED_OPERATION": TargetDefinition(allowed_values=frozenset({"COMPANY_A", "MAYOR_OFFICE"}), headline_eligible=True, headline_value_required=True, headline_polarity_required=True),
        }, visible_source_ids=frozenset(self.sources))
        candidate = {"status": "RESOLVED", "claims": headline["claims"]}
        validation = validate_headline_candidate(candidate, catalogue)
        if not validation.can_proceed:
            raise ValueError("authored headline failed runtime validation")
        evaluations = evaluate_publication(self.story, headline["claims"], self.evidence)
        self.publication = PublicationSnapshot(headline["text"], json.dumps(headline["claims"], sort_keys=True),
            tuple(sorted(self.evidence)), tuple(sorted(self.sources)), json.dumps(evaluations, sort_keys=True), self.story["version"])
        if not evaluations:
            self.ending = "NO_CLAIM"
        elif all(e["underlying"] == "SUPPORTED" and e["attribution"] in {"SUPPORTED", "NOT_APPLICABLE"} for e in evaluations):
            self.ending = "SUPPORTED_REPORT"
        elif all(e["attribution"] == "SUPPORTED" for e in evaluations):
            self.ending = "CONTESTED_ATTRIBUTION"
        else:
            self.ending = "UNSUPPORTED_REPORT"
        # Explicit authored result-to-event choice, not an automatic label-to-delta rule.
        self._event(self.ending)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--choices", help="Comma-separated choice IDs for an offline walkthrough; omit for interactive choices.")
    args = parser.parse_args(argv)
    session = StorySession()
    print(session.story["title"] + " — " + session.story["status"])
    print(session.story["premise"])
    if args.choices:
        for choice in args.choices.split(","):
            print(session.choose(choice))
    else:
        while not session.ending:
            print("\n" + session.story["nodes"][session.node]["text"])
            if session.node == "confirm":
                print("当前标题：" + session.story["headlines"][session.draft]["text"])
            for choice in session.choices():
                print(f"  {choice['id']}: {choice['label']}")
            try:
                print(session.choose(input("> ").strip()))
            except ValueError as error:
                print(error)
    print(json.dumps({"ending": session.ending, "evidence": sorted(session.evidence),
                      "variables": session.state.as_dict()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
