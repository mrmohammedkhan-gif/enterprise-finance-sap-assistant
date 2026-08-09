from datetime import datetime
from typing import Optional

from mock_sap.posting_period_data import (
    POSTING_PERIODS,
    PostingPeriod,
)
from src.close_persistence import (
    get_persisted_posting_period,
    save_posting_period,
)


def validate_period_number(
    period_number: int,
) -> None:
    """
    Validate that the accounting period is between 1 and 12.
    """
    if period_number < 1 or period_number > 12:
        raise ValueError(
            "Period number must be between 1 and 12. "
            f"Received: {period_number}."
        )


def find_posting_period(
    company_code: str,
    fiscal_year: int,
    period_number: int,
) -> Optional[PostingPeriod]:
    """
    Find one posting period.

    Persistent database state takes priority over
    the original in-memory configuration.
    """
    validate_period_number(period_number)

    company_code = company_code.upper()

    persisted_period = get_persisted_posting_period(
        company_code,
        fiscal_year,
        period_number,
    )

    if persisted_period is not None:
        return persisted_period

    for posting_period in POSTING_PERIODS:
        if (
            posting_period["company_code"] == company_code
            and posting_period["fiscal_year"] == fiscal_year
            and posting_period["period_number"] == period_number
        ):
            return posting_period

    return None

def open_period(
    company_code: str,
    fiscal_year: int,
    period_number: int,
) -> PostingPeriod:
    """
    Open an existing posting period or create it if needed.
    """
    validate_period_number(period_number)

    company_code = company_code.upper()

    posting_period = find_posting_period(
        company_code,
        fiscal_year,
        period_number,
    )

    if posting_period is None:
        posting_period = {
            "company_code": company_code,
            "fiscal_year": fiscal_year,
            "period_number": period_number,
            "status": "OPEN",
            "opened_at": datetime.now(),
            "closed_at": None,
        }

        POSTING_PERIODS.append(posting_period)

    else:
        posting_period["status"] = "OPEN"
        posting_period["opened_at"] = datetime.now()
        posting_period["closed_at"] = None

    save_posting_period(
        company_code=posting_period["company_code"],
        fiscal_year=posting_period["fiscal_year"],
        period_number=posting_period["period_number"],
        status=posting_period["status"],
        opened_at=(
            posting_period["opened_at"].isoformat()
            if isinstance(posting_period["opened_at"], datetime)
            else posting_period["opened_at"]
        ),
        closed_at=(
            posting_period["closed_at"].isoformat()
            if isinstance(posting_period["closed_at"], datetime)
            else posting_period["closed_at"]
        ),
    )

    return posting_period

def close_period(
    company_code: str,
    fiscal_year: int,
    period_number: int,
) -> PostingPeriod:
    """
    Close an existing posting period and persist the change.
    """
    validate_period_number(period_number)

    company_code = company_code.upper()

    posting_period = find_posting_period(
        company_code,
        fiscal_year,
        period_number,
    )

    if posting_period is None:
        raise ValueError(
            f"Posting period {period_number:02d}/{fiscal_year} "
            f"does not exist for Company Code {company_code}."
        )

    posting_period["status"] = "CLOSED"
    posting_period["closed_at"] = datetime.now()

    save_posting_period(
        company_code=posting_period["company_code"],
        fiscal_year=posting_period["fiscal_year"],
        period_number=posting_period["period_number"],
        status=posting_period["status"],
        opened_at=(
            posting_period["opened_at"].isoformat()
            if isinstance(posting_period["opened_at"], datetime)
            else posting_period["opened_at"]
        ),
        closed_at=(
            posting_period["closed_at"].isoformat()
            if isinstance(posting_period["closed_at"], datetime)
            else posting_period["closed_at"]
        ),
    )

    return posting_period
    if posting_period is None:
        raise ValueError(
            f"Posting period {period_number:02d}/{fiscal_year} "
            f"does not exist for Company Code {company_code}."
        )

    posting_period["status"] = "CLOSED"
    posting_period["closed_at"] = datetime.now()

    return posting_period


def is_period_open(
    company_code: str,
    fiscal_year: int,
    period_number: int,
) -> bool:
    """
    Return True only when the posting period exists
    and its status is OPEN.
    """
    posting_period = find_posting_period(
        company_code,
        fiscal_year,
        period_number,
    )

    if posting_period is None:
        return False

    return posting_period["status"].upper() == "OPEN"


def validate_posting_period(
    company_code: str,
    fiscal_year: int,
    period_number: int,
) -> None:
    """
    Validate that the selected posting period exists
    and is open for accounting postings.
    """
    posting_period = find_posting_period(
        company_code,
        fiscal_year,
        period_number,
    )

    if posting_period is None:
        raise ValueError(
            f"Posting period {period_number:02d}/{fiscal_year} "
            f"is not configured for Company Code {company_code}."
        )

    if posting_period["status"].upper() != "OPEN":
        raise ValueError(
            f"Posting period {period_number:02d}/{fiscal_year} "
            f"is closed for Company Code {company_code}."
        )