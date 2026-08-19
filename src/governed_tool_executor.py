from typing import Any, Callable

from src.tool_governance import (
    can_ai_execute_tool,
    get_tool_policy,
)


def execute_governed_tool(
    tool_name: str,
    tool_function: Callable[..., Any],
    tool_arguments: dict[str, Any],
    human_approved: bool = False,
) -> dict[str, Any]:
    """
    Execute a finance tool only when governance policy allows it.
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
            "message": (
                f"Execution of tool '{tool_name}' "
                "is not permitted under the current governance policy."
            ),
        }

    result = tool_function(
        **tool_arguments
    )

    return {
        "status": "EXECUTED",
        "tool_name": tool_name,
        "permission": policy["permission"],
        "result": result,
    }