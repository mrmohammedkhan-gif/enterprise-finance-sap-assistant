import json

from langchain_core.tools import tool

try:
    from src.rag import search_finance_policies
    from src.sap_client import SAPClient
except ModuleNotFoundError:
    from rag import search_finance_policies
    from sap_client import SAPClient

sap_client = SAPClient()


# ---------------------------------------------------------
# INVOICES
# ---------------------------------------------------------


@tool
def get_overdue_invoices(minimum_days: int = 1) -> str:
    """Return invoices overdue by at least the specified number of days."""
    invoices = sap_client.get_overdue_invoices(minimum_days)
    return json.dumps(invoices, indent=2)


@tool
def get_open_invoices(minimum_amount: float = 0) -> str:
    """Return open invoices above the specified minimum amount."""
    invoices = sap_client.get_invoices(
        status="OPEN",
        minimum_amount=minimum_amount,
    )
    return json.dumps(invoices, indent=2)


@tool
def review_invoice_for_approval(
    invoice_id: str,
    approval_limit: float = 10000,
) -> str:
    """
    Review an invoice and return an approval recommendation.

    This tool checks vendor status, invoice value and overdue status.
    It does not approve, post or pay the invoice.
    """
    invoice = sap_client.get_invoice(invoice_id)
    vendor = sap_client.get_vendor(invoice["vendor_id"])

    checks = {
        "vendor_active": vendor["status"] == "ACTIVE",
        "within_approval_limit": invoice["amount"] <= approval_limit,
        "invoice_not_overdue": invoice["status"] != "OVERDUE",
    }

    failed_reasons: list[str] = []

    if not checks["vendor_active"]:
        failed_reasons.append("vendor is inactive")

    if not checks["within_approval_limit"]:
        failed_reasons.append(
            f"invoice amount exceeds the "
            f"£{approval_limit:,.0f} approval limit"
        )

    if not checks["invoice_not_overdue"]:
        failed_reasons.append("invoice is overdue")

    if not checks["vendor_active"]:
        recommendation = "REJECT"
        reason = "The vendor is inactive."
    elif failed_reasons:
        recommendation = "REVIEW"
        reason = (
            "Manual review is required because "
            + " and ".join(failed_reasons)
            + "."
        )
    else:
        recommendation = "APPROVE"
        reason = "All configured approval checks passed."

    result = {
        "invoice": invoice,
        "vendor": vendor,
        "approval_limit": approval_limit,
        "checks": checks,
        "recommendation": recommendation,
        "reason": reason,
    }

    return json.dumps(result, indent=2)


# ---------------------------------------------------------
# VENDORS
# ---------------------------------------------------------


@tool
def get_vendor(vendor_id: str) -> str:
    """Return vendor master data for the specified vendor ID."""
    vendor = sap_client.get_vendor(vendor_id)
    return json.dumps(vendor, indent=2)


# ---------------------------------------------------------
# GENERAL LEDGER
# ---------------------------------------------------------


@tool
def get_gl_balances(company_code: str = "UK01") -> str:
    """Return general-ledger balances for the specified company code."""
    balances = sap_client.get_gl_balances(company_code)
    return json.dumps(balances, indent=2)


# ---------------------------------------------------------
# SAP ORGANISATION
# ---------------------------------------------------------


@tool
def get_company_code(company_code: str) -> str:
    """
    Return SAP company-code master data.

    Use this tool for questions about company name, country,
    local currency, chart of accounts, fiscal-year variant
    and company-code status.
    """
    company = sap_client.get_company_code(company_code)
    return json.dumps(company, indent=2)

@tool
def list_charts_of_accounts() -> str:
    """
    Return all configured SAP Charts of Accounts.
    """

    charts = sap_client.get_charts_of_accounts()

    return json.dumps(charts, indent=2)


@tool
def get_chart_of_accounts(chart_id: str) -> str:
    """
    Return one SAP Chart of Accounts.
    """

    chart = sap_client.get_chart_of_accounts(chart_id)

    return json.dumps(chart, indent=2)


@tool
def get_company_chart_of_accounts(company_code: str) -> str:
    """
    Return the Chart(s) of Accounts assigned to a Company Code.
    """

    charts = sap_client.get_charts_for_company_code(company_code)

    return json.dumps(charts, indent=2)
