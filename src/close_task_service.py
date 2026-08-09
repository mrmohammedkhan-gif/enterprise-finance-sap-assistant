from datetime import datetime
from typing import Any

from src.close_persistence import (
    get_persisted_close_task,
    get_persisted_close_tasks,
    save_close_task,
)


CLOSE_TASK_TEMPLATES: list[dict[str, str]] = [
    {
        "template_id": "CLOSE-001",
        "task_name": "Bank reconciliation",
        "owner": "Financial Accountant",
    },
    {
        "template_id": "CLOSE-002",
        "task_name": "Review AP exceptions",
        "owner": "AP Manager",
    },
    {
        "template_id": "CLOSE-003",
        "task_name": "Review accruals and prepayments",
        "owner": "Finance Manager",
    },
]


def build_task_id(
    company_code: str,
    fiscal_year: int,
    period_number: int,
    template_id: str,
) -> str:
    """
    Build a unique close-task ID for one accounting period.
    """
    return (
        f"{company_code.upper()}-"
        f"{fiscal_year}-"
        f"{period_number:02d}-"
        f"{template_id}"
    )


def initialise_close_tasks(
    company_code: str,
    fiscal_year: int,
    period_number: int,
) -> list[dict[str, Any]]:
    """
    Create any missing month-end close tasks for one period.
    """
    company_code = company_code.upper()

    for template in CLOSE_TASK_TEMPLATES:
        task_id = build_task_id(
            company_code=company_code,
            fiscal_year=fiscal_year,
            period_number=period_number,
            template_id=template["template_id"],
        )

        existing_task = get_persisted_close_task(
            task_id
        )

        if existing_task is not None:
            continue

        task = {
            "task_id": task_id,
            "company_code": company_code,
            "fiscal_year": fiscal_year,
            "period_number": period_number,
            "task_name": template["task_name"],
            "status": "PENDING",
            "owner": template["owner"],
            "completed_by": None,
            "completed_at": None,
        }

        save_close_task(task)

    return get_persisted_close_tasks(
        company_code=company_code,
        fiscal_year=fiscal_year,
        period_number=period_number,
    )


def get_close_tasks(
    company_code: str,
    fiscal_year: int,
    period_number: int,
) -> list[dict[str, Any]]:
    """
    Return persistent close tasks for one accounting period.
    """
    return get_persisted_close_tasks(
        company_code=company_code,
        fiscal_year=fiscal_year,
        period_number=period_number,
    )


def complete_close_task(
    task_id: str,
    completed_by: str,
) -> dict[str, Any]:
    """
    Mark one persisted month-end close task as completed.
    """
    completed_by = completed_by.strip()

    if not completed_by:
        raise ValueError(
            "A named user is required to complete a close task."
        )

    task = get_persisted_close_task(
        task_id
    )

    if task is None:
        raise ValueError(
            f"Close task {task_id} was not found."
        )

    if task["status"] == "COMPLETED":
        raise ValueError(
            f"Close task {task_id} is already completed."
        )

    task["status"] = "COMPLETED"
    task["completed_by"] = completed_by
    task["completed_at"] = datetime.now().isoformat()

    save_close_task(task)

    return task