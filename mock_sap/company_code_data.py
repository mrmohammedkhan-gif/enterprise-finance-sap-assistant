COMPANY_CODES = [
    {
        "company_code": "UK01",
        "company_name": "Enterprise Finance UK Ltd",
        "country": "United Kingdom",
        "country_code": "GB",
        "local_currency": "GBP",
        "fiscal_year_variant": "V3",
        "fiscal_year_description": "April to March",
        "chart_of_accounts": "YCOA",
        "language": "EN",
        "status": "Active",
    },
    {
        "company_code": "US01",
        "company_name": "Enterprise Finance USA Inc",
        "country": "United States",
        "country_code": "US",
        "local_currency": "USD",
        "fiscal_year_variant": "K4",
        "fiscal_year_description": "January to December",
        "chart_of_accounts": "YCOA",
        "language": "EN",
        "status": "Active",
    },
    {
        "company_code": "DE01",
        "company_name": "Enterprise Finance Germany GmbH",
        "country": "Germany",
        "country_code": "DE",
        "local_currency": "EUR",
        "fiscal_year_variant": "K4",
        "fiscal_year_description": "January to December",
        "chart_of_accounts": "YCOA",
        "language": "DE",
        "status": "Active",
    },
]


def get_all_company_codes() -> list[dict]:
    """
    Return all configured SAP Company Codes.
    """
    return COMPANY_CODES


def get_company_code_by_id(company_code: str) -> dict | None:
    """
    Return one Company Code by its identifier.

    The search is case-insensitive, so uk01 and UK01 both work.
    """
    normalised_code = company_code.strip().upper()

    for company in COMPANY_CODES:
        if company["company_code"] == normalised_code:
            return company

    return None


def company_code_exists(company_code: str) -> bool:
    """
    Check whether a Company Code exists in the master data.
    """
    return get_company_code_by_id(company_code) is not None