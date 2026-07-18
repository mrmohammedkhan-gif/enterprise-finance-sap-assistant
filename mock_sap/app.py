from fastapi import FastAPI, HTTPException

from mock_sap.business_partner_data import BUSINESS_PARTNERS
from mock_sap.organisation_data import COMPANY_CODES, POSTING_PERIODS
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
# SAP INVOICES
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