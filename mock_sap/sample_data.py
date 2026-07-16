VENDORS = [
    {
        "vendor_id": "V1001",
        "name": "Alpha Office Supplies",
        "country": "UK",
        "payment_terms_days": 30,
        "status": "ACTIVE",
    },
    {
        "vendor_id": "V1002",
        "name": "Global Technology Ltd",
        "country": "UK",
        "payment_terms_days": 45,
        "status": "ACTIVE",
    },
]

INVOICES = [
    {
        "invoice_id": "INV-1001",
        "vendor_id": "V1001",
        "amount": 12500.00,
        "currency": "GBP",
        "invoice_date": "2026-05-01",
        "due_date": "2026-05-31",
        "status": "OVERDUE",
        "days_overdue": 41,
    },
    {
        "invoice_id": "INV-1002",
        "vendor_id": "V1002",
        "amount": 7800.00,
        "currency": "GBP",
        "invoice_date": "2026-06-15",
        "due_date": "2026-07-30",
        "status": "OPEN",
        "days_overdue": 0,
    },
    {
        "invoice_id": "INV-1003",
        "vendor_id": "V1002",
        "amount": 24500.00,
        "currency": "GBP",
        "invoice_date": "2026-04-20",
        "due_date": "2026-06-04",
        "status": "OVERDUE",
        "days_overdue": 37,
    },
]

GL_BALANCES = [
    {
        "company_code": "UK01",
        "gl_account": "400000",
        "description": "Sales Revenue",
        "period": "2026-06",
        "balance": 425000.00,
        "currency": "GBP",
    },
    {
        "company_code": "UK01",
        "gl_account": "610000",
        "description": "Operating Expenses",
        "period": "2026-06",
        "balance": 172000.00,
        "currency": "GBP",
    },
]