from typing import Any

from src.finance_agent import run_finance_agent
from src.procurement_agent import run_procurement_agent


def route_agent_request(
    domain: str,
    request_type: str,
    company_code: str,
    user_id: str,
) -> dict[str, Any]:
    """
    Route a request to the appropriate specialist agent.
    """

    domain = domain.strip().lower()

    if domain == "finance":
        return run_finance_agent(
            request_type=request_type,
            company_code=company_code,
            user_id=user_id,
        )

    if domain in {"procurement", "ap"}:
        return run_procurement_agent(
            request_type=request_type,
            company_code=company_code,
            user_id=user_id,
        )

    return {
        "status": "UNSUPPORTED_DOMAIN",
        "message": (
            f"No specialist agent is configured for domain "
            f"'{domain}'."
        ),
    }