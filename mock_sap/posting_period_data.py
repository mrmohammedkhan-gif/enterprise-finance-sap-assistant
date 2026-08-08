from datetime import datetime
from typing import Optional, TypedDict


class PostingPeriod(TypedDict):
    company_code: str
    fiscal_year: int
    period_number: int
    status: str
    opened_at: Optional[datetime]
    closed_at: Optional[datetime]


POSTING_PERIODS: list[PostingPeriod] = [
    {
        "company_code": "UK01",
        "fiscal_year": 2026,
        "period_number": 7,
        "status": "CLOSED",
        "opened_at": datetime(2026, 7, 1, 9, 0),
        "closed_at": datetime(2026, 8, 5, 17, 0),
    },
    {
        "company_code": "UK01",
        "fiscal_year": 2026,
        "period_number": 8,
        "status": "OPEN",
        "opened_at": datetime(2026, 8, 1, 9, 0),
        "closed_at": None,
    },

]
