from typing import Any


def extract_invoice_document(
    file_path: str,
) -> dict[str, Any]:
    """
    Placeholder extraction provider.

    A production implementation can later call Azure Document
    Intelligence, UiPath Document Understanding, or another
    approved extraction service.
    """

    return {
        "status": "EXTRACTION_PENDING",
        "file_path": file_path,
        "provider": "NOT_CONFIGURED",
        "data": {},
        "confidence": {},
    }