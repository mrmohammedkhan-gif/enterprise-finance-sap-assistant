from datetime import date


VENDOR_INVOICES = [
    {
        "invoice_number": "510000001",
        "vendor_id": "V1001",
        "vendor_name": "Office Supplies Ltd",
        "company_code": "UK01",
        "invoice_date": "2026-07-01",
        "due_date": "2026-07-31",
        "amount": 750.00,
        "currency": "GBP",
        "status": "OPEN",
    },
    {
        "invoice_number": "510000002",
        "vendor_id": "V1002",
        "vendor_name": "Global Technology Ltd",
        "company_code": "UK01",
        "invoice_date": "2026-07-15",
        "due_date": "2026-08-14",
        "amount": 1200.00,
        "currency": "GBP",
        "status": "OPEN",
    },
    {
        "invoice_number": "510000003",
        "vendor_id": "V1001",
        "vendor_name": "Office Supplies Ltd",
        "company_code": "UK01",
        "invoice_date": "2026-06-01",
        "due_date": "2026-07-01",
        "amount": 500.00,
        "currency": "GBP",
        "status": "PAID",
    },
]


def get_all_vendor_invoices() -> list[dict]:
    """
    Return all vendor invoices.
    """
    return VENDOR_INVOICES


def get_vendor_invoice(invoice_number: str) -> dict | None:
    """
    Return one vendor invoice by invoice number.
    """
    for invoice in VENDOR_INVOICES:
        if invoice["invoice_number"] == invoice_number:
            return invoice

    return None


def get_open_vendor_invoices(
    company_code: str | None = None,
) -> list[dict]:
    """
    Return all open vendor invoices.

    Optionally filter by Company Code.
    """
    invoices = []

    for invoice in VENDOR_INVOICES:
        if invoice["status"] != "OPEN":
            continue

        if (
            company_code is not None
            and invoice["company_code"] != company_code.upper()
        ):
            continue

        invoices.append(invoice)

    return invoices


def get_overdue_vendor_invoices(
    as_of_date: str | None = None,
    company_code: str | None = None,
) -> list[dict]:
    """
    Return open invoices whose due date is before the reporting date.

    Optionally filter by Company Code.
    """
    reporting_date = (
        date.fromisoformat(as_of_date)
        if as_of_date
        else date.today()
    )

    overdue_invoices = []

    for invoice in get_open_vendor_invoices(company_code):
        due_date = date.fromisoformat(invoice["due_date"])

        if due_date < reporting_date:
            overdue_invoices.append(invoice)

    return overdue_invoices


def get_vendor_open_balance(vendor_id: str) -> dict:
    """
    Calculate the open Accounts Payable balance for one vendor.
    """
    vendor_id = vendor_id.upper()

    vendor_invoices = [
        invoice
        for invoice in get_open_vendor_invoices()
        if invoice["vendor_id"] == vendor_id
    ]

    total_open_amount = sum(
        invoice["amount"]
        for invoice in vendor_invoices
    )

    return {
        "vendor_id": vendor_id,
        "open_invoice_count": len(vendor_invoices),
        "total_open_amount": total_open_amount,
        "invoices": vendor_invoices,
    }