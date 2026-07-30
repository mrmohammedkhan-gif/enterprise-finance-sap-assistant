
from mock_sap.trial_balance_data import calculate_trial_balance

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
from mock_sap.organisation_data import COMPANY_CODES, POSTING_PERIODS
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
            and item["period"] == period
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