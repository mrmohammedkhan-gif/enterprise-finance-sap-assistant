from src.agent_shared_state import AgentSharedState


_STATE_STORE: dict[str, AgentSharedState] = {}


def save_agent_state(
    state: AgentSharedState,
) -> AgentSharedState:
    """
    Save shared agent state by finance request ID.
    """

    request_id = state.context.request_id
    _STATE_STORE[request_id] = state

    return state


def get_agent_state(
    request_id: str,
) -> AgentSharedState | None:
    """
    Retrieve shared agent state for one finance request.
    """

    return _STATE_STORE.get(request_id)

def get_agent_state_result(
    request_id: str,
) -> dict[str, object]:
    """
    Return an explicit state lookup result for one request ID.
    """

    state = get_agent_state(request_id)

    if state is None:
        return {
            "status": "STATE_NOT_FOUND",
            "request_id": request_id,
            "state": None,
        }

    return {
        "status": "STATE_FOUND",
        "request_id": request_id,
        "state": state,
    }