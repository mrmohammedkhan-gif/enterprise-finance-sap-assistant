from typing import Any, Callable

from src.approval_service import get_approval_request
from src.finance_rbac import is_user_authorised
from src.tool_governance import (
    can_ai_execute_tool,
    get_tool_policy,
)


def execute_governed_tool(
    tool_name: str,
    tool_function: Callable[..., Any],
    tool_arguments: dict[str, Any],
    approval_request_id: str | None = None,
    user_id: str | None = None,
    company_code: str | None = None,
) -> dict[str, Any]:
    """
    Execute a finance tool only when:
    1. Tool governance allows it.
    2. A valid persisted approval exists when required.
    3. The approver is authorised.
    4. The user is authorised for the action and Company Code.
    """

    policy = get_tool_policy(tool_name)

    human_approved = False
    approval_request = None

    # -----------------------------------------------------
    # TRUSTED APPROVAL CHECK
    # -----------------------------------------------------

    if policy["requires_human_approval"]:

        if approval_request_id is None:
            return {
                "status": "BLOCKED",
                "tool_name": tool_name,
                "permission": policy["permission"],
                "reason": "APPROVAL_REQUIRED",
                "message": (
                    "A persisted human approval request "
                    "is required before this tool can execute."
                ),
            }

        approval_request = get_approval_request(
            approval_request_id
        )

        if approval_request is None:
            return {
                "status": "BLOCKED",
                "tool_name": tool_name,
                "permission": policy["permission"],
                "reason": "APPROVAL_NOT_FOUND",
                "message": (
                    f"Approval request '{approval_request_id}' "
                    "was not found."
                ),
            }

        if approval_request["status"] != "APPROVED":
            return {
                "status": "BLOCKED",
                "tool_name": tool_name,
                "permission": policy["permission"],
                "reason": "APPROVAL_NOT_APPROVED",
                "approval_status": approval_request["status"],
                "message": (
                    "The approval request has not been approved."
                ),
            }

        if approval_request["tool_name"] != tool_name:
            return {
                "status": "BLOCKED",
                "tool_name": tool_name,
                "permission": policy["permission"],
                "reason": "APPROVAL_TOOL_MISMATCH",
                "message": (
                    "The approval request does not match "
                    "the requested finance tool."
                ),
            }

        if (
            company_code is None
            or approval_request["company_code"]
            != company_code.upper()
        ):
            return {
                "status": "BLOCKED",
                "tool_name": tool_name,
                "permission": policy["permission"],
                "reason": "APPROVAL_COMPANY_MISMATCH",
                "message": (
                    "The approval request does not match "
                    "the requested Company Code."
                ),
            }

        approved_by = approval_request["approved_by"]

        if not approved_by:
            return {
                "status": "BLOCKED",
                "tool_name": tool_name,
                "permission": policy["permission"],
                "reason": "APPROVER_MISSING",
                "message": (
                    "The approval record does not contain "
                    "an approver identity."
                ),
            }

        approver_authorised = is_user_authorised(
            user_id=approved_by,
            action=tool_name,
            company_code=company_code,
        )

        if not approver_authorised:
            return {
                "status": "BLOCKED",
                "tool_name": tool_name,
                "permission": policy["permission"],
                "reason": "APPROVER_RBAC_DENIED",
                "approved_by": approved_by,
                "message": (
                    f"Approver '{approved_by}' is not authorised "
                    f"to approve '{tool_name}' for Company Code "
                    f"'{company_code.upper()}'."
                ),
            }

        human_approved = True

    # -----------------------------------------------------
    # TOOL GOVERNANCE
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # USER IDENTITY AND COMPANY CODE
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # RBAC
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # EXECUTION
    # -----------------------------------------------------

    result = tool_function(
        **tool_arguments
    )

    return {
        "status": "EXECUTED",
        "tool_name": tool_name,
        "permission": policy["permission"],
        "user_id": user_id,
        "company_code": company_code.upper(),
        "approval_request_id": approval_request_id,
        "result": result,
    }