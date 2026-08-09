
from mock_sap.trial_balance_data import calculate_trial_balance

from mock_sap.posting_period_data import POSTING_PERIODS

from pydantic import BaseModel

from mock_sap.posting_engine import create_journal_entry

from src.close_readiness_service import check_close_readiness

from src.close_persistence import get_close_audit_history

from src.month_end_close_service import execute_period_close

from fastapi import FastAPI, HTTPException

from fastapi import HTTPException



from mock_sap.tax_codes_data import (
    get_all_tax_codes,
    get_tax_code,
    get_tax_codes_for_country,
    get_tax_codes_for_region,
    get_compound_tax_codes,
)

from mock_sap.tax_engine import (
    calculate_single_tax,
    calculate_compound_tax,
    build_ap_tax_journal_lines,
    build_ar_tax_journal_lines,
)

from mock_sap.vendor_invoices_data import (
    get_all_vendor_invoices,
    get_vendor_invoice,
    get_open_vendor_invoices,
    get_overdue_vendor_invoices,
    get_vendor_open_balance,
)

from mock_sap.vendor_payments_data import (
    get_all_vendor_payments,
    get_vendor_payment,
    get_vendor_payments_for_vendor,
    get_vendor_payments_for_invoice,
    post_vendor_payment,
)



from mock_sap.financial_statements_data import (
    calculate_financial_statements,
    get_balance_sheet,
    get_profit_and_loss,
)


from mock_sap.journal_entries_data import (
    get_all_journal_entries,
    get_journal_entry,
    get_company_journal_entries,
)



from mock_sap.gl_account_data import (
    get_all_gl_accounts,
    get_gl_account_by_id,
    get_gl_accounts_for_chart,
)



from mock_sap.chart_of_accounts_data import (
    get_all_charts_of_accounts,
    get_chart_of_accounts_by_id,
    get_charts_for_company_code,
)


from fastapi import FastAPI, HTTPException

from mock_sap.ap_invoice_data import AP_INVOICES
from mock_sap.business_partner_data import BUSINESS_PARTNERS
from mock_sap.purchase_order_data import PURCHASE_ORDERS
from mock_sap.sample_data import GL_BALANCES, INVOICES, VENDORS


app = FastAPI(
    title="Mock SAP Finance API",
    description=(
        "Mock SAP finance endpoints for the "
        "Enterprise Finance AI Assistant."
    ),
    version="1.0.0",
)

class JournalEntryRequest(BaseModel):
    """
    Data required to create a two-line journal entry.
    """

    company_code: str
    debit_gl_account: str
    credit_gl_account: str
    amount: float
    reference: str
    document_type: str = "SA"
    currency: str | None = None
    posting_date: str | None = None


class VendorPaymentRequest(BaseModel):
    """
    Data required to pay one vendor invoice.
    """

    invoice_number: str
    payment_method: str = "BANK_TRANSFER"
    bank_gl_account: str = "100000"
    payment_date: str | None = None

class SingleTaxRequest(BaseModel):
    net_amount: float
    tax_code: str
    transaction_date: str | None = None


class CompoundTaxRequest(BaseModel):
    net_amount: float
    compound_group: str
    transaction_date: str | None = None


class APTaxJournalRequest(BaseModel):
    net_amount: float
    expense_gl_account: str
    accounts_payable_gl_account: str
    tax_code: str
    transaction_date: str | None = None


class ARTaxJournalRequest(BaseModel):
    net_amount: float
    revenue_gl_account: str
    accounts_receivable_gl_account: str
    tax_code: str
    transaction_date: str | None = None


@app.get("/")
def root() -> dict:
    return {
        "service": "Mock SAP Finance API",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict:
    return {"status": "healthy"}




# ---------------------------------------------------------
# SAP ORGANISATION
# ---------------------------------------------------------


@app.get("/company-codes")
def list_company_codes() -> list[dict]:
    return COMPANY_CODES


@app.get("/company-codes/{company_code}")
def get_company_code(company_code: str) -> dict:
    company = next(
        (
            item
            for item in COMPANY_CODES
            if item["company_code"].lower()
            == company_code.lower()
        ),
        None,
    )

    if company is None:
        raise HTTPException(
            status_code=404,
            detail=f"Company code {company_code} was not found.",
        )

    return company


@app.get("/posting-periods/{company_code}")
def get_posting_period(
    company_code: str,
    fiscal_year: int,
    period: int,
) -> dict:
    posting_period = next(
        (
            item
            for item in POSTING_PERIODS
            if item["company_code"].lower()
            == company_code.lower()
            and item["fiscal_year"] == fiscal_year
            and item["period_number"] == period
        ),
        None,
    )

    if posting_period is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Posting period {period}/{fiscal_year} "
                f"was not found for {company_code}."
            ),
        )

    return posting_period


