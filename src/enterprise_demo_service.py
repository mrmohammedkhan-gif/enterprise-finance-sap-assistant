from typing import Any

from src.finance_context import create_finance_context
from src.agent_request_schema import AgentRequest
from src.request_parameter_schemas import GLBalanceParameters
from src.context_aware_router import route_structured_request
from src.agent_shared_state import (
    create_shared_state,
    add_memory_event,
    complete_agent_step,
)
from src.agent_state_store import save_agent_state


def run_finance_demo(
    company_code: str,
    fiscal_year: int,
    period_number: int,
    user_id: str,
    user_role: str,
) -> dict[str, Any]:
    """
    Run one end-to-end governed finance demo request.
    """

    context = create_finance_context(
        company_code=company_code,
        fiscal_year=fiscal_year,
        period_number=period_number,
        user_id=user_id,
        user_role=user_role,
    )

    shared_state = create_shared_state(
        context=context,
        initial_agent="finance_agent",
    )

    request = AgentRequest(
        domain="finance",
        request_type="gl_balances",
        context=context,
        parameters=GLBalanceParameters(
            company_code=company_code,
        ),
    )

    result = route_structured_request(
        request
    )

    add_memory_event(
        state=shared_state,
        agent_name="finance_agent",
        event_type="GL_BALANCE_REQUEST_COMPLETED",
        payload={
            "status": result.get("status"),
            "tool_name": result.get("tool_name"),
        },
    )

    complete_agent_step(
        shared_state,
        "finance_agent",
    )

    save_agent_state(
        shared_state
    )

    return {
        "status": result.get("status"),
        "request_id": context.request_id,
        "context": result.get("context"),
        "finance_result": result,
        "shared_state": shared_state,
    }