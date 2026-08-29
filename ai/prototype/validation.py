"""Deterministic Frozen-v0.1 candidate validation for Technical Prototype 01.

Runtime validation deliberately does not attempt to infer natural-language
completeness. Fixture ground-truth comparison is a separate baseline oracle.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
import json
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator


SCHEMA_DIRECTORY = Path(__file__).resolve().parents[1] / "schemas"


@dataclass(frozen=True)
class TargetDefinition:
    allowed_acts: frozenset[str] = field(default_factory=frozenset)
    allowed_values: frozenset[str] = field(default_factory=frozenset)
    value_required_acts: frozenset[str] = field(default_factory=frozenset)
    polarity_allowed_acts: frozenset[str] = field(default_factory=frozenset)
    polarity_required_acts: frozenset[str] = field(default_factory=frozenset)
    allowed_tactics: frozenset[str] = field(default_factory=frozenset)
    target_kind: str = "PROPOSITION"
    headline_eligible: bool = False
    headline_value_required: bool = False
    headline_polarity_required: bool = False


@dataclass(frozen=True)
class RuntimeCatalogue:
    targets: Mapping[str, TargetDefinition]
    visible_evidence_ids: frozenset[str] = field(default_factory=frozenset)
    visible_source_ids: frozenset[str] = field(default_factory=frozenset)
    pending_interaction_ids: frozenset[str] = field(default_factory=frozenset)
    pending_interaction_allowed_acts: Mapping[str, frozenset[str]] = field(
        default_factory=dict
    )


@dataclass(frozen=True)
class ValidationResult:
    can_proceed: bool
    failure_class: str
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True)
class BaselineEvaluation:
    exact_match: bool
    runtime_result: ValidationResult
    reasons: tuple[str, ...] = ()


def _system_failure(*reasons: str) -> ValidationResult:
    return ValidationResult(False, "AI_SYSTEM_FAILURE", tuple(reasons))


@lru_cache(maxsize=2)
def _schema_validator(filename: str) -> Draft202012Validator:
    with (SCHEMA_DIRECTORY / filename).open(encoding="utf-8") as schema_file:
        schema = json.load(schema_file)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _schema_errors(candidate: Any, filename: str) -> tuple[str, ...]:
    errors = _schema_validator(filename).iter_errors(candidate)
    return tuple(
        f"SCHEMA:{'/'.join(str(part) for part in error.absolute_path) or '$'}:{error.message}"
        for error in sorted(errors, key=lambda item: list(item.absolute_path))
    )


def validate_dialogue_candidate(
    candidate: Mapping[str, Any], catalogue: RuntimeCatalogue
) -> ValidationResult:
    """Validate a non-authoritative Dialogue candidate against current context."""

    schema_errors = _schema_errors(candidate, "dialogue_candidate.v0.1.schema.json")
    if schema_errors:
        return _system_failure(*schema_errors)

    status = candidate["status"]
    if status != "RESOLVED":
        return ValidationResult(False, "SEMANTIC_FAILURE", (status,))

    act = candidate["act"]
    if act in {"ACCEPT", "REFUSE"}:
        if len(catalogue.pending_interaction_ids) != 1:
            return _system_failure("PENDING_INTERACTION_NOT_UNIQUE")
        pending_interaction_id = next(iter(catalogue.pending_interaction_ids))
        allowed_acts = catalogue.pending_interaction_allowed_acts.get(pending_interaction_id)
        if allowed_acts is None or act not in allowed_acts:
            return _system_failure("PENDING_INTERACTION_NOT_VALID_FOR_ACT")
        forbidden_context_fields = {"target_id", "value_id", "polarity"}.intersection(candidate)
        if forbidden_context_fields:
            return _system_failure("MODEL_SELECTED_PENDING_INTERACTION_CONTEXT")
        return _validate_visible_evidence(candidate, catalogue)

    target_id = candidate.get("target_id")
    if target_id is None:
        return _system_failure("TARGET_REQUIRED")

    target = catalogue.targets.get(target_id)
    if target is None:
        return _system_failure("TARGET_UNAVAILABLE_OR_NONEXISTENT")
    if act not in target.allowed_acts:
        return _system_failure("ACT_NOT_ALLOWED_FOR_TARGET")
    if act == "REQUEST" and target.target_kind != "REQUEST":
        return _system_failure("REQUEST_REQUIRES_AUTHORED_REQUEST_TARGET")
    if act == "OFFER" and target.target_kind != "DEAL":
        return _system_failure("OFFER_REQUIRES_AUTHORED_BILATERAL_DEAL")

    value_id = candidate.get("value_id")
    if act in target.value_required_acts and value_id is None:
        return _system_failure("VALUE_REQUIRED")
    if value_id is not None and value_id not in target.allowed_values:
        return _system_failure("VALUE_NOT_ALLOWED_FOR_TARGET")

    polarity = candidate.get("polarity")
    if act in target.polarity_required_acts and polarity is None:
        return _system_failure("POLARITY_REQUIRED")
    if polarity is not None and act not in target.polarity_allowed_acts:
        return _system_failure("POLARITY_NOT_ALLOWED_FOR_ACT_TARGET")

    tactics = frozenset(candidate.get("tactics", ()))
    if not tactics.issubset(target.allowed_tactics):
        return _system_failure("TACTIC_NOT_ALLOWED_FOR_TARGET")

    return _validate_visible_evidence(candidate, catalogue)


def _validate_visible_evidence(
    candidate: Mapping[str, Any], catalogue: RuntimeCatalogue
) -> ValidationResult:
    evidence_ids = frozenset(candidate.get("evidence_ref_ids", ()))
    if not evidence_ids.issubset(catalogue.visible_evidence_ids):
        return _system_failure("EVIDENCE_UNAVAILABLE_OR_NONEXISTENT")
    return ValidationResult(True, "NONE")


def validate_headline_candidate(
    candidate: Mapping[str, Any], catalogue: RuntimeCatalogue
) -> ValidationResult:
    """Validate a Headline candidate; only resolved output is publication-ready."""

    schema_errors = _schema_errors(candidate, "headline_candidate.v0.1.schema.json")
    if schema_errors:
        return _system_failure(*schema_errors)

    status = candidate["status"]
    if status != "RESOLVED":
        return ValidationResult(False, "SEMANTIC_FAILURE", (status,))

    reasons: list[str] = []
    for index, claim in enumerate(candidate["claims"]):
        target = catalogue.targets.get(claim["target_id"])
        prefix = f"CLAIM_{index}"
        if target is None:
            reasons.append(f"{prefix}:TARGET_UNAVAILABLE_OR_NONEXISTENT")
            continue
        if not target.headline_eligible:
            reasons.append(f"{prefix}:TARGET_NOT_HEADLINE_ELIGIBLE")

        value_id = claim.get("value_id")
        if target.headline_value_required and value_id is None:
            reasons.append(f"{prefix}:VALUE_REQUIRED")
        if value_id is not None and value_id not in target.allowed_values:
            reasons.append(f"{prefix}:VALUE_NOT_ALLOWED_FOR_TARGET")

        polarity = claim.get("polarity")
        if target.headline_polarity_required and polarity is None:
            reasons.append(f"{prefix}:POLARITY_REQUIRED")
        if polarity is not None and not target.headline_polarity_required:
            reasons.append(f"{prefix}:POLARITY_NOT_ALLOWED_FOR_TARGET")

        source_ref_id = claim.get("source_ref_id")
        if source_ref_id is not None and source_ref_id not in catalogue.visible_source_ids:
            reasons.append(f"{prefix}:SOURCE_UNAVAILABLE_OR_NONEXISTENT")

    if reasons:
        return _system_failure(*reasons)
    return ValidationResult(True, "NONE")


def evaluate_dialogue_baseline(
    candidate: Mapping[str, Any],
    expected_candidate: Mapping[str, Any],
    catalogue: RuntimeCatalogue,
) -> BaselineEvaluation:
    runtime_result = validate_dialogue_candidate(candidate, catalogue)
    exact_match = _normalise_dialogue(candidate) == _normalise_dialogue(expected_candidate)
    reasons = () if exact_match else ("FIXTURE_SEMANTIC_MISMATCH",)
    return BaselineEvaluation(exact_match, runtime_result, reasons)


def evaluate_headline_baseline(
    candidate: Mapping[str, Any],
    expected_candidate: Mapping[str, Any],
    catalogue: RuntimeCatalogue,
) -> BaselineEvaluation:
    runtime_result = validate_headline_candidate(candidate, catalogue)
    exact_match = _normalise_headline(candidate) == _normalise_headline(expected_candidate)
    reasons = () if exact_match else ("FIXTURE_CLAIM_SET_MISMATCH",)
    return BaselineEvaluation(exact_match, runtime_result, reasons)


def _normalise_dialogue(candidate: Mapping[str, Any]) -> dict[str, Any]:
    normalised = dict(candidate)
    for field_name in ("tactics", "evidence_ref_ids"):
        if field_name in normalised:
            normalised[field_name] = sorted(normalised[field_name])
    return normalised


def _normalise_headline(candidate: Mapping[str, Any]) -> dict[str, Any]:
    normalised = dict(candidate)
    claims = normalised.get("claims")
    if claims is not None:
        normalised["claims"] = sorted(
            (dict(claim) for claim in claims),
            key=lambda claim: json.dumps(claim, sort_keys=True),
        )
    return normalised