@tool
def get_chart_of_accounts(chart_id: str) -> str:
    """
    Return SAP Chart of Accounts master data.
    """

    chart = sap_client.get_chart_of_accounts(chart_id)

    return json.dumps(chart, indent=2)


@tool
def list_charts_of_accounts() -> str:
    """
    Return all configured Charts of Accounts.
    """

    charts = sap_client.get_charts_of_accounts()

    return json.dumps(charts, indent=2)


@tool
def get_company_charts(company_code: str) -> str:
    """
    Return Charts of Accounts assigned to a Company Code.
    """

    charts = sap_client.get_charts_for_company_code(company_code)

    return json.dumps(charts, indent=2)


@tool
def check_posting_period(
    company_code: str,
    fiscal_year: int,
    period: int,
) -> str:
    """
    Check whether an SAP posting period is open.

    Use this tool before recommending that a journal entry,
    invoice or other finance document can be posted.
    """
    posting_period = sap_client.get_posting_period(
        company_code=company_code,
        fiscal_year=fiscal_year,
        period=period,
    )

    result = {
        "company_code": company_code,
        "fiscal_year": fiscal_year,
        "period": period,
        "status": posting_period["status"],
        "is_open": posting_period["status"] == "OPEN",
    }

    return json.dumps(result, indent=2)


# ---------------------------------------------------------
# SAP BUSINESS PARTNERS
# ---------------------------------------------------------


@tool
def list_business_partners(
    partner_type: str | None = None,
    company_code: str | None = None,
    status: str | None = None,
) -> str:
    """
    Return SAP business partners using optional filters.

    partner_type can be VENDOR or CUSTOMER.
    status can be ACTIVE or INACTIVE.
    """
    partners = sap_client.get_business_partners(
        partner_type=partner_type,
        company_code=company_code,
        status=status,
    )

    return json.dumps(partners, indent=2)


@tool
def get_business_partner(business_partner: str) -> str:
    """
    Return SAP business-partner master data.

    Use this tool for questions about a partner's type,
    company code, country, currency, payment terms,
    payment block, bank account and status.
    """
    partner = sap_client.get_business_partner(
        business_partner
    )
    return json.dumps(partner, indent=2)


@tool
def list_blocked_business_partners() -> str:
    """Return all SAP business partners blocked for payment."""
    partners = sap_client.get_blocked_business_partners()
    return json.dumps(partners, indent=2)


@tool
def check_business_partner_payment(
    business_partner: str,
) -> str:
    """
    Check whether a business partner can receive payment.

    Payment is permitted only when the partner is an active
    vendor and is not blocked for payment.
    """
    partner = sap_client.get_business_partner(
        business_partner
    )

    can_receive_payment = (
        partner["partner_type"] == "VENDOR"
        and partner["status"] == "ACTIVE"
        and partner["payment_block"] is False
    )

    reasons: list[str] = []

    if partner["partner_type"] != "VENDOR":
        reasons.append(
            "The business partner is not configured as a vendor."
        )

    if partner["status"] != "ACTIVE":
        reasons.append(
            "The business partner is not active."
        )

    if partner["payment_block"] is True:
        reasons.append(
            "The business partner has a payment block."
        )

    if can_receive_payment:
        decision = "PAYMENT ALLOWED"
        explanation = (
            "The business partner is an active vendor "
            "and has no payment block."
        )
    else:
        decision = "PAYMENT NOT ALLOWED"
        explanation = " ".join(reasons)

    result = {
        "business_partner": partner,
        "can_receive_payment": can_receive_payment,
        "decision": decision,
        "explanation": explanation,
    }

    return json.dumps(result, indent=2)


# ---------------------------------------------------------
# SAP PURCHASE ORDERS
# ---------------------------------------------------------


@tool
def list_purchase_orders(
    company_code: str | None = None,
    business_partner: str | None = None,
    approval_status: str | None = None,
    po_status: str | None = None,
) -> str:
    """
    Return SAP purchase orders using optional filters.

    Use this tool to filter purchase orders by company code,
    supplier, approval status or purchase-order status.
    """
    purchase_orders = sap_client.get_purchase_orders(
        company_code=company_code,
        business_partner=business_partner,
        approval_status=approval_status,
        po_status=po_status,
    )

    return json.dumps(purchase_orders, indent=2)


@tool
def get_purchase_order(purchase_order: str) -> str:
    """
    Return details for a specified SAP purchase order.

    The result includes supplier, company code, total value,
    approval status, goods receipt, invoice receipt and PO status.
    """
    result = sap_client.get_purchase_order(
        purchase_order
    )

    return json.dumps(result, indent=2)


