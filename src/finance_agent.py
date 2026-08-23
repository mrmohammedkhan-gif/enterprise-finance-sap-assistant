from typing import Any

from src.mcp_server import (
    close_accounting_period,
    get_gl_balances,
    get_vendor_invoices,
)


def run_finance_agent(
    request_type: str,
    company_code: str,
    user_id: str,
    fiscal_year: int | None = None,
    period_number: int | None = None,
    approval_request_id: str | None = None,
) -> dict[str, Any]:
    """
    Route finance requests to existing governed MCP tools.
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

    if request_type == "close_period":
        if (
            fiscal_year is None
            or period_number is None
            or approval_request_id is None
        ):
            return {
                "status": "MISSING_PARAMETERS",
                "message": (
                    "Fiscal year, period number and approval request ID "
                    "are required to close an accounting period."
                ),
            }

        return close_accounting_period(
            company_code=company_code,
            fiscal_year=fiscal_year,
            period_number=period_number,
            approval_request_id=approval_request_id,
            user_id=user_id,
        )

    return {
        "status": "UNSUPPORTED_REQUEST",
        "message": (
            f"Finance Agent does not support request type "
            f"'{request_type}'."
        ),
    }