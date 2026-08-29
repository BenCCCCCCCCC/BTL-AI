from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from ai.prototype.consequence_stub import (
    AuthoredConsequenceEvent,
    DeterministicallyResolvedGameplayResult,
    ExperimentalAuthoritativeTestState,
    ExperimentalVariableEffect,
    GlobalVariable,
    apply_authored_consequence_event,
)


def test_authored_consequence_event_applies_experimental_effects_to_all_variables() -> None:
    state = ExperimentalAuthoritativeTestState(money=100)
    result = DeterministicallyResolvedGameplayResult("RESULT_PUBLICATION_01")
    event = AuthoredConsequenceEvent(
        event_id="EVENT_EXPERIMENTAL_01",
        source_result_id=result.result_id,
        effects=(
            ExperimentalVariableEffect(GlobalVariable.REPUTATION, 1),
            ExperimentalVariableEffect(GlobalVariable.PUBLIC_OPINION, -1),
            ExperimentalVariableEffect(GlobalVariable.THREAT_LEVEL, 2),
            ExperimentalVariableEffect(GlobalVariable.MONEY, -50),
        ),
    )

    updated = apply_authored_consequence_event(state, result, event)

    assert state.as_dict() == {
        "Reputation": 0,
        "Public Opinion": 0,
        "Threat Level": 0,
        "Money": 100,
    }
    assert updated.as_dict() == {
        "Reputation": 1,
        "Public Opinion": -1,
        "Threat Level": 2,
        "Money": 50,
    }


@pytest.mark.parametrize(
    ("artifact_name", "artifact"),
    [
        ("raw LLM output", "set Reputation to 99"),
        ("Dialogue semantic candidate", {"status": "RESOLVED", "act": "REQUEST"}),
        ("Claim Atom", {"target_id": "FIRE_FIRST", "commitment_mode": "ASSERTED"}),
        ("publication-support label", "SUPPORTED"),
        ("NPC surface text", "You are respected now."),
    ],
)
def test_ai_language_artifacts_cannot_directly_mutate_variables(
    artifact_name: str, artifact: object
) -> None:
    state = ExperimentalAuthoritativeTestState()
    result = DeterministicallyResolvedGameplayResult("RESULT_01")
    with pytest.raises(TypeError):
        apply_authored_consequence_event(state, result, artifact)  # type: ignore[arg-type]
    assert state == ExperimentalAuthoritativeTestState(), artifact_name


def test_event_must_match_a_resolved_gameplay_result() -> None:
    state = ExperimentalAuthoritativeTestState()
    unresolved = DeterministicallyResolvedGameplayResult("RESULT_01", resolved=False)
    event = AuthoredConsequenceEvent("EVENT_01", "RESULT_01", ())
    with pytest.raises(ValueError, match="not deterministically resolved"):
        apply_authored_consequence_event(state, unresolved, event)

    resolved = DeterministicallyResolvedGameplayResult("RESULT_02")
    with pytest.raises(ValueError, match="does not match"):
        apply_authored_consequence_event(state, resolved, event)


def test_experimental_authoritative_state_is_immutable() -> None:
    state = ExperimentalAuthoritativeTestState()
    with pytest.raises(FrozenInstanceError):
        state.reputation = 100  # type: ignore[misc]
