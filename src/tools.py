import json

from langchain_core.tools import tool

from src.rag import search_finance_policies
from src.sap_client import SAPClient


sap_client = SAPClient()


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
def get_vendor(vendor_id: str) -> str:
    """Return vendor master data for the specified vendor ID."""
    vendor = sap_client.get_vendor(vendor_id)
    return json.dumps(vendor, indent=2)


@tool
def get_gl_balances(company_code: str = "UK01") -> str:
    """Return general-ledger balances for the specified company code."""
    balances = sap_client.get_gl_balances(company_code)
    return json.dumps(balances, indent=2)


@tool
def get_company_code(company_code: str) -> str:
    """
    Return SAP company-code master data.

    Use this tool for questions about company name, country,
    local currency, chart of accounts, fiscal-year variant,
    and company-code status.
    """
    company = sap_client.get_company_code(company_code)
    return json.dumps(company, indent=2)


@tool
def check_posting_period(
    company_code: str,
    fiscal_year: int,
    period: int,
) -> str:
    """
    Check whether an SAP posting period is open.

    Use this tool before recommending that a journal entry,
    invoice, or other finance document can be posted.
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
    payment block, bank account, and status.
    """
    partner = sap_client.get_business_partner(
        business_partner
    )
    return json.dumps(partner, indent=2)


@tool
def list_blocked_business_partners() -> str:
    """
    Return all SAP business partners blocked for payment.
    """
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


@tool
def review_invoice_for_approval(
    invoice_id: str,
    approval_limit: float = 10000,
) -> str:
    """
    Review an invoice and return an approval recommendation.

    This tool checks vendor status, invoice value, and overdue status.
    It does not approve, post, or pay the invoice.
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


@tool
def search_finance_policy(question: str) -> str:
    """
    Search company finance policies for approval, payment,
    travel, audit, and finance-procedure questions.
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


@tool
def get_cfo_dashboard_summary() -> str:
    """
    Return CFO dashboard metrics and key finance risks.

    Use this tool for dashboard risks, outstanding AP,
    overdue exposure, current finance position, and
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


SAP_TOOLS = [
    get_overdue_invoices,
    get_open_invoices,
    get_vendor,
    get_gl_balances,
    get_company_code,
    check_posting_period,
    list_business_partners,
    get_business_partner,
    list_blocked_business_partners,
    check_business_partner_payment,
    review_invoice_for_approval,
    search_finance_policy,
    get_cfo_dashboard_summary,
]