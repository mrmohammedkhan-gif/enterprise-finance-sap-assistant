from typing import Any, Callable

from src.finance_rbac import is_user_authorised
from src.tool_governance import (
    can_ai_execute_tool,
    get_tool_policy,
)


def execute_governed_tool(
    tool_name: str,
    tool_function: Callable[..., Any],
    tool_arguments: dict[str, Any],
    human_approved: bool = False,
    user_id: str | None = None,
    company_code: str | None = None,
) -> dict[str, Any]:
    """
    Execute a finance tool only when:
    1. Tool governance allows it.
    2. Human approval is present when required.
    3. The user is authorised for the action and Company Code.
    """

    policy = get_tool_policy(tool_name)

    allowed = can_ai_execute_tool(
        tool_name=tool_name,
        human_approved=human_approved,
    )

    if not allowed:
        return {
            "status": "BLOCKED",
            "tool_name": tool_name,
            "permission": policy["permission"],
            "requires_human_approval": policy[
                "requires_human_approval"
            ],
            "reason": "GOVERNANCE_POLICY",
            "message": (
                f"Execution of tool '{tool_name}' "
                "is not permitted under the current governance policy."
            ),
        }

    if user_id is None or company_code is None:
        return {
            "status": "BLOCKED",
            "tool_name": tool_name,
            "permission": policy["permission"],
            "reason": "MISSING_IDENTITY_OR_COMPANY_CODE",
            "message": (
                "User identity and Company Code are required "
                "before this finance action can execute."
            ),
        }

    authorised = is_user_authorised(
        user_id=user_id,
        action=tool_name,
        company_code=company_code,
    )

    if not authorised:
        return {
            "status": "BLOCKED",
            "tool_name": tool_name,
            "permission": policy["permission"],
            "reason": "RBAC_DENIED",
            "user_id": user_id,
            "company_code": company_code.upper(),
            "message": (
                f"User '{user_id}' is not authorised to execute "
                f"'{tool_name}' for Company Code "
                f"'{company_code.upper()}'."
            ),
        }

    result = tool_function(
        **tool_arguments
    )

    return {
        "status": "EXECUTED",
        "tool_name": tool_name,
        "permission": policy["permission"],
        "user_id": user_id,
        "company_code": company_code.upper(),
        "result": result,
    }