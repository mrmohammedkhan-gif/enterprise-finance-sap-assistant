from dataclasses import dataclass, field
from typing import Any

from src.finance_context import (
    FinanceContext,
    validate_finance_context,
)


@dataclass
class AgentSharedState:
    """
    Controlled shared state for specialist agents
    participating in the same finance request.
    """

    context: FinanceContext
    current_agent: str
    completed_agents: list[str] = field(default_factory=list)
    state_data: dict[str, Any] = field(default_factory=dict)
    memory_events: list[dict[str, Any]] = field(default_factory=list)


def create_shared_state(
    context: FinanceContext,
    initial_agent: str,
) -> AgentSharedState:
    """
    Create shared state for one governed finance request.
    """

    return AgentSharedState(
        context=context,
        current_agent=initial_agent,
    )


def update_shared_state(
    state: AgentSharedState,
    key: str,
    value: Any,
) -> AgentSharedState:
    """
    Store controlled cross-agent state for the current request.
    """

    state.state_data[key] = value
    return state


def complete_agent_step(
    state: AgentSharedState,
    agent_name: str,
) -> AgentSharedState:
    """
    Mark one specialist agent as completed.
    """

    if agent_name not in state.completed_agents:
        state.completed_agents.append(agent_name)

    return state


def handoff_to_agent(
    state: AgentSharedState,
    next_agent: str,
) -> AgentSharedState:
    """
    Transfer control to another specialist agent while
    preserving a valid finance context and recording the handoff.
    """

    validation = validate_finance_context(
        state.context
    )

    if validation["status"] != "VALID_CONTEXT":
        raise ValueError(
            "Cannot hand off agent state with invalid finance context."
        )

    previous_agent = state.current_agent

    state.current_agent = next_agent

    add_memory_event(
        state=state,
        agent_name=previous_agent,
        event_type="AGENT_HANDOFF",
        payload={
            "from_agent": previous_agent,
            "to_agent": next_agent,
        },
    )

    return state

def add_memory_event(
    state: AgentSharedState,
    agent_name: str,
    event_type: str,
    payload: dict[str, Any],
) -> AgentSharedState:
    """
    Record one request-scoped cross-agent memory event.
    """

    state.memory_events.append(
        {
            "request_id": state.context.request_id,
            "agent_name": agent_name,
            "event_type": event_type,
            "payload": payload,
        }
    )

    return state

def get_memory_events(
    state: AgentSharedState,
    event_type: str | None = None,
) -> list[dict[str, Any]]:
    """
    Return request-scoped memory events, optionally filtered
    by event type.
    """

    if event_type is None:
        return list(state.memory_events)

    return [
        event
        for event in state.memory_events
        if event["event_type"] == event_type
    ]