# ---------------------------------------------------------
# SAP BUSINESS PARTNERS
# ---------------------------------------------------------


@app.get("/business-partners/blocked")
def list_blocked_business_partners() -> list[dict]:
    return [
        partner
        for partner in BUSINESS_PARTNERS
        if partner["payment_block"] is True
    ]


@app.get("/business-partners")
def list_business_partners(
    partner_type: str | None = None,
    company_code: str | None = None,
    status: str | None = None,
) -> list[dict]:
    results = BUSINESS_PARTNERS

    if partner_type:
        results = [
            partner
            for partner in results
            if partner["partner_type"].lower()
            == partner_type.lower()
        ]

    if company_code:
        results = [
            partner
            for partner in results
            if partner["company_code"].lower()
            == company_code.lower()
        ]

    if status:
        results = [
            partner
            for partner in results
            if partner["status"].lower()
            == status.lower()
        ]

    return results


@app.get("/business-partners/{business_partner}")
def get_business_partner(
    business_partner: str,
) -> dict:
    partner = next(
        (
            item
            for item in BUSINESS_PARTNERS
            if item["business_partner"].lower()
            == business_partner.lower()
        ),
        None,
    )

    if partner is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Business partner {business_partner} "
                "was not found."
            ),
        )

    return partner


# ---------------------------------------------------------
# SAP PURCHASE ORDERS
# ---------------------------------------------------------


@app.get("/purchase-orders/open")
def list_open_purchase_orders() -> list[dict]:
    return [
        purchase_order
        for purchase_order in PURCHASE_ORDERS
        if purchase_order["po_status"] == "OPEN"
    ]


@app.get("/purchase-orders")
def list_purchase_orders(
    company_code: str | None = None,
    business_partner: str | None = None,
    approval_status: str | None = None,
    po_status: str | None = None,
) -> list[dict]:
    results = PURCHASE_ORDERS

    if company_code:
        results = [
            purchase_order
            for purchase_order in results
            if purchase_order["company_code"].lower()
            == company_code.lower()
        ]

    if business_partner:
        results = [
            purchase_order
            for purchase_order in results
            if purchase_order["business_partner"].lower()
            == business_partner.lower()
        ]

    if approval_status:
        results = [
            purchase_order
            for purchase_order in results
            if purchase_order["approval_status"].lower()
            == approval_status.lower()
        ]

    if po_status:
        results = [
            purchase_order
            for purchase_order in results
            if purchase_order["po_status"].lower()
            == po_status.lower()
        ]

    return results


@app.get("/purchase-orders/{purchase_order}")
def get_purchase_order(
    purchase_order: str,
) -> dict:
    result = next(
        (
            item
            for item in PURCHASE_ORDERS
            if item["purchase_order"].lower()
            == purchase_order.lower()
        ),
        None,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Purchase order {purchase_order} "
                "was not found."
            ),
        )

    return result


# ---------------------------------------------------------
# SAP ACCOUNTS PAYABLE
# ---------------------------------------------------------


@app.get("/ap-invoices/blocked")
def list_blocked_ap_invoices() -> list[dict]:
    return [
        invoice
        for invoice in AP_INVOICES
        if invoice["payment_block"] is True
        or invoice["invoice_status"] == "BLOCKED"
    ]


@app.get("/ap-invoices/duplicates")
def list_duplicate_ap_invoices() -> list[dict]:
    return [
        invoice
        for invoice in AP_INVOICES
        if invoice["duplicate_check_status"] == "DUPLICATE"
    ]


@app.get("/ap-invoices/parked")
def list_parked_ap_invoices() -> list[dict]:
    return [
        invoice
        for invoice in AP_INVOICES
        if invoice["invoice_status"] == "PARKED"
    ]


@app.get("/ap-invoices")
def list_ap_invoices(
    company_code: str | None = None,
    business_partner: str | None = None,
    invoice_status: str | None = None,
    payment_status: str | None = None,
    matching_status: str | None = None,
) -> list[dict]:
    results = AP_INVOICES

    if company_code:
        results = [
            invoice
            for invoice in results
            if invoice["company_code"].lower()
            == company_code.lower()
        ]

    if business_partner:
        results = [
            invoice
            for invoice in results
            if invoice["business_partner"].lower()
            == business_partner.lower()
        ]

    if invoice_status:
        results = [
            invoice
            for invoice in results
            if invoice["invoice_status"].lower()
            == invoice_status.lower()
        ]

    if payment_status:
        results = [
            invoice
            for invoice in results
            if invoice["payment_status"].lower()
            == payment_status.lower()
        ]

    if matching_status:
        results = [
            invoice
            for invoice in results
            if invoice["matching_status"].lower()
            == matching_status.lower()
        ]

    return results


