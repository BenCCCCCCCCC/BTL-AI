"""Experimental deterministic Consequence Event interface.

Placeholder deltas exercise the authority boundary only. They are not final
ranges, formulas, balance, decay, cross-variable rules, or ending thresholds.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum


class GlobalVariable(str, Enum):
    REPUTATION = "Reputation"
    PUBLIC_OPINION = "Public Opinion"
    THREAT_LEVEL = "Threat Level"
    MONEY = "Money"


@dataclass(frozen=True)
class DeterministicallyResolvedGameplayResult:
    result_id: str
    resolved: bool = True


@dataclass(frozen=True)
class ExperimentalVariableEffect:
    variable: GlobalVariable
    delta: int
    experimental_placeholder: bool = True


@dataclass(frozen=True)
class AuthoredConsequenceEvent:
    event_id: str
    source_result_id: str
    effects: tuple[ExperimentalVariableEffect, ...]
    authored: bool = True


@dataclass(frozen=True)
class ExperimentalAuthoritativeTestState:
    reputation: int = 0
    public_opinion: int = 0
    threat_level: int = 0
    money: int = 0

    def as_dict(self) -> dict[str, int]:
        return {
            GlobalVariable.REPUTATION.value: self.reputation,
            GlobalVariable.PUBLIC_OPINION.value: self.public_opinion,
            GlobalVariable.THREAT_LEVEL.value: self.threat_level,
            GlobalVariable.MONEY.value: self.money,
        }


def apply_authored_consequence_event(
    state: ExperimentalAuthoritativeTestState,
    result: DeterministicallyResolvedGameplayResult,
    event: AuthoredConsequenceEvent,
) -> ExperimentalAuthoritativeTestState:
    """Apply only an authored event linked to an already resolved result."""

    if not isinstance(state, ExperimentalAuthoritativeTestState):
        raise TypeError("state must be ExperimentalAuthoritativeTestState")
    if not isinstance(result, DeterministicallyResolvedGameplayResult):
        raise TypeError("result must be DeterministicallyResolvedGameplayResult")
    if not isinstance(event, AuthoredConsequenceEvent):
        raise TypeError("event must be AuthoredConsequenceEvent")
    if not result.resolved:
        raise ValueError("gameplay result is not deterministically resolved")
    if not event.authored:
        raise ValueError("consequence event is not authored")
    if event.source_result_id != result.result_id:
        raise ValueError("consequence event does not match the resolved result")
    if not all(effect.experimental_placeholder for effect in event.effects):
        raise ValueError("Batch 1 accepts Experimental placeholder effects only")

    updated = state
    for effect in event.effects:
        if effect.variable is GlobalVariable.REPUTATION:
            updated = replace(updated, reputation=updated.reputation + effect.delta)
        elif effect.variable is GlobalVariable.PUBLIC_OPINION:
            updated = replace(updated, public_opinion=updated.public_opinion + effect.delta)
        elif effect.variable is GlobalVariable.THREAT_LEVEL:
            updated = replace(updated, threat_level=updated.threat_level + effect.delta)
        elif effect.variable is GlobalVariable.MONEY:
            updated = replace(updated, money=updated.money + effect.delta)
        else:
            raise ValueError(f"unsupported global variable: {effect.variable}")
    return updated
