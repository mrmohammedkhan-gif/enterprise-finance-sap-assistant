"""
Mock SAP purchase-order data.
"""

PURCHASE_ORDERS = [
    {
        "purchase_order": "4500001001",
        "business_partner": "BP1000",
        "company_code": "UK01",
        "description": "Office furniture and equipment",
        "currency": "GBP",
        "total_value": 12500.00,
        "approval_status": "APPROVED",
        "goods_receipt_status": "RECEIVED",
        "invoice_receipt_status": "MATCHED",
        "po_status": "CLOSED",
    },
    {
        "purchase_order": "4500001002",
        "business_partner": "BP2000",
        "company_code": "UK01",
        "description": "IT support services",
        "currency": "GBP",
        "total_value": 24000.00,
        "approval_status": "PENDING",
        "goods_receipt_status": "NOT_RECEIVED",
        "invoice_receipt_status": "NOT_RECEIVED",
        "po_status": "OPEN",
    },
    {
        "purchase_order": "4500001003",
        "business_partner": "BP4000",
        "company_code": "DE01",
        "description": "Manufacturing components",
        "currency": "EUR",
        "total_value": 48000.00,
        "approval_status": "APPROVED",
        "goods_receipt_status": "PARTIAL",
        "invoice_receipt_status": "PARTIAL",
        "po_status": "OPEN",
    },
    {
        "purchase_order": "4500001004",
        "business_partner": "BP1000",
        "company_code": "UK01",
        "description": "Printer consumables",
        "currency": "GBP",
        "total_value": 3500.00,
        "approval_status": "REJECTED",
        "goods_receipt_status": "NOT_RECEIVED",
        "invoice_receipt_status": "NOT_RECEIVED",
        "po_status": "CANCELLED",
    },
]