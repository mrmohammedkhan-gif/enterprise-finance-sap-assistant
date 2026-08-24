from typing import Any

from src.agent_request_schema import (
    AgentRequest,
    validate_agent_request,
)
from src.agent_router import route_agent_request


def route_structured_request(
    request: AgentRequest,
) -> dict[str, Any]:
    """
    Validate a structured agent request before routing it
    to the existing specialist-agent layer.
    """

    validation = validate_agent_request(
        request
    )

    if validation["status"] != "VALID_AGENT_REQUEST":
        return {
            "status": "BLOCKED",
            "reason": "INVALID_AGENT_REQUEST",
            "validation": validation,
        }

    result = route_agent_request(
        domain=request.domain,
        request_type=request.request_type,
        company_code=request.context.company_code,
        user_id=request.context.user_id,
    )

    return {
        **result,
        "context": {
            "request_id": request.context.request_id,
            "company_code": request.context.company_code,
            "fiscal_year": request.context.fiscal_year,
            "period_number": request.context.period_number,
            "user_id": request.context.user_id,
            "user_role": request.context.user_role,
        },
    }