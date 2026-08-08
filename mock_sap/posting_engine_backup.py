from datetime import date
from typing import Any

from src.posting_period_service import validate_posting_period


def create_journal_entry(
    company_code: str,
    debit_gl_account: str,
    credit_gl_account: str,
    amount: float | int | str,
    reference: str,
    document_type: str = "SA",
    currency: str | None = None,
    posting_date: str | None = None,
) -> dict[str, Any]:
    """
    Create and store a balanced two-line journal entry.
    """

    company = validate_company_code(company_code)

    debit_account = validate_gl_account(debit_gl_account)
    credit_account = validate_gl_account(credit_gl_account)

    if debit_gl_account == credit_gl_account:
        raise ValueError(
            "Debit and credit G/L accounts must be different."
        )

    validated_amount = validate_amount(amount)

    if currency is None:
        currency = company["local_currency"]

    if posting_date is None:
        posting_date = date.today().isoformat()

    try:
        parsed_posting_date = date.fromisoformat(posting_date)
    except ValueError as error:
        raise ValueError(
            "Posting date must use YYYY-MM-DD format."
        ) from error

    validate_posting_period(
        company_code=company["company_code"],
        fiscal_year=parsed_posting_date.year,
        period_number=parsed_posting_date.month,
    )

    document_number = generate_document_number()

    journal_entry = {
        "document_number": document_number,
        "company_code": company["company_code"],
        "posting_date": posting_date,
        "document_type": document_type.upper(),
        "currency": currency.upper(),
        "reference": reference.strip(),
        "line_items": [
            {
                "line": 1,
                "gl_account": debit_account["gl_account"],
                "description": debit_account["description"],
                "debit": validated_amount,
                "credit": 0.0,
            },
            {
                "line": 2,
                "gl_account": credit_account["gl_account"],
                "description": credit_account["description"],
                "debit": 0.0,
                "credit": validated_amount,
            },
        ],
    }

    JOURNAL_ENTRIES.append(journal_entry)

    return journal_entry