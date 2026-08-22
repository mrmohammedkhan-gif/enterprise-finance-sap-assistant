from typing import Any

from mcp.server import MCPServer

from mock_sap.app import (
    list_gl_balances,
    list_open_vendor_invoices,
)
from src.governed_tool_executor import execute_governed_tool


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

    return execute_governed_tool(
        tool_name="get_vendor_invoices",
        tool_function=list_open_vendor_invoices,
        tool_arguments={
            "company_code": company_code,
        },
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