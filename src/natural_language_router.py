from typing import Any

from src.agent_router import route_agent_request


def route_natural_language_request(
    user_request: str,
    company_code: str,
    user_id: str,
) -> dict[str, Any]:
    """
    Interpret a simple natural-language finance request
    and route it to the correct specialist agent.
    """

    text = user_request.strip().lower()

    if "gl balance" in text or "general ledger" in text:
        return route_agent_request(
            domain="finance",
            request_type="gl_balances",
            company_code=company_code,
            user_id=user_id,
        )

    if "vendor invoice" in text or "open invoice" in text:
        return route_agent_request(
            domain="procurement",
            request_type="vendor_invoices",
            company_code=company_code,
            user_id=user_id,
        )

    return {
        "status": "UNSUPPORTED_REQUEST",
        "message": (
            "The request could not be mapped to a supported "
            "Finance or Procurement agent capability."
        ),
    }