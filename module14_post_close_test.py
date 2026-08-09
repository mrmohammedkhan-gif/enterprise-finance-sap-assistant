from src.month_end_close_service import execute_period_close
from mock_sap.posting_engine import create_journal_entry


def run_test() -> None:
    print("MODULE 14 - POST-CLOSE POSTING CONTROL TEST")

    result = execute_period_close(
        company_code="UK01",
        fiscal_year=2026,
        period_number=8,
        approved_by="Finance Manager",
    )

    print("PERIOD CLOSE STATUS:", result["status"])

    try:
        create_journal_entry(
            company_code="UK01",
            debit_gl_account="500000",
            credit_gl_account="100000",
            amount=100,
            reference="Post-close August test",
            posting_date="2026-08-20",
        )

        print("FAIL: August posting was allowed after close.")

    except ValueError as error:
        print(
            "PASS: August posting rejected after close ->",
            error,
        )


if __name__ == "__main__":
    run_test()