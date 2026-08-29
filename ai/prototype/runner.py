"""Minimal provider-independent Batch 2A baseline policy runner.

The runner orchestrates non-authoritative output through existing validators
and evaluation. It has no gameplay-state or consequence authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Any, Callable, Mapping

from .adapters import AdapterOutcome, ModelAdapter
from .measurement import RunMeasurement, append_jsonl
from .npc_output_gate import NPCFixtureValidationMetadata, validate_npc_surface_text
from .validation import (
    RuntimeCatalogue,
    SemanticFidelityResult,
    ValidationResult,
    evaluate_dialogue_baseline,
    evaluate_headline_baseline,
    validate_dialogue_candidate,
    validate_headline_candidate,
)


@dataclass(frozen=True)
class AuthoredNPCFallback:
    response_mode: str
    surface_text: str
    fallback_type: str = "AUTHORED_TEMPLATE"


@dataclass(frozen=True)
class BaselineRunResult:
    validated_output: Any | None
    attempt_count: int
    first_pass_runtime_result: str
    final_runtime_result: str
    semantic_fidelity: SemanticFidelityResult | None
    retry_used: bool
    fallback_used: bool
    fallback_type: str | None
    publication_ready: bool | None
    display_ready: bool | None
    draft_preserved: bool | None
    safe_non_consequential: bool
    hard_safety_gate_breach: bool
    reasons: tuple[str, ...]
    measurement: RunMeasurement


@dataclass(frozen=True)
class _Attempt:
    outcome: AdapterOutcome
    validation: ValidationResult


class BaselineRunner:
    def __init__(
        self,
        adapter: ModelAdapter,
        *,
        manifest_version: str,
        contract_version: str,
    ) -> None:
        self.adapter = adapter
        self.manifest_version = manifest_version
        self.contract_version = contract_version

    def run_dialogue(
        self,
        *,
        run_id: str,
        case_id: str,
        model_input: Mapping[str, Any],
        catalogue: RuntimeCatalogue,
        expected_candidate: Mapping[str, Any] | None = None,
        measurement_path: Path | None = None,
    ) -> BaselineRunResult:
        return self._run_parser(
            run_id=run_id,
            case_id=case_id,
            component="dialogue",
            model_input=model_input,
            validate=lambda candidate: validate_dialogue_candidate(candidate, catalogue),
            evaluate=(
                None
                if expected_candidate is None
                else lambda candidate: evaluate_dialogue_baseline(
                    candidate, expected_candidate, catalogue
                ).semantic_fidelity
            ),
            publication_component=False,
            measurement_path=measurement_path,
        )

    def run_headline(
        self,
        *,
        run_id: str,
        case_id: str,
        model_input: Mapping[str, Any],
        catalogue: RuntimeCatalogue,
        expected_candidate: Mapping[str, Any] | None = None,
        measurement_path: Path | None = None,
    ) -> BaselineRunResult:
        return self._run_parser(
            run_id=run_id,
            case_id=case_id,
            component="headline",
            model_input=model_input,
            validate=lambda candidate: validate_headline_candidate(candidate, catalogue),
            evaluate=(
                None
                if expected_candidate is None
                else lambda candidate: evaluate_headline_baseline(
                    candidate, expected_candidate, catalogue
                ).semantic_fidelity
            ),
            publication_component=True,
            measurement_path=measurement_path,
        )

    def run_npc_surface(
        self,
        *,
        run_id: str,
        case_id: str,
        model_input: Mapping[str, Any],
        response_mode: str,
        metadata: NPCFixtureValidationMetadata,
        authored_fallback: AuthoredNPCFallback,
        measurement_path: Path | None = None,
    ) -> BaselineRunResult:
        started = perf_counter()
        attempts: list[_Attempt] = []
        for _ in range(2):
            attempt = self._invoke(
                "npc_surface",
                model_input,
                lambda output: self._validate_npc_output(output, metadata),
            )
            attempts.append(attempt)
            if attempt.validation.can_proceed:
                break

        final_validation = attempts[-1].validation
        validated_output = (
            attempts[-1].outcome.output if final_validation.can_proceed else None
        )
        fallback_used = False
        fallback_type: str | None = None
        fallback_reasons: tuple[str, ...] = ()

        if not final_validation.can_proceed:
            fallback_used = True
            fallback_type = authored_fallback.fallback_type
            if authored_fallback.response_mode != response_mode:
                final_validation = ValidationResult(
                    False,
                    "AI_SYSTEM_FAILURE",
                    ("FALLBACK_RESPONSE_MODE_MISMATCH",),
                )
            else:
                final_validation = self._validate_npc_output(
                    authored_fallback.surface_text, metadata
                )
                if final_validation.can_proceed:
                    validated_output = authored_fallback.surface_text
            fallback_reasons = final_validation.reasons

        display_ready = final_validation.can_proceed
        hard_safety_gate_breach = display_ready and not final_validation.can_proceed
        reasons = _unique_reasons(attempts, fallback_reasons)
        measurement = self._measurement(
            started=started,
            run_id=run_id,
            case_id=case_id,
            component="npc_surface",
            attempts=attempts,
            final_validation=final_validation,
            semantic_fidelity=None,
            fallback_used=fallback_used,
            fallback_type=fallback_type,
            publication_ready=None,
            display_ready=display_ready,
            hard_safety_gate_breach=hard_safety_gate_breach,
            reasons=reasons,
        )
        if measurement_path is not None:
            append_jsonl(measurement_path, measurement)
        return BaselineRunResult(
            validated_output=validated_output,
            attempt_count=len(attempts),
            first_pass_runtime_result=_runtime_label(attempts[0].validation),
            final_runtime_result=_runtime_label(final_validation),
            semantic_fidelity=None,
            retry_used=len(attempts) == 2,
            fallback_used=fallback_used,
            fallback_type=fallback_type,
            publication_ready=None,
            display_ready=display_ready,
            draft_preserved=None,
            safe_non_consequential=not display_ready,
            hard_safety_gate_breach=hard_safety_gate_breach,
            reasons=reasons,
            measurement=measurement,
        )

    def _run_parser(
        self,
        *,
        run_id: str,
        case_id: str,
        component: str,
        model_input: Mapping[str, Any],
        validate: Callable[[Any], ValidationResult],
        evaluate: Callable[[Mapping[str, Any]], SemanticFidelityResult] | None,
        publication_component: bool,
        measurement_path: Path | None,
    ) -> BaselineRunResult:
        started = perf_counter()
        attempts: list[_Attempt] = []
        for _ in range(2):
            attempt = self._invoke(component, model_input, validate)
            attempts.append(attempt)
            if attempt.validation.can_proceed:
                break
            if attempt.validation.failure_class == "SEMANTIC_FAILURE":
                break

        final_attempt = attempts[-1]
        final_validation = final_attempt.validation
        validated_output = (
            final_attempt.outcome.output if final_validation.can_proceed else None
        )
        semantic_fidelity = (
            evaluate(validated_output)
            if evaluate is not None and final_validation.can_proceed
            else None
        )
        publication_ready = (
            final_validation.can_proceed if publication_component else None
        )
        hard_safety_gate_breach = (
            validated_output is not None and not final_validation.can_proceed
        ) or (publication_ready is True and not final_validation.can_proceed)
        retry_exhausted = (
            len(attempts) == 2
            and final_validation.failure_class == "AI_SYSTEM_FAILURE"
        )
        reasons = _unique_reasons(
            attempts,
            ("RETRY_EXHAUSTED",) if retry_exhausted else (),
        )
        measurement = self._measurement(
            started=started,
            run_id=run_id,
            case_id=case_id,
            component=component,
            attempts=attempts,
            final_validation=final_validation,
            semantic_fidelity=semantic_fidelity,
            fallback_used=False,
            fallback_type=None,
            publication_ready=publication_ready,
            display_ready=None,
            hard_safety_gate_breach=hard_safety_gate_breach,
            reasons=reasons,
        )
        if measurement_path is not None:
            append_jsonl(measurement_path, measurement)
        return BaselineRunResult(
            validated_output=validated_output,
            attempt_count=len(attempts),
            first_pass_runtime_result=_runtime_label(attempts[0].validation),
            final_runtime_result=_runtime_label(final_validation),
            semantic_fidelity=semantic_fidelity,
            retry_used=len(attempts) == 2,
            fallback_used=False,
            fallback_type=None,
            publication_ready=publication_ready,
            display_ready=None,
            draft_preserved=(not publication_ready if publication_component else None),
            safe_non_consequential=not final_validation.can_proceed,
            hard_safety_gate_breach=hard_safety_gate_breach,
            reasons=reasons,
            measurement=measurement,
        )

    def _invoke(
        self,
        component: str,
        model_input: Mapping[str, Any],
        validate: Callable[[Any], ValidationResult],
    ) -> _Attempt:
        outcome = self.adapter.invoke(component, model_input)
        if outcome.system_failure_reason is not None:
            validation = ValidationResult(
                False,
                "AI_SYSTEM_FAILURE",
                (f"ADAPTER:{outcome.system_failure_reason}",),
            )
        else:
            validation = validate(outcome.output)
        return _Attempt(outcome, validation)

    @staticmethod
    def _validate_npc_output(
        output: Any, metadata: NPCFixtureValidationMetadata
    ) -> ValidationResult:
        if not isinstance(output, str):
            return ValidationResult(
                False, "AI_SYSTEM_FAILURE", ("NPC_SURFACE_TEXT_REQUIRED",)
            )
        gate_result = validate_npc_surface_text(output, metadata)
        if not gate_result.passed:
            return ValidationResult(False, "AI_SYSTEM_FAILURE", gate_result.reasons)
        return ValidationResult(True, "NONE")

    def _measurement(
        self,
        *,
        started: float,
        run_id: str,
        case_id: str,
        component: str,
        attempts: list[_Attempt],
        final_validation: ValidationResult,
        semantic_fidelity: SemanticFidelityResult | None,
        fallback_used: bool,
        fallback_type: str | None,
        publication_ready: bool | None,
        display_ready: bool | None,
        hard_safety_gate_breach: bool,
        reasons: tuple[str, ...],
    ) -> RunMeasurement:
        outcomes = [attempt.outcome for attempt in attempts]
        return RunMeasurement(
            run_id=run_id,
            case_id=case_id,
            component=component,
            manifest_version=self.manifest_version,
            contract_version=self.contract_version,
            adapter_identifier=self.adapter.adapter_identifier,
            model_identifier=self.adapter.model_identifier,
            prompt_version=self.adapter.prompt_version,
            schema_version=self.adapter.schema_version,
            attempt_count=len(attempts),
            first_pass_runtime_result=_runtime_label(attempts[0].validation),
            final_runtime_result=_runtime_label(final_validation),
            semantic_fidelity_result=(
                None
                if semantic_fidelity is None
                else "PASS" if semantic_fidelity.passed else "FAIL"
            ),
            retry_used=len(attempts) == 2,
            fallback_used=fallback_used,
            fallback_type=fallback_type,
            publication_ready=publication_ready,
            display_ready=display_ready,
            input_tokens=_sum_if_complete(outcome.input_tokens for outcome in outcomes),
            output_tokens=_sum_if_complete(outcome.output_tokens for outcome in outcomes),
            model_call_latency_ms=_sum_if_complete(
                outcome.model_call_latency_ms for outcome in outcomes
            ),
            end_to_end_latency_ms=(perf_counter() - started) * 1000,
            estimated_cost=_sum_if_complete(
                outcome.estimated_cost for outcome in outcomes
            ),
            hard_safety_gate_breach=hard_safety_gate_breach,
            reason_codes=reasons,
        )


def _runtime_label(validation: ValidationResult) -> str:
    return "PASS" if validation.can_proceed else validation.failure_class


def _unique_reasons(
    attempts: list[_Attempt], extra_reasons: tuple[str, ...] = ()
) -> tuple[str, ...]:
    reasons = [
        reason
        for attempt in attempts
        for reason in attempt.validation.reasons
    ] + list(extra_reasons)
    return tuple(dict.fromkeys(reasons))


def _sum_if_complete(values) -> int | float | None:
    collected = tuple(values)
    if not collected or any(value is None for value in collected):
        return None
    return sum(collected)