@tool
def list_open_purchase_orders() -> str:
    """Return all SAP purchase orders with an OPEN status."""
    purchase_orders = sap_client.get_open_purchase_orders()
    return json.dumps(purchase_orders, indent=2)


@tool
def check_purchase_order_invoice_match(
    purchase_order: str,
) -> str:
    """
    Check whether a purchase order is ready for invoice matching.

    The check considers PO approval, goods receipt,
    invoice-receipt status, supplier status and payment block.
    """
    po = sap_client.get_purchase_order(purchase_order)
    partner = sap_client.get_business_partner(
        po["business_partner"]
    )

    checks = {
        "po_approved": po["approval_status"] == "APPROVED",
        "goods_received": (
            po["goods_receipt_status"] == "RECEIVED"
        ),
        "invoice_not_already_matched": (
            po["invoice_receipt_status"] != "MATCHED"
        ),
        "supplier_active": partner["status"] == "ACTIVE",
        "supplier_not_blocked": (
            partner["payment_block"] is False
        ),
    }

    failed_reasons: list[str] = []

    if not checks["po_approved"]:
        failed_reasons.append(
            "the purchase order is not approved"
        )

    if not checks["goods_received"]:
        failed_reasons.append(
            "the goods receipt is not complete"
        )

    if not checks["invoice_not_already_matched"]:
        failed_reasons.append(
            "the purchase order is already invoice matched"
        )

    if not checks["supplier_active"]:
        failed_reasons.append(
            "the supplier is inactive"
        )

    if not checks["supplier_not_blocked"]:
        failed_reasons.append(
            "the supplier has a payment block"
        )

    ready_for_matching = all(checks.values())

    if po["invoice_receipt_status"] == "MATCHED":
        decision = "ALREADY MATCHED"
        explanation = (
            "The purchase order has already been matched "
            "to an invoice."
        )
    elif ready_for_matching:
        decision = "READY FOR INVOICE MATCHING"
        explanation = (
            "The purchase order is approved, goods have been "
            "received and the supplier is active and unblocked."
        )
    else:
        decision = "NOT READY FOR INVOICE MATCHING"
        explanation = (
            "The purchase order requires attention because "
            + " and ".join(failed_reasons)
            + "."
        )

    result = {
        "purchase_order": po,
        "business_partner": partner,
        "checks": checks,
        "ready_for_invoice_matching": ready_for_matching,
        "decision": decision,
        "explanation": explanation,
    }

    return json.dumps(result, indent=2)


# ---------------------------------------------------------
# FINANCE POLICY RAG
# ---------------------------------------------------------


@tool
def search_finance_policy(question: str) -> str:
    """
    Search company finance policies for approval, payment,
    travel, audit and finance-procedure questions.
    """
    documents = search_finance_policies(question)

    results = [
        {
            "source": document.metadata.get("source", "unknown"),
            "content": document.page_content,
        }
        for document in documents
    ]

    return json.dumps(results, indent=2)


# ---------------------------------------------------------
# CFO DASHBOARD
# ---------------------------------------------------------


