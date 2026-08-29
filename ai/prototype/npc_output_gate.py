"""Experimental fixture-scoped lexical NPC Output Validation Gate.

This is deliberately not a production natural-language safety solution. It
uses authored regular-expression metadata and never mutates gameplay state.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any, Mapping


@dataclass(frozen=True)
class LexicalRule:
    rule_id: str
    patterns: tuple[str, ...]

    def matches(self, text: str) -> bool:
        return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in self.patterns)


@dataclass(frozen=True)
class NPCFixtureValidationMetadata:
    required_content: tuple[LexicalRule, ...] = ()
    forbidden_content: tuple[LexicalRule, ...] = ()
    canon_lexemes: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    authorised_canon_ids: frozenset[str] = field(default_factory=frozenset)
    unauthorised_commitments: tuple[LexicalRule, ...] = ()
    state_or_evidence_consequences: tuple[LexicalRule, ...] = ()


@dataclass(frozen=True)
class NPCGateResult:
    passed: bool
    reasons: tuple[str, ...] = ()


def metadata_from_mapping(data: Mapping[str, Any]) -> NPCFixtureValidationMetadata:
    """Load authored fixture metadata from the versioned baseline manifest."""

    def rules(field_name: str) -> tuple[LexicalRule, ...]:
        return tuple(
            LexicalRule(item["rule_id"], tuple(item["patterns"]))
            for item in data.get(field_name, ())
        )

    return NPCFixtureValidationMetadata(
        required_content=rules("required_content"),
        forbidden_content=rules("forbidden_content"),
        canon_lexemes={
            canon_id: tuple(patterns)
            for canon_id, patterns in data.get("canon_lexemes", {}).items()
        },
        authorised_canon_ids=frozenset(data.get("authorised_canon_ids", ())),
        unauthorised_commitments=rules("unauthorised_commitments"),
        state_or_evidence_consequences=rules("state_or_evidence_consequences"),
    )


def validate_npc_surface_text(
    surface_text: str, metadata: NPCFixtureValidationMetadata
) -> NPCGateResult:
    """Return PASS/FAIL reasons without producing or applying any state change."""

    reasons: list[str] = []
    for rule in metadata.required_content:
        if not rule.matches(surface_text):
            reasons.append(f"MISSING_REQUIRED_CONTENT:{rule.rule_id}")
    for rule in metadata.forbidden_content:
        if rule.matches(surface_text):
            reasons.append(f"FORBIDDEN_CONTENT:{rule.rule_id}")

    for canon_id, patterns in metadata.canon_lexemes.items():
        if canon_id in metadata.authorised_canon_ids:
            continue
        if any(re.search(pattern, surface_text, flags=re.IGNORECASE) for pattern in patterns):
            reasons.append(f"INVENTED_OR_UNAUTHORISED_CANON:{canon_id}")

    for rule in metadata.unauthorised_commitments:
        if rule.matches(surface_text):
            reasons.append(f"UNAUTHORISED_COMMITMENT:{rule.rule_id}")
    for rule in metadata.state_or_evidence_consequences:
        if rule.matches(surface_text):
            reasons.append(f"INVENTED_STATE_OR_EVIDENCE_CONSEQUENCE:{rule.rule_id}")

    return NPCGateResult(not reasons, tuple(reasons))
