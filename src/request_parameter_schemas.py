from dataclasses import dataclass


@dataclass(frozen=True)
class GLBalanceParameters:
    """
    Structured parameters for General Ledger balance requests.
    """

    company_code: str


@dataclass(frozen=True)
class VendorInvoiceParameters:
    """
    Structured parameters for vendor invoice requests.
    """

    company_code: str


@dataclass(frozen=True)
class ClosePeriodParameters:
    """
    Structured parameters for accounting-period close requests.
    """

    company_code: str
    fiscal_year: int
    period_number: int
    approval_request_id: str