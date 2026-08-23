from typing import Any

from src.mcp_server import (
    get_gl_balances,
    get_vendor_invoices,
)


def run_finance_agent(
    request_type: str,
    company_code: str,
    user_id: str,
) -> dict[str, Any]:
    """
    Route a finance request to an existing governed MCP tool.
    """

    request_type = request_type.strip().lower()

    if request_type == "gl_balances":
        return get_gl_balances(
            company_code=company_code,
            user_id=user_id,
        )

    if request_type == "vendor_invoices":
        return get_vendor_invoices(
            company_code=company_code,
            user_id=user_id,
        )

    return {
        "status": "UNSUPPORTED_REQUEST",
        "message": (
            f"Finance Agent does not support request type "
            f"'{request_type}'."
        ),
    }