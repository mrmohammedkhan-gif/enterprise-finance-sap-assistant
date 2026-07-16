
from fastapi import FastAPI, HTTPException

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


@app.get("/vendors")
def list_vendors() -> list[dict]:
    return VENDORS


@app.get("/vendors/{vendor_id}")
def get_vendor(vendor_id: str) -> dict:
    vendor = next(
        (
            item
            for item in VENDORS
            if item["vendor_id"].lower() == vendor_id.lower()
        ),
        None,
    )

    if vendor is None:
        raise HTTPException(
            status_code=404,
            detail=f"Vendor {vendor_id} was not found.",
        )

    return vendor


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