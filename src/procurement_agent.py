from typing import Any

from src.mcp_server import get_vendor_invoices


def run_procurement_agent(
    request_type: str,
    company_code: str,
    user_id: str,
) -> dict[str, Any]:
    """
    Route procurement/AP requests to governed MCP tools.
    """

    request_type = request_type.strip().lower()

    if request_type == "vendor_invoices":
        return get_vendor_invoices(
            company_code=company_code,
            user_id=user_id,
        )

    return {
        "status": "UNSUPPORTED_REQUEST",
        "message": (
            f"Procurement Agent does not support request type "
            f"'{request_type}'."
        ),
    }