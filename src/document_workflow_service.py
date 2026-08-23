from typing import Any

from src.document_intelligence_service import (
    process_invoice_extraction,
)
from src.mcp_server import get_vendor_invoices


def prepare_invoice_for_finance_workflow(
    extracted_data: dict[str, Any],
    field_confidence: dict[str, float],
) -> dict[str, Any]:
    """
    Allow invoice data to continue only when document
    validation and confidence controls have passed.
    """

    document_result = process_invoice_extraction(
        extracted_data=extracted_data,
        field_confidence=field_confidence,
    )

    if document_result["status"] != "READY_FOR_WORKFLOW":
        return {
            "status": "BLOCKED",
            "reason": document_result["status"],
            "document_result": document_result,
        }

    return {
        "status": "READY_FOR_FINANCE",
        "invoice_data": document_result["data"],
        "document_result": document_result,
    }


def enrich_invoice_with_ap_context(
    extracted_data: dict[str, Any],
    field_confidence: dict[str, float],
    user_id: str,
) -> dict[str, Any]:
    """
    Enrich a validated invoice with governed AP context.

    Document data must pass validation and confidence checks
    before any governed finance tool is called.
    """

    prepared = prepare_invoice_for_finance_workflow(
        extracted_data=extracted_data,
        field_confidence=field_confidence,
    )

    if prepared["status"] != "READY_FOR_FINANCE":
        return prepared

    invoice_data = prepared["invoice_data"]

    ap_context = get_vendor_invoices(
        company_code=invoice_data["company_code"],
        user_id=user_id,
    )

    return {
        "status": "ENRICHED",
        "invoice_data": invoice_data,
        "ap_context": ap_context,
    }