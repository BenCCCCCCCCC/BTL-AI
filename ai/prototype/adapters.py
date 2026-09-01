"""Provider-independent scripted adapter for Batch 2A policy tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol, Sequence


@dataclass(frozen=True)
class AdapterOutcome:
    output: Any = None
    system_failure_reason: str | None = None
    model_identifier: str | None = None
    prompt_version: str | None = None
    schema_version: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    model_call_latency_ms: float | None = None
    estimated_cost: float | None = None

    @classmethod
    def success(
        cls,
        output: Any,
        *,
        model_identifier: str | None = None,
        prompt_version: str | None = None,
        schema_version: str | None = None,
        input_tokens: int | None = None,
        output_tokens: int | None = None,
        model_call_latency_ms: float | None = None,
        estimated_cost: float | None = None,
    ) -> AdapterOutcome:
        return cls(
            output=output,
            model_identifier=model_identifier,
            prompt_version=prompt_version,
            schema_version=schema_version,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            model_call_latency_ms=model_call_latency_ms,
            estimated_cost=estimated_cost,
        )

    @classmethod
    def system_failure(
        cls,
        reason: str,
        *,
        model_identifier: str | None = None,
        prompt_version: str | None = None,
        schema_version: str | None = None,
        input_tokens: int | None = None,
        output_tokens: int | None = None,
        model_call_latency_ms: float | None = None,
        estimated_cost: float | None = None,
    ) -> AdapterOutcome:
        return cls(
            system_failure_reason=reason,
            model_identifier=model_identifier,
            prompt_version=prompt_version,
            schema_version=schema_version,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            model_call_latency_ms=model_call_latency_ms,
            estimated_cost=estimated_cost,
        )


@dataclass(frozen=True)
class AdapterCall:
    component: str
    model_input: Mapping[str, Any]


class ModelAdapter(Protocol):
    adapter_identifier: str
    model_identifier: str | None
    prompt_version: str | None
    schema_version: str | None

    def invoke(
        self, component: str, model_input: Mapping[str, Any]
    ) -> AdapterOutcome: ...


class ScriptedAdapter:
    """Return authored outcomes in order without calling a model or provider."""

    adapter_identifier = "scripted"

    def __init__(
        self,
        outcomes: Sequence[AdapterOutcome],
        *,
        model_identifier: str | None = None,
        prompt_version: str | None = None,
        schema_version: str | None = None,
    ) -> None:
        self._outcomes = tuple(outcomes)
        self._next_outcome = 0
        self.model_identifier = model_identifier
        self.prompt_version = prompt_version
        self.schema_version = schema_version
        self.calls: list[AdapterCall] = []

    def invoke(
        self, component: str, model_input: Mapping[str, Any]
    ) -> AdapterOutcome:
        if self._next_outcome >= len(self._outcomes):
            raise RuntimeError("scripted adapter outcome sequence exhausted")
        self.calls.append(AdapterCall(component, model_input))
        outcome = self._outcomes[self._next_outcome]
        self._next_outcome += 1
        return outcome