@app.get("/ap-invoices/{invoice_document}")
def get_ap_invoice(
    invoice_document: str,
) -> dict:
    invoice = next(
        (
            item
            for item in AP_INVOICES
            if item["invoice_document"].lower()
            == invoice_document.lower()
        ),
        None,
    )

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"AP invoice {invoice_document} "
                "was not found."
            ),
        )

    return invoice


# ---------------------------------------------------------
# SAP VENDORS
# ---------------------------------------------------------


@app.get("/vendors")
def list_vendors() -> list[dict]:
    return VENDORS


@app.get("/vendors/{vendor_id}")
def get_vendor(vendor_id: str) -> dict:
    vendor = next(
        (
            item
            for item in VENDORS
            if item["vendor_id"].lower()
            == vendor_id.lower()
        ),
        None,
    )

    if vendor is None:
        raise HTTPException(
            status_code=404,
            detail=f"Vendor {vendor_id} was not found.",
        )

    return vendor


# ---------------------------------------------------------
# SAP LEGACY INVOICES
# ---------------------------------------------------------


@app.get("/invoices")
def list_invoices(
    status: str | None = None,
    minimum_amount: float | None = None,
) -> list[dict]:
    results = INVOICES

    if status:
        results = [
            invoice
            for invoice in results
            if invoice["status"].lower() == status.lower()
        ]

    if minimum_amount is not None:
        results = [
            invoice
            for invoice in results
            if invoice["amount"] >= minimum_amount
        ]

    return results


@app.get("/invoices/overdue")
def list_overdue_invoices(
    minimum_days: int = 1,
) -> list[dict]:
    return [
        invoice
        for invoice in INVOICES
        if invoice["status"] == "OVERDUE"
        and invoice["days_overdue"] >= minimum_days
    ]


# ---------------------------------------------------------
# SAP GENERAL LEDGER
# ---------------------------------------------------------


@app.get("/gl-balances")
def list_gl_balances(
    company_code: str | None = None,
) -> list[dict]:
    if company_code is None:
        return GL_BALANCES

    return [
        balance
        for balance in GL_BALANCES
        if balance["company_code"].lower()
        == company_code.lower()
    ]


@app.get("/company-codes")
def list_company_codes():
    """
    Return all configured Company Codes.
    """
    return get_all_company_codes()


@app.get("/company-codes/{company_code}")
def get_company_code(company_code: str):
    """
    Return details for one Company Code.
    """
    company = get_company_code_by_id(company_code)

    if company is None:
        return {
            "error": f"Company Code '{company_code}' was not found."
        }

    return company

@app.get("/chart-of-accounts")
def list_charts_of_accounts():
    return get_all_charts_of_accounts()


@app.get("/chart-of-accounts/{chart_id}")
def get_chart_of_accounts(chart_id: str):
    chart = get_chart_of_accounts_by_id(chart_id)

    if chart is None:
        return {
            "error": f"Chart of Accounts '{chart_id}' was not found."
        }

    return chart


@app.get("/company-codes/{company_code}/chart-of-accounts")
def get_company_chart(company_code: str):
    return get_charts_for_company_code(company_code)

@app.get("/gl-accounts")
def list_gl_accounts():
    """Return all configured General Ledger accounts."""
    return get_all_gl_accounts()


@app.get("/gl-accounts/{gl_account}")
def get_gl_account(gl_account: str):
    """Return details for one General Ledger account."""
    account = get_gl_account_by_id(gl_account)

    if account is None:
        return {
            "error": f"G/L Account '{gl_account}' was not found."
        }

    return account


@app.get("/chart-of-accounts/{chart_of_accounts}/gl-accounts")
def get_chart_gl_accounts(chart_of_accounts: str):
    """Return all G/L accounts assigned to one Chart of Accounts."""
    return get_gl_accounts_for_chart(chart_of_accounts)


@app.get("/journal-entries")
def list_journal_entries():
    """Return all journal entries."""
    return get_all_journal_entries()


@app.get("/journal-entries/{document_number}")
def get_journal_entry_by_number(document_number: str):
    """Return one journal entry by document number."""
    entry = get_journal_entry(document_number)

    if entry is None:
        return {
            "error": f"Journal Entry '{document_number}' was not found."
        }

    return entry


