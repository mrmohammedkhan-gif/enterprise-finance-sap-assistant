from typing import Any

from mock_sap.journal_entries_data import get_company_journal_entries
from mock_sap.trial_balance_data import calculate_trial_balance
from mock_sap.vendor_invoices_data import get_all_vendor_invoices
from src.posting_period_service import find_posting_period
from src.close_task_service import get_close_tasks

def check_close_readiness(
    company_code: str,
    fiscal_year: int,
    period_number: int,
) -> dict[str, Any]:
    """
    Assess whether a Company Code is ready for month-end close.

    """
   
    company_code = company_code.upper()

    checks: list[dict[str, Any]] = []

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

    checklist_passed = len(incomplete_tasks) == 0

    checks.append(
        {
            "check": "CLOSE_CHECKLIST_COMPLETE",
            "passed": checklist_passed,
            "message": (
                "All month-end close tasks are completed."
                if checklist_passed
                else f"{len(incomplete_tasks)} close task(s) remain incomplete."
            ),
        }
    )

    # --------------------------------------------------
    # CHECK 1 - POSTING PERIOD EXISTS AND IS OPEN
    # --------------------------------------------------

    posting_period = find_posting_period(
        company_code,
        fiscal_year,
        period_number,
    )

    period_open = (
        posting_period is not None
        and posting_period["status"].upper() == "OPEN"
    )

    checks.append(
        {
            "check": "POSTING_PERIOD_OPEN",
            "passed": period_open,
            "message": (
                "Posting period is open."
                if period_open
                else "Posting period is not open or is not configured."
            ),
        }
    )

    # --------------------------------------------------
    # CHECK 2 - TRIAL BALANCE BALANCES
    # --------------------------------------------------

    trial_balance = calculate_trial_balance()

    trial_balance_balanced = bool(
        trial_balance.get("balances", False)
    )

    checks.append(
        {
            "check": "TRIAL_BALANCE_BALANCED",
            "passed": trial_balance_balanced,
            "message": (
                "Trial Balance is balanced."
                if trial_balance_balanced
                else "Trial Balance is not balanced."
            ),
        }
    )

    # --------------------------------------------------
    # CHECK 3 - AP EXCEPTIONS
    # --------------------------------------------------

    invoices = get_all_vendor_invoices()

    company_invoices = [
        invoice
        for invoice in invoices
        if invoice["company_code"] == company_code
    ]

    ap_exceptions = [
        invoice
        for invoice in company_invoices
        if (
            invoice.get("status") in {
                "BLOCKED",
                "UNMATCHED",
                "DUPLICATE",
                "UNPOSTED",
                "REJECTED",
            }
            or invoice.get("payment_block") is True
        )
    ]

    no_ap_exceptions = len(ap_exceptions) == 0

    checks.append(
        {
            "check": "AP_EXCEPTIONS",
            "passed": no_ap_exceptions,
            "message": (
                "No unresolved AP exceptions remain."
                if no_ap_exceptions
                else (
                    f"{len(ap_exceptions)} unresolved AP "
                    "exception(s) require review."
                )
            ),
        }
    )

    # --------------------------------------------------
    # CHECK 4 - JOURNAL ENTRIES AVAILABLE
    # --------------------------------------------------

    journals = get_company_journal_entries(
        company_code
    )

    journals_available = len(journals) > 0

    checks.append(
        {
            "check": "JOURNAL_ACTIVITY",
            "passed": journals_available,
            "message": (
                "Journal activity exists for the Company Code."
                if journals_available
                else "No journal activity exists for the Company Code."
            ),
        }
    )

    blockers = [
        check
        for check in checks
        if not check["passed"]
    ]

    readiness_status = (
        "READY"
        if len(blockers) == 0
        else "NOT_READY"
    )

    return {
        "company_code": company_code,
        "fiscal_year": fiscal_year,
        "period_number": period_number,
        "status": readiness_status,
        "checks": checks,
        "blockers": blockers,
    }