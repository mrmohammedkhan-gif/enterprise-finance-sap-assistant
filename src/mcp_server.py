from typing import Any

from mcp.server import MCPServer


from mock_sap.app import (
    list_gl_balances,
    list_open_vendor_invoices,
)
from src.governed_tool_executor import execute_governed_tool
from src.month_end_close_service import execute_period_close


mcp = MCPServer(
    "Enterprise SAP Finance Assistant"
)


@mcp.tool()
def health_check() -> dict[str, str]:
    """
    Confirm that the Enterprise SAP Finance MCP server is available.
    """
    return {
        "status": "OK",
        "service": "Enterprise SAP Finance Assistant",
    }


@mcp.tool()
def get_gl_balances(
    company_code: str,
    user_id: str,
) -> dict[str, Any]:
    """
    Return General Ledger balances for one Company Code.

    This is a READ_ONLY finance tool and remains subject
    to governance and RBAC controls.

    """
@mcp.tool()
def get_vendor_invoices(
    company_code: str,
    user_id: str,
) -> dict[str, Any]:
    """
    Return open vendor invoices for one Company Code.

    This is a READ_ONLY finance tool and remains subject
    to governance and RBAC controls.

    """
@mcp.tool()
def close_accounting_period(
    company_code: str,
    fiscal_year: int,
    period_number: int,
    approval_request_id: str,
    user_id: str,
) -> dict[str, Any]:
    """
    Close one accounting period through the governed MCP layer.

    This action requires:
    - a persisted approved request,
    - valid RBAC for the user and approver,
    - matching Company Code,
    - finance close-readiness controls to pass.
    """

    return execute_governed_tool(
        tool_name="close_accounting_period",
        tool_function=execute_period_close,
        tool_arguments={
            "company_code": company_code,
            "fiscal_year": fiscal_year,
            "period_number": period_number,
            "approved_by": user_id,
        },
        approval_request_id=approval_request_id,
        user_id=user_id,
        company_code=company_code,
    )
  
    return execute_governed_tool(
        tool_name="get_gl_balances",
        tool_function=list_gl_balances,
        tool_arguments={
            "company_code": company_code,
        },
        user_id=user_id,
        company_code=company_code,
    )


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        json_response=True,
    )