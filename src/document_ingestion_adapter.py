from typing import Any

from src.document_intelligence_service import (
    process_invoice_extraction,
)

from src.document_workflow_service import (
    prepare_invoice_for_finance_workflow,
)


def normalise_invoice_document(
    raw_document: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalise raw extracted invoice data into the schema
    expected by the document-intelligence workflow.
    """

    return {
        "invoice_number": raw_document.get("invoice_number"),
        "vendor_id": raw_document.get("vendor_id"),
        "company_code": raw_document.get("company_code"),
        "invoice_date": raw_document.get("invoice_date"),
        "amount": raw_document.get("amount"),
        "currency": raw_document.get("currency"),
    }


def normalise_confidence_scores(
    raw_confidence: dict[str, float],
) -> dict[str, float]:
    """
    Normalise field-level confidence scores for invoice extraction.
    """

    return {
        "invoice_number": raw_confidence.get("invoice_number", 0.0),
        "vendor_id": raw_confidence.get("vendor_id", 0.0),
        "company_code": raw_confidence.get("company_code", 0.0),
        "invoice_date": raw_confidence.get("invoice_date", 0.0),
        "amount": raw_confidence.get("amount", 0.0),
        "currency": raw_confidence.get("currency", 0.0),
    }


def ingest_invoice_document(
    raw_document: dict[str, Any],
    raw_confidence: dict[str, float],
) -> dict[str, Any]:
    """
    Normalise raw document extraction results and pass them
    through the document-intelligence validation controls.
    """

    extracted_data = normalise_invoice_document(
        raw_document
    )

    field_confidence = normalise_confidence_scores(
        raw_confidence
    )

    return process_invoice_extraction(
        extracted_data=extracted_data,
        field_confidence=field_confidence,
    )

def ingest_invoice_for_finance(
    raw_document: dict[str, Any],
    raw_confidence: dict[str, float],
) -> dict[str, Any]:
    """
    Ingest raw invoice extraction results and pass them
    through the complete document-to-finance control gate.
    """

    extracted_data = normalise_invoice_document(
        raw_document
    )

    field_confidence = normalise_confidence_scores(
        raw_confidence
    )

    return prepare_invoice_for_finance_workflow(
        extracted_data=extracted_data,
        field_confidence=field_confidence,
    )