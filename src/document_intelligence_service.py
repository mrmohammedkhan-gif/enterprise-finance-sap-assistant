from typing import Any


REQUIRED_INVOICE_FIELDS = {
    "invoice_number",
    "vendor_id",
    "company_code",
    "invoice_date",
    "amount",
    "currency",
}

MINIMUM_CONFIDENCE = 0.85


def validate_invoice_document(
    extracted_data: dict[str, Any],
) -> dict[str, Any]:
    """
    Validate structured fields extracted from a finance document.
    """

    missing_fields = sorted(
        field
        for field in REQUIRED_INVOICE_FIELDS
        if (
            field not in extracted_data
            or extracted_data[field] is None
            or (
                isinstance(extracted_data[field], str)
                and not extracted_data[field].strip()
            )
        )
    )

    if missing_fields:
        return {
            "status": "INVALID",
            "missing_fields": missing_fields,
            "data": extracted_data,
        }

    return {
        "status": "VALID",
        "missing_fields": [],
        "data": extracted_data,
    }


def assess_extraction_confidence(
    field_confidence: dict[str, float],
) -> dict[str, Any]:
    """
    Identify extracted invoice fields that require
    human review because confidence is too low.
    """

    low_confidence_fields = {
        field: confidence
        for field, confidence in field_confidence.items()
        if confidence < MINIMUM_CONFIDENCE
    }

    if low_confidence_fields:
        return {
            "status": "HUMAN_REVIEW_REQUIRED",
            "threshold": MINIMUM_CONFIDENCE,
            "low_confidence_fields": low_confidence_fields,
        }

    return {
        "status": "ACCEPTED",
        "threshold": MINIMUM_CONFIDENCE,
        "low_confidence_fields": {},
    }


def process_invoice_extraction(
    extracted_data: dict[str, Any],
    field_confidence: dict[str, float],
) -> dict[str, Any]:
    """
    Validate extracted invoice data and determine whether
    it is safe to continue into the finance workflow.
    """

    validation = validate_invoice_document(
        extracted_data
    )

    if validation["status"] != "VALID":
        return {
            "status": "REJECTED",
            "reason": "MISSING_REQUIRED_FIELDS",
            "validation": validation,
        }

    confidence = assess_extraction_confidence(
        field_confidence
    )

    if confidence["status"] != "ACCEPTED":
        return {
            "status": "HUMAN_REVIEW_REQUIRED",
            "reason": "LOW_EXTRACTION_CONFIDENCE",
            "validation": validation,
            "confidence": confidence,
        }

    return {
        "status": "READY_FOR_WORKFLOW",
        "validation": validation,
        "confidence": confidence,
        "data": extracted_data,
    }