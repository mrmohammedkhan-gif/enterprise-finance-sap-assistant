"""
Mock SAP Business Partner master data.
"""

BUSINESS_PARTNERS = [
    {
        "business_partner": "BP1000",
        "partner_type": "VENDOR",
        "name": "Office Supplies Ltd",
        "company_code": "UK01",
        "country": "GB",
        "currency": "GBP",
        "payment_terms": "30 DAYS",
        "payment_block": False,
        "status": "ACTIVE",
        "bank_account": "GB29NWBK60161331926819",
    },
    {
        "business_partner": "BP2000",
        "partner_type": "VENDOR",
        "name": "Global IT Services",
        "company_code": "UK01",
        "country": "GB",
        "currency": "GBP",
        "payment_terms": "14 DAYS",
        "payment_block": True,
        "status": "ACTIVE",
        "bank_account": "GB82WEST12345698765432",
    },
    {
        "business_partner": "BP3000",
        "partner_type": "CUSTOMER",
        "name": "ABC Retail plc",
        "company_code": "UK01",
        "country": "GB",
        "currency": "GBP",
        "payment_terms": "30 DAYS",
        "payment_block": False,
        "status": "ACTIVE",
        "bank_account": "",
    },
    {
        "business_partner": "BP4000",
        "partner_type": "VENDOR",
        "name": "European Components GmbH",
        "company_code": "DE01",
        "country": "DE",
        "currency": "EUR",
        "payment_terms": "45 DAYS",
        "payment_block": False,
        "status": "INACTIVE",
        "bank_account": "DE89370400440532013000",
    },
]