@app.get("/company-codes/{company_code}/journal-entries")
def list_company_journal_entries(company_code: str):
    """Return journal entries for one Company Code."""
    return get_company_journal_entries(company_code)

@app.get("/trial-balance")
def get_trial_balance():
    """Return the calculated Trial Balance."""
    return calculate_trial_balance()

@app.get("/financial-statements")
def get_financial_statements():
    """Return the complete Financial Statements report."""
    return calculate_financial_statements()


@app.get("/balance-sheet")
def get_balance_sheet_report():
    """Return the calculated Balance Sheet."""
    return get_balance_sheet()


@app.get("/profit-and-loss")
def get_profit_and_loss_report():
    """Return the calculated Profit and Loss Statement."""
    return get_profit_and_loss()

@app.post("/journal-entries")
def post_journal_entry(request: JournalEntryRequest):
    """
    Validate and create a new balanced journal entry.
    """

    try:
        return create_journal_entry(
            company_code=request.company_code,
            debit_gl_account=request.debit_gl_account,
            credit_gl_account=request.credit_gl_account,
            amount=request.amount,
            reference=request.reference,
            document_type=request.document_type,
            currency=request.currency,
            posting_date=request.posting_date,
        )

    except ValueError as error:
        return {
            "error": str(error)
        }

@app.get("/vendor-invoices")
def list_vendor_invoices():
    """Return all vendor invoices."""
    return get_all_vendor_invoices()


@app.get("/vendor-invoices/open")
def list_open_vendor_invoices(
    company_code: str | None = None,
):
    """Return open vendor invoices."""
    return get_open_vendor_invoices(company_code)


@app.get("/vendor-invoices/overdue")
def list_overdue_vendor_invoices(
    as_of_date: str | None = None,
    company_code: str | None = None,
):
    """Return overdue vendor invoices."""
    return get_overdue_vendor_invoices(
        as_of_date=as_of_date,
        company_code=company_code,
    )


@app.get("/vendor-invoices/{invoice_number}")
def get_vendor_invoice_by_number(invoice_number: str):
    """Return one vendor invoice."""
    invoice = get_vendor_invoice(invoice_number)

    if invoice is None:
        return {
            "error": f"Vendor invoice '{invoice_number}' was not found."
        }

    return invoice


@app.get("/vendors/{vendor_id}/open-balance")
def get_vendor_balance(vendor_id: str):
    """Return one vendor's open invoice balance."""
    return get_vendor_open_balance(vendor_id)

@app.get("/vendor-payments")
def list_vendor_payments():
    """
    Return all vendor payments.
    """
    return get_all_vendor_payments()


@app.get("/vendor-payments/{payment_number}")
def get_vendor_payment_by_number(payment_number: str):
    """
    Return one vendor payment.
    """
    payment = get_vendor_payment(payment_number)

    if payment is None:
        return {
            "error": f"Vendor payment '{payment_number}' was not found."
        }

    return payment


@app.get("/vendors/{vendor_id}/payments")
def list_vendor_payments_for_vendor(vendor_id: str):
    """
    Return all payments for one vendor.
    """
    return get_vendor_payments_for_vendor(vendor_id)


@app.get("/vendor-invoices/{invoice_number}/payments")
def list_vendor_payments_for_invoice(invoice_number: str):
    """
    Return all payments linked to one vendor invoice.
    """
    return get_vendor_payments_for_invoice(invoice_number)


@app.post("/vendor-payments")
def create_vendor_payment(request: VendorPaymentRequest):
    """
    Pay one open vendor invoice.
    """
    try:
        return post_vendor_payment(
            invoice_number=request.invoice_number,
            payment_method=request.payment_method,
            bank_gl_account=request.bank_gl_account,
            payment_date=request.payment_date,
        )

    except ValueError as error:
        return {
            "error": str(error)
        }

@app.get("/tax-codes")
def list_tax_codes():
    """Return all configured tax codes."""
    return get_all_tax_codes()

@app.get("/tax-codes")
def list_tax_codes():
    """Return all configured tax codes."""
    return get_all_tax_codes()


@app.get("/tax-codes/country/{country_code}")
def list_tax_codes_by_country(country_code: str):
    """Return active tax codes for one country."""
    return get_tax_codes_for_country(country_code)


@app.get("/tax-codes/country/{country_code}/region/{region_code}")
def list_tax_codes_by_region(
    country_code: str,
    region_code: str,
):
    """Return active tax codes for one country and region."""
    return get_tax_codes_for_region(
        country_code,
        region_code,
    )


@app.get("/tax-codes/compound/{compound_group}")
def list_compound_tax_codes(compound_group: str):
    """Return tax codes belonging to one compound group."""
    return get_compound_tax_codes(compound_group)


