from datetime import date
from typing import Any

from mock_sap.posting_engine import create_journal_entry
from mock_sap.vendor_invoices_data import get_vendor_invoice


VENDOR_PAYMENTS: list[dict[str, Any]] = []


def generate_payment_number() -> str:
    """
    Generate the next mock SAP vendor payment number.
    """
    if not VENDOR_PAYMENTS:
        return "700000001"

    existing_numbers = [
        int(payment["payment_number"])
        for payment in VENDOR_PAYMENTS
    ]

    return str(max(existing_numbers) + 1)


def get_all_vendor_payments() -> list[dict]:
    """
    Return all vendor payments.
    """
    return VENDOR_PAYMENTS


def get_vendor_payment(
    payment_number: str,
) -> dict | None:
    """
    Return one vendor payment by payment number.
    """
    for payment in VENDOR_PAYMENTS:
        if payment["payment_number"] == payment_number:
            return payment

    return None


def get_vendor_payments_for_vendor(
    vendor_id: str,
) -> list[dict]:
    """
    Return all payments made to one vendor.
    """
    vendor_id = vendor_id.upper()

    return [
        payment
        for payment in VENDOR_PAYMENTS
        if payment["vendor_id"] == vendor_id
    ]


def get_vendor_payments_for_invoice(
    invoice_number: str,
) -> list[dict]:
    """
    Return all payments linked to one vendor invoice.
    """
    return [
        payment
        for payment in VENDOR_PAYMENTS
        if payment["invoice_number"] == invoice_number
    ]


def post_vendor_payment(
    invoice_number: str,
    payment_method: str = "BANK_TRANSFER",
    bank_gl_account: str = "100000",
    payment_date: str | None = None,
) -> dict:
    """
    Pay one open vendor invoice and create the accounting journal entry.
    """
    invoice = get_vendor_invoice(invoice_number)

    if invoice is None:
        raise ValueError(
            f"Vendor invoice '{invoice_number}' was not found."
        )

    if invoice["status"] != "OPEN":
        raise ValueError(
            f"Vendor invoice '{invoice_number}' is not open."
        )

    if payment_date is None:
        payment_date = date.today().isoformat()

    journal_entry = create_journal_entry(
        company_code=invoice["company_code"],
        debit_gl_account="200000",
        credit_gl_account=bank_gl_account,
        amount=invoice["amount"],
        reference=f"Vendor payment for invoice {invoice_number}",
        document_type="KZ",
        currency=invoice["currency"],
        posting_date=payment_date,
    )

    payment = {
        "payment_number": generate_payment_number(),
        "vendor_id": invoice["vendor_id"],
        "vendor_name": invoice["vendor_name"],
        "invoice_number": invoice["invoice_number"],
        "company_code": invoice["company_code"],
        "payment_date": payment_date,
        "amount": float(invoice["amount"]),
        "currency": invoice["currency"],
        "payment_method": payment_method.upper(),
        "bank_gl_account": bank_gl_account,
        "journal_document_number": journal_entry["document_number"],
        "status": "POSTED",
    }

    VENDOR_PAYMENTS.append(payment)
    invoice["status"] = "PAID"

    return {
        "payment": payment,
        "journal_entry": journal_entry,
    }