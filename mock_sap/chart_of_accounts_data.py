CHARTS_OF_ACCOUNTS = [
    {
        "chart_of_accounts": "YCOA",
        "description": "Enterprise Group Chart of Accounts",
        "language": "EN",
        "status": "Active",
        "assigned_company_codes": ["UK01", "US01", "DE01"],
    },
    {
        "chart_of_accounts": "UKCO",
        "description": "United Kingdom Local Chart of Accounts",
        "language": "EN",
        "status": "Active",
        "assigned_company_codes": ["UK01"],
    },
]


def get_all_charts_of_accounts() -> list[dict]:
    """
    Return all configured Charts of Accounts.
    """
    return CHARTS_OF_ACCOUNTS


def get_chart_of_accounts_by_id(chart_of_accounts: str) -> dict | None:
    """
    Return one Chart of Accounts by its identifier.
    """
    normalised_id = chart_of_accounts.strip().upper()

    for chart in CHARTS_OF_ACCOUNTS:
        if chart["chart_of_accounts"] == normalised_id:
            return chart

    return None


def get_charts_for_company_code(company_code: str) -> list[dict]:
    """
    Return all Charts of Accounts assigned to a Company Code.
    """
    normalised_code = company_code.strip().upper()

    return [
        chart
        for chart in CHARTS_OF_ACCOUNTS
        if normalised_code in chart["assigned_company_codes"]
    ]


def chart_of_accounts_exists(chart_of_accounts: str) -> bool:
    """
    Check whether a Chart of Accounts exists.
    """
    return get_chart_of_accounts_by_id(chart_of_accounts) is not None