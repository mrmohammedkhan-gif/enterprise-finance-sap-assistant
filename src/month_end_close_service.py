from datetime import datetime
from typing import Any

from src.close_readiness_service import check_close_readiness
from src.posting_period_service import close_period
from src.close_persistence import add_close_audit_record


CLOSE_AUDIT_LOG: list[dict[str, Any]] = []


def execute_period_close(
    company_code: str,
    fiscal_year: int,
    period_number: int,
    approved_by: str,
) -> dict[str, Any]:
    """
    Close an accounting period only after:
    1. Close-readiness controls pass.
    2. A human approver is supplied.
    3. The close action is recorded in the audit log.
    """

    readiness = check_close_readiness(
        company_code=company_code,
        fiscal_year=fiscal_year,
        period_number=period_number,
    )

    if readiness["status"] != "READY":
        raise ValueError(
            "Period cannot be closed because "
            "close-readiness controls have not passed."
        )

    approver = approved_by.strip()

    if not approver:
        raise ValueError(
            "Human approval is required before period close."
        )

    closed_period = close_period(
        company_code=company_code,
        fiscal_year=fiscal_year,
        period_number=period_number,
    )

    closed_at = datetime.now().isoformat()

    audit_id = add_close_audit_record(
        company_code=company_code,
        fiscal_year=fiscal_year,
        period_number=period_number,
        action="PERIOD_CLOSED",
        approved_by=approver,
        action_at=closed_at,
        readiness_status=readiness["status"],
    )

    audit_record = {
        "audit_id": audit_id,
        "company_code": company_code,
        "fiscal_year": fiscal_year,
        "period_number": period_number,
        "action": "PERIOD_CLOSED",
        "approved_by": approver,
        "closed_at": closed_at,
        "readiness_status": readiness["status"],
    }

    CLOSE_AUDIT_LOG.append(audit_record)

    return {
        "status": "CLOSED",
        "period": closed_period,
        "audit_record": audit_record,
    }