from mock_sap.journal_entries_data import JOURNAL_ENTRIES
from mock_sap.posting_engine import create_journal_entry


def run_module_13_tests() -> None:
    """
    Acceptance tests for Module 13 - Posting Period Control.
    """

    starting_count = len(JOURNAL_ENTRIES)

    print("=" * 60)
    print("MODULE 13 - POSTING PERIOD CONTROL ACCEPTANCE TEST")
    print("=" * 60)

    # -----------------------------------------------------
    # TEST 1 - JULY MUST BE BLOCKED
    # -----------------------------------------------------

    print("\nTEST 1: July 2026 should be CLOSED")

    try:
        create_journal_entry(
            company_code="UK01",
            debit_gl_account="500000",
            credit_gl_account="100000",
            amount=100,
            reference="Module 13 July Closed Period Test",
            posting_date="2026-07-15",
        )

        print("FAIL: July posting was incorrectly allowed.")

    except ValueError as error:
        print(f"PASS: July posting rejected -> {error}")

    after_july_count = len(JOURNAL_ENTRIES)

    if after_july_count == starting_count:
        print("PASS: No invalid July journal was stored.")
    else:
        print("FAIL: A July journal was stored.")

    # -----------------------------------------------------
    # TEST 2 - AUGUST MUST BE ALLOWED
    # -----------------------------------------------------

    print("\nTEST 2: August 2026 should be OPEN")

    try:
        august_journal = create_journal_entry(
            company_code="UK01",
            debit_gl_account="500000",
            credit_gl_account="100000",
            amount=100,
            reference="Module 13 August Open Period Test",
            posting_date="2026-08-10",
        )

        print("PASS: August posting accepted.")
        print(
            "Journal document:",
            august_journal["document_number"],
        )

    except ValueError as error:
        print(f"FAIL: August posting rejected -> {error}")
        return

    # -----------------------------------------------------
    # TEST 3 - JOURNAL MUST BE BALANCED
    # -----------------------------------------------------

    print("\nTEST 3: Journal must be balanced")

    total_debit = sum(
        float(line["debit"])
        for line in august_journal["line_items"]
    )

    total_credit = sum(
        float(line["credit"])
        for line in august_journal["line_items"]
    )

    if total_debit == total_credit:
        print(
            f"PASS: Debit {total_debit:.2f} "
            f"= Credit {total_credit:.2f}"
        )
    else:
        print(
            f"FAIL: Debit {total_debit:.2f} "
            f"!= Credit {total_credit:.2f}"
        )

    # -----------------------------------------------------
    # TEST 4 - AUGUST JOURNAL MUST BE STORED
    # -----------------------------------------------------

    print("\nTEST 4: August journal must be stored")

    stored = any(
        entry["document_number"]
        == august_journal["document_number"]
        for entry in JOURNAL_ENTRIES
    )

    if stored:
        print("PASS: August journal stored successfully.")
    else:
        print("FAIL: August journal was not stored.")

    print("\n" + "=" * 60)
    print("MODULE 13 ACCEPTANCE TEST FINISHED")
    print("=" * 60)


if __name__ == "__main__":
    run_module_13_tests()