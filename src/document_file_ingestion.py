from pathlib import Path
from typing import Any


SUPPORTED_DOCUMENT_TYPES = {
    ".pdf": "PDF",
    ".png": "IMAGE",
    ".jpg": "IMAGE",
    ".jpeg": "IMAGE",
}

from src.document_ingestion_adapter import (
    ingest_invoice_for_finance,
)

def inspect_document_file(
    file_path: str,
) -> dict[str, Any]:
    """
    Validate a finance document file before extraction.
    """

    path = Path(file_path)

    if not path.exists():
        return {
            "status": "REJECTED",
            "reason": "FILE_NOT_FOUND",
            "file_path": str(path),
        }

    extension = path.suffix.lower()

    if extension not in SUPPORTED_DOCUMENT_TYPES:
        return {
            "status": "REJECTED",
            "reason": "UNSUPPORTED_DOCUMENT_TYPE",
            "file_path": str(path),
            "extension": extension,
        }

    return {
        "status": "ACCEPTED",
        "file_path": str(path),
        "file_name": path.name,
        "extension": extension,
        "document_type": SUPPORTED_DOCUMENT_TYPES[extension],
        "size_bytes": path.stat().st_size,
    }

def process_finance_document(
    file_path: str,
    raw_document: dict[str, Any],
    raw_confidence: dict[str, float],
) -> dict[str, Any]:
    """
    Validate the document file before passing extracted
    invoice data into the finance document workflow.
    """

    file_result = inspect_document_file(
        file_path
    )

    if file_result["status"] != "ACCEPTED":
        return {
            "status": "BLOCKED",
            "reason": file_result["reason"],
            "file_result": file_result,
        }

    finance_result = ingest_invoice_for_finance(
        raw_document=raw_document,
        raw_confidence=raw_confidence,
    )

    return {
        "status": finance_result["status"],
        "file_result": file_result,
        "finance_result": finance_result,
    }