@tool
def get_cfo_dashboard_summary() -> str:
    """
    Return CFO dashboard metrics and key finance risks.

    Use this tool for dashboard risks, outstanding AP,
    overdue exposure, current finance position and
    largest vendor exposure.
    """
    invoices = sap_client.get_invoices()
    overdue_invoices = sap_client.get_overdue_invoices(1)

    open_invoices = [
        invoice
        for invoice in invoices
        if invoice["status"] == "OPEN"
    ]

    outstanding_invoices = [
        invoice
        for invoice in invoices
        if invoice["status"] in {"OPEN", "OVERDUE"}
    ]

    outstanding_ap = sum(
        invoice["amount"]
        for invoice in outstanding_invoices
    )

    vendor_exposure: dict[str, float] = {}

    for invoice in outstanding_invoices:
        vendor_id = invoice["vendor_id"]
        vendor_exposure[vendor_id] = (
            vendor_exposure.get(vendor_id, 0.0)
            + invoice["amount"]
        )

    largest_vendor_id = max(
        vendor_exposure,
        key=vendor_exposure.get,
        default=None,
    )

    largest_vendor_exposure = (
        vendor_exposure[largest_vendor_id]
        if largest_vendor_id
        else 0.0
    )

    largest_vendor_name = None

    if largest_vendor_id:
        vendor = sap_client.get_vendor(largest_vendor_id)
        largest_vendor_name = vendor["name"]

    largest_overdue_invoice = max(
        overdue_invoices,
        key=lambda invoice: invoice["amount"],
        default=None,
    )

    risks: list[str] = []

    if overdue_invoices:
        risks.append(
            f"{len(overdue_invoices)} invoice(s) are overdue."
        )

    if largest_overdue_invoice:
        risks.append(
            f"The largest overdue invoice is "
            f"{largest_overdue_invoice['invoice_id']} "
            f"for £{largest_overdue_invoice['amount']:,.2f}."
        )

    if largest_vendor_name:
        risks.append(
            f"The largest vendor exposure is "
            f"£{largest_vendor_exposure:,.2f} "
            f"with {largest_vendor_name}."
        )

    result = {
        "outstanding_ap": outstanding_ap,
        "open_invoice_count": len(open_invoices),
        "overdue_invoice_count": len(overdue_invoices),
        "largest_vendor_id": largest_vendor_id,
        "largest_vendor_name": largest_vendor_name,
        "largest_vendor_exposure": largest_vendor_exposure,
        "largest_overdue_invoice": largest_overdue_invoice,
        "risks": risks,
    }

    return json.dumps(result, indent=2)
@tool
def explain_ap_invoice_status(
    invoice_document: str,
) -> str:
    """
    Explain why an SAP AP invoice is blocked,
    parked, duplicated, matched or ready for payment.
    """
    invoice = sap_client.get_ap_invoice(invoice_document)
    partner = sap_client.get_business_partner(
        invoice["business_partner"]
    )

    purchase_order = None

    if invoice["purchase_order"]:
        purchase_order = sap_client.get_purchase_order(
            invoice["purchase_order"]
        )

    checks = {
        "invoice_posted": invoice["invoice_status"] == "POSTED",
        "invoice_not_blocked": invoice["payment_block"] is False,
        "invoice_unique": (
            invoice["duplicate_check_status"] == "UNIQUE"
        ),
        "invoice_matched": invoice["matching_status"] in {
            "MATCHED",
            "NON_PO",
        },
        "supplier_active": partner["status"] == "ACTIVE",
        "supplier_not_blocked": (
            partner["payment_block"] is False
        ),
    }

    if purchase_order is not None:
        checks["po_approved"] = (
            purchase_order["approval_status"] == "APPROVED"
        )
        checks["goods_received"] = (
            purchase_order["goods_receipt_status"] == "RECEIVED"
        )

    reasons: list[str] = []

    if not checks["invoice_posted"]:
        reasons.append(
            f"the invoice status is {invoice['invoice_status']}"
        )

    if not checks["invoice_not_blocked"]:
        reasons.append("the invoice has a payment block")

    if not checks["invoice_unique"]:
        reasons.append("the invoice is flagged as a duplicate")

    if not checks["invoice_matched"]:
        reasons.append(
            f"the matching status is "
            f"{invoice['matching_status']}"
        )

    if not checks["supplier_active"]:
        reasons.append("the supplier is inactive")

    if not checks["supplier_not_blocked"]:
        reasons.append("the supplier has a payment block")

    if purchase_order is not None:
        if not checks["po_approved"]:
            reasons.append(
                "the related purchase order is not approved"
            )

        if not checks["goods_received"]:
            reasons.append(
                "the goods receipt is not complete"
            )

    ready_for_payment = all(checks.values())

    if ready_for_payment:
        decision = "READY FOR PAYMENT"
        explanation = (
            "The invoice is posted, unique, fully matched, "
            "unblocked, and the supplier is active and unblocked."
        )
    else:
        decision = "NOT READY FOR PAYMENT"
        explanation = (
            "The invoice cannot be paid because "
            + ", ".join(reasons)
            + "."
        )

    result = {
        "invoice": invoice,
        "business_partner": partner,
        "purchase_order": purchase_order,
        "checks": checks,
        "ready_for_payment": ready_for_payment,
        "decision": decision,
        "explanation": explanation,
    }

    return json.dumps(result, indent=2)