@app.get("/tax-codes/{tax_code}")
def get_tax_code_by_id(tax_code: str):
    """Return one tax code."""
    tax_record = get_tax_code(tax_code)

    if tax_record is None:
        return {
            "error": f"Tax code '{tax_code}' was not found."
        }

    return tax_record


@app.get("/tax-codes/{tax_code}")
def get_tax_code_by_id(tax_code: str):
    """Return one tax code."""
    tax_record = get_tax_code(tax_code)

    if tax_record is None:
        return {
            "error": f"Tax code '{tax_code}' was not found."
        }

    return tax_record


@app.get("/tax-codes/country/{country_code}")
def list_tax_codes_by_country(country_code: str):
    """Return active tax codes for one country."""
    return get_tax_codes_for_country(country_code)


@app.get("/tax-codes/country/{country_code}/region/{region_code}")
def list_tax_codes_by_region(
    country_code: str,
    region_code: str,
):
    """Return active tax codes for one country and region."""
    return get_tax_codes_for_region(
        country_code,
        region_code,
    )


@app.get("/tax-codes/compound/{compound_group}")
def list_compound_tax_codes(compound_group: str):
    """Return tax codes belonging to one compound group."""
    return get_compound_tax_codes(compound_group)


@app.post("/tax/calculate")
def calculate_tax(request: SingleTaxRequest):
    """Calculate one VAT, GST, HST, PST or sales-tax component."""
    try:
        return calculate_single_tax(
            net_amount=request.net_amount,
            tax_code=request.tax_code,
            transaction_date=request.transaction_date,
        )

    except ValueError as error:
        return {
            "error": str(error)
        }


@app.post("/tax/calculate-compound")
def calculate_tax_compound(request: CompoundTaxRequest):
    """Calculate a compound tax group."""
    try:
        return calculate_compound_tax(
            net_amount=request.net_amount,
            compound_group=request.compound_group,
            transaction_date=request.transaction_date,
        )

    except ValueError as error:
        return {
            "error": str(error)
        }


@app.post("/tax/ap-journal-lines")
def calculate_ap_tax_journal(
    request: APTaxJournalRequest,
):
    """Build AP journal lines including tax."""
    try:
        return build_ap_tax_journal_lines(
            net_amount=request.net_amount,
            expense_gl_account=request.expense_gl_account,
            accounts_payable_gl_account=(
                request.accounts_payable_gl_account
            ),
            tax_code=request.tax_code,
            transaction_date=request.transaction_date,
        )

    except ValueError as error:
        return {
            "error": str(error)
        }


@app.post("/tax/ar-journal-lines")
def calculate_ar_tax_journal(
    request: ARTaxJournalRequest,
):
    """Build AR journal lines including tax."""
    try:
        return build_ar_tax_journal_lines(
            net_amount=request.net_amount,
            revenue_gl_account=request.revenue_gl_account,
            accounts_receivable_gl_account=(
                request.accounts_receivable_gl_account
            ),
            tax_code=request.tax_code,
            transaction_date=request.transaction_date,
        )

    except ValueError as error:
        return {
            "error": str(error)
        }

@app.get("/posting-periods")
def get_posting_periods():
    """
    Return all configured posting periods.
    """
    return POSTING_PERIODS

@app.get("/close-readiness/{company_code}")
def get_close_readiness(
    company_code: str,
    fiscal_year: int,
    period_number: int,
) -> dict:
    """
    Return month-end close readiness for one Company Code
    and accounting period.
    """
    return check_close_readiness(
        company_code=company_code,
        fiscal_year=fiscal_year,
        period_number=period_number,
    )

@app.get("/close-audit/{company_code}")
def get_close_audit(company_code: str):
    """
    Return persisted month-end close audit history
    for the selected Company Code.
    """
    return {
        "company_code": company_code.upper(),
        "audit_history": get_close_audit_history(company_code),
    }

@app.post("/period-close")
def period_close(
    company_code: str,
    fiscal_year: int,
    period_number: int,
    approved_by: str,
):
    """
    Close an accounting period through the controlled
    month-end close service.
    """
    return execute_period_close(
        company_code=company_code,
        fiscal_year=fiscal_year,
        period_number=period_number,
        approved_by=approved_by,
    )


 @app.post("/period-close")
def period_close(
    company_code: str,
    fiscal_year: int,
    period_number: int,
    approved_by: str,
):
    """
    Close an accounting period through the controlled
    month-end close service.
    """
    try:
        return execute_period_close(
            company_code=company_code,
            fiscal_year=fiscal_year,
            period_number=period_number,
            approved_by=approved_by,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error