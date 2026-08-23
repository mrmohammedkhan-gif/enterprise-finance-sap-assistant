from pathlib import Path
from typing import Any

from pypdf import PdfReader


def extract_invoice_document(
    file_path: str,
) -> dict[str, Any]:
    """
    Extract text from a text-based PDF invoice.

    Scanned/image-only PDFs are not OCR'd here.
    They are returned as requiring an OCR-capable provider.
    """

    path = Path(file_path)

    if not path.exists():
        return {
            "status": "EXTRACTION_FAILED",
            "reason": "FILE_NOT_FOUND",
            "file_path": file_path,
            "provider": "PYPDF",
            "data": {},
            "confidence": {},
        }

    if path.suffix.lower() != ".pdf":
        return {
            "status": "EXTRACTION_FAILED",
            "reason": "UNSUPPORTED_PROVIDER_FILE_TYPE",
            "file_path": file_path,
            "provider": "PYPDF",
            "data": {},
            "confidence": {},
        }

    try:
        reader = PdfReader(str(path))

        extracted_pages = []

        for page in reader.pages:
            page_text = page.extract_text() or ""
            extracted_pages.append(page_text)

        text = "\n".join(extracted_pages).strip()

    except Exception as exc:
        return {
            "status": "EXTRACTION_FAILED",
            "reason": "PDF_READ_ERROR",
            "message": str(exc),
            "file_path": file_path,
            "provider": "PYPDF",
            "data": {},
            "confidence": {},
        }

    if not text:
        return {
            "status": "OCR_REQUIRED",
            "reason": "NO_EXTRACTABLE_TEXT",
            "file_path": file_path,
            "provider": "PYPDF",
            "data": {},
            "confidence": {},
        }

    return {
        "status": "TEXT_EXTRACTED",
        "file_path": file_path,
        "provider": "PYPDF",
        "text": text,
        "data": {},
        "confidence": {},
    }

def parse_invoice_text(
    text: str,
) -> dict[str, Any]:
    """
    Parse simple invoice fields from extracted PDF text.
    """

    fields = {}

    for line in text.splitlines():
        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        key = key.strip().lower()
        value = value.strip()

        if key == "invoice number":
            fields["invoice_number"] = value

        elif key == "vendor id":
            fields["vendor_id"] = value

        elif key == "company code":
            fields["company_code"] = value

        elif key == "invoice date":
            fields["invoice_date"] = value

        elif key == "amount":
            try:
                fields["amount"] = float(value)
            except ValueError:
                fields["amount"] = None

        elif key == "currency":
            fields["currency"] = value

    return fields

def extract_structured_invoice(
    file_path: str,
) -> dict[str, Any]:
    """
    Extract machine-readable PDF text and convert it into
    structured invoice fields for the document pipeline.
    """

    extraction = extract_invoice_document(
        file_path
    )

    if extraction["status"] != "TEXT_EXTRACTED":
        return extraction

    data = parse_invoice_text(
        extraction["text"]
    )

    expected_fields = {
        "invoice_number",
        "vendor_id",
        "company_code",
        "invoice_date",
        "amount",
        "currency",
    }

    confidence = {
        field: 1.0 if field in data and data[field] is not None else 0.0
        for field in expected_fields
    }

    return {
        "status": "EXTRACTED",
        "file_path": file_path,
        "provider": "PYPDF",
        "data": data,
        "confidence": confidence,
        "text": extraction["text"],
    }