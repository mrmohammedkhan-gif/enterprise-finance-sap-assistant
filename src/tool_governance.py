from typing import Any


TOOL_POLICIES: dict[str, dict[str, Any]] = {
    "get_gl_balances": {
        "permission": "READ_ONLY",
        "requires_human_approval": False,
        "description": "Read General Ledger balances.",
    },
    "get_vendor_invoices": {
        "permission": "READ_ONLY",
        "requires_human_approval": False,
        "description": "Read vendor invoice information.",
    },
    "get_close_readiness": {
        "permission": "READ_ONLY",
        "requires_human_approval": False,
        "description": "Read month-end close readiness controls.",
    },
    "create_journal_entry": {
        "permission": "APPROVAL_REQUIRED",
        "requires_human_approval": True,
        "description": "Create a journal entry.",
    },
    "close_accounting_period": {
        "permission": "APPROVAL_REQUIRED",
        "requires_human_approval": True,
        "description": "Close an accounting period.",
    },
}


def get_tool_policy(
    tool_name: str,
) -> dict[str, Any]:
    """
    Return the governance policy for one AI tool.
    """
    policy = TOOL_POLICIES.get(tool_name)

    if policy is None:
        return {
            "permission": "PROHIBITED",
            "requires_human_approval": True,
            "description": "Tool is not approved for AI use.",
        }

    return {
        "tool_name": tool_name,
        **policy,
    }


def can_ai_execute_tool(
    tool_name: str,
    human_approved: bool = False,
) -> bool:
    """
    Decide whether the AI is allowed to execute a tool.
    """
    policy = get_tool_policy(tool_name)

    if policy["permission"] == "PROHIBITED":
        return False

    if policy["permission"] == "READ_ONLY":
        return True

    if (
        policy["permission"] == "APPROVAL_REQUIRED"
        and human_approved
    ):
        return True

    return False