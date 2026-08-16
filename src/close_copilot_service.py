from typing import Any

from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from src.close_readiness_service import check_close_readiness
from src.close_task_service import get_close_tasks
from src.posting_period_service import find_posting_period
from src.graph import finance_graph

def analyse_month_end_close(
    company_code: str,
    fiscal_year: int,
    period_number: int,
) -> dict[str, Any]:
    """
    Collect the controlled finance information required
    by the Month-End Close Copilot.

    This function does not close the accounting period.
    It only analyses the current close position.
    """

    company_code = company_code.upper()

    posting_period = find_posting_period(
        company_code=company_code,
        fiscal_year=fiscal_year,
        period_number=period_number,
    )

    readiness = check_close_readiness(
        company_code=company_code,
        fiscal_year=fiscal_year,
        period_number=period_number,
    )

    close_tasks = get_close_tasks(
        company_code=company_code,
        fiscal_year=fiscal_year,
        period_number=period_number,
    )

    incomplete_tasks = [
        task
        for task in close_tasks
        if task["status"] != "COMPLETED"
    ]

    blockers = readiness.get(
        "blockers",
        [],
    )

    return {
        "company_code": company_code,
        "fiscal_year": fiscal_year,
        "period_number": period_number,
        "posting_period": posting_period,
        "readiness_status": readiness["status"],
        "checks": readiness["checks"],
        "blockers": blockers,
        "close_tasks": close_tasks,
        "incomplete_tasks": incomplete_tasks,
        "requires_human_approval": True,
    }

def build_close_copilot_summary(
    company_code: str,
    fiscal_year: int,
    period_number: int,
) -> str:
    """
    Build a deterministic finance summary that can be given
    to an AI model for explanation and recommendation.
    """

    analysis = analyse_month_end_close(
        company_code=company_code,
        fiscal_year=fiscal_year,
        period_number=period_number,
    )

    posting_period = analysis["posting_period"]
    readiness_status = analysis["readiness_status"]
    blockers = analysis["blockers"]
    incomplete_tasks = analysis["incomplete_tasks"]

    period_status = (
        posting_period["status"]
        if posting_period is not None
        else "NOT CONFIGURED"
    )

    if period_status == "CLOSED":
        return (
            f"Company Code {company_code.upper()}, "
            f"fiscal year {fiscal_year}, period {period_number} "
            "is already CLOSED. "
            "The accounting period must not be closed again. "
            "Historical close information should be reviewed "
            "through the audit trail."
        )

    if readiness_status == "READY":
        return (
            f"Company Code {company_code.upper()}, "
            f"fiscal year {fiscal_year}, period {period_number} "
            "is READY for month-end close. "
            "All configured close-readiness controls have passed. "
            "Human approval is still required before the period "
            "can be closed."
        )

    blocker_messages = [
        blocker["message"]
        for blocker in blockers
    ]

    incomplete_task_names = [
        task["task_name"]
        for task in incomplete_tasks
    ]

    return (
        f"Company Code {company_code.upper()}, "
        f"fiscal year {fiscal_year}, period {period_number} "
        "is NOT READY for month-end close. "
        f"Blockers: {blocker_messages}. "
        f"Incomplete close tasks: {incomplete_task_names}. "
        "The identified issues must be resolved before "
        "human approval and period close."
    )

def get_ai_close_explanation(
    company_code: str,
    fiscal_year: int,
    period_number: int,
) -> str:
    """
    Ask the finance AI to explain the trusted
    month-end close analysis.

    The AI is advisory only and must not execute
    the accounting-period close.
    """

    trusted_summary = build_close_copilot_summary(
        company_code=company_code,
        fiscal_year=fiscal_year,
        period_number=period_number,
    )

    system_instruction = (
        "You are an enterprise Finance Month-End Close Copilot. "
        "Use only the trusted finance-control information supplied. "
        "Do not invent balances, invoices, controls or approvals. "
        "Explain the accounting position clearly for a Finance Manager. "
        "If the period is not ready, explain the blockers and required actions. "
        "If the period is ready, state that human approval is still required. "
        "If the period is already closed, do not recommend closing it again. "
        "You are advisory only and cannot execute the period close."
    )

    result = finance_graph.invoke(
        {
            "messages": [
                SystemMessage(
                    content=system_instruction
                ),
                HumanMessage(
                    content=(
                        "Explain this month-end close position:\n\n"
                        f"{trusted_summary}"
                    )
                ),
            ]
        }
    )

    final_message = result["messages"][-1]

    return str(final_message.content)