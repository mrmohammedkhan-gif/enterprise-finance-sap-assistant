JOURNAL_ENTRIES = [
    {
        "document_number": "900000001",
        "company_code": "UK01",
        "posting_date": "2026-07-28",
        "document_type": "KR",
        "currency": "GBP",
        "reference": "Office Supplies Invoice",
        "line_items": [
            {
                "line": 1,
                "gl_account": "500000",
                "description": "Office Expenses",
                "debit": 500.00,
                "credit": 0.00,
            },
            {
                "line": 2,
                "gl_account": "200000",
                "description": "Accounts Payable",
                "debit": 0.00,
                "credit": 500.00,
            },
        ],
    },
    {
        "document_number": "900000002",
        "company_code": "UK01",
        "posting_date": "2026-07-29",
        "document_type": "KZ",
        "currency": "GBP",
        "reference": "Vendor Payment",
        "line_items": [
            {
                "line": 1,
                "gl_account": "200000",
                "description": "Accounts Payable",
                "debit": 500.00,
                "credit": 0.00,
            },
            {
                "line": 2,
                "gl_account": "100000",
                "description": "Bank",
                "debit": 0.00,
                "credit": 500.00,
            },
        ],
    },
]


def get_all_journal_entries():
    return JOURNAL_ENTRIES


def get_journal_entry(document_number):
    for entry in JOURNAL_ENTRIES:
        if entry["document_number"] == document_number:
            return entry
    return None


def get_company_journal_entries(company_code):
    company_code = company_code.upper()

    return [
        entry
        for entry in JOURNAL_ENTRIES
        if entry["company_code"] == company_code
    ]