@tool
def generate_payment_proposal(
    company_code: str = "UK01",
) -> str:
    """
    Generate a payment proposal for AP invoices that are ready for payment.

    The proposal excludes blocked, duplicate, unmatched,
    unposted, inactive-supplier, and supplier-blocked invoices.
    """
    invoices = sap_client.get_ap_invoices(
        company_code=company_code
    )

    proposed_invoices: list[dict] = []
    excluded_invoices: list[dict] = []

    total_proposed_amount = 0.0

    for invoice in invoices:
        partner = sap_client.get_business_partner(
            invoice["business_partner"]
        )

        checks = {
            "invoice_posted": (
                invoice["invoice_status"] == "POSTED"
            ),
            "invoice_unpaid": (
                invoice["payment_status"] == "UNPAID"
            ),
            "invoice_not_blocked": (
                invoice["payment_block"] is False
            ),
            "invoice_unique": (
                invoice["duplicate_check_status"] == "UNIQUE"
            ),
            "invoice_matched": (
                invoice["matching_status"] in {
                    "MATCHED",
                    "NON_PO",
                }
            ),
            "supplier_active": (
                partner["status"] == "ACTIVE"
            ),
            "supplier_not_blocked": (
                partner["payment_block"] is False
            ),
        }

        ready_for_payment = all(checks.values())

        if ready_for_payment:
            proposed_invoices.append(
                {
                    "invoice_document": (
                        invoice["invoice_document"]
                    ),
                    "business_partner": (
                        invoice["business_partner"]
                    ),
                    "vendor_invoice_reference": (
                        invoice["vendor_invoice_reference"]
                    ),
                    "currency": invoice["currency"],
                    "invoice_amount": (
                        invoice["invoice_amount"]
                    ),
                    "payment_due_date": (
                        invoice["payment_due_date"]
                    ),
                }
            )

            total_proposed_amount += invoice["invoice_amount"]
        else:
            failed_checks = [
                check_name
                for check_name, passed in checks.items()
                if not passed
            ]

            excluded_invoices.append(
                {
                    "invoice_document": (
                        invoice["invoice_document"]
                    ),
                    "failed_checks": failed_checks,
                }
            )

    result = {
        "company_code": company_code,
        "proposal_status": (
            "PAYMENT PROPOSAL GENERATED"
        ),
        "invoice_count": len(proposed_invoices),
        "total_proposed_amount": total_proposed_amount,
        "proposed_invoices": proposed_invoices,
        "excluded_invoices": excluded_invoices,
        "note": (
            "This is a simulated payment proposal. "
            "No payment has been executed."
        ),
    }

    return json.dumps(result, indent=2)

@tool
def list_gl_accounts() -> list[dict]:
    """List all General Ledger accounts."""
    return sap_client.get_gl_accounts()


@tool
def get_gl_account(gl_account: str) -> dict:
    """Return details for one General Ledger account."""
    return sap_client.get_gl_account(gl_account)


@tool
def get_gl_accounts_for_chart(chart_of_accounts: str) -> list[dict]:
    """List all G/L accounts assigned to a Chart of Accounts."""
    return sap_client.get_gl_accounts_for_chart(chart_of_accounts)

@tool
def list_journal_entries() -> list[dict]:
    """List all journal entries."""
    return sap_client.get_journal_entries()


@tool
def get_journal_entry(document_number: str) -> dict:
    """Return one journal entry by document number."""
    return sap_client.get_journal_entry(document_number)


@tool
def get_company_journal_entries(company_code: str) -> list[dict]:
    """List journal entries for one Company Code."""
    return sap_client.get_company_journal_entries(company_code)

@tool
def get_trial_balance() -> list[dict]:
    """Return the calculated Trial Balance."""
    return sap_client.get_trial_balance()

SAP_TOOLS = [
  
    generate_payment_proposal,
    explain_ap_invoice_status,
    get_overdue_invoices,
    get_open_invoices,
    review_invoice_for_approval,
    get_vendor,
    get_gl_balances,
    get_company_code,
    list_charts_of_accounts,
    get_chart_of_accounts,
    get_company_chart_of_accounts,
    check_posting_period,
    list_business_partners,
    get_business_partner,
    list_blocked_business_partners,
    check_business_partner_payment,
    list_purchase_orders,
    get_purchase_order,
    list_open_purchase_orders,
    check_purchase_order_invoice_match,
    search_finance_policy,
    get_cfo_dashboard_summary,
    list_gl_accounts,
    get_gl_account,
    get_gl_accounts_for_chart,
    list_journal_entries,
    get_journal_entry,
    get_company_journal_entries,
    get_trial_balance,

]