from typing import Any


FINANCE_USERS: dict[str, dict[str, Any]] = {
    "finance.manager@demo.local": {
        "display_name": "Finance Manager",
        "roles": ["FINANCE_MANAGER"],
        "company_codes": ["UK01"],
    },
    "financial.accountant@demo.local": {
        "display_name": "Financial Accountant",
        "roles": ["FINANCIAL_ACCOUNTANT"],
        "company_codes": ["UK01"],
    },
    "ap.manager@demo.local": {
        "display_name": "AP Manager",
        "roles": ["AP_MANAGER"],
        "company_codes": ["UK01"],
    },
}


ACTION_ROLES: dict[str, list[str]] = {
    "close_accounting_period": [
        "FINANCE_MANAGER",
    ],
    "create_journal_entry": [
        "FINANCE_MANAGER",
        "FINANCIAL_ACCOUNTANT",
    ],
    "get_gl_balances": [
        "FINANCE_MANAGER",
        "FINANCIAL_ACCOUNTANT",
    ],
    "get_vendor_invoices": [
        "FINANCE_MANAGER",
        "FINANCIAL_ACCOUNTANT",
        "AP_MANAGER",
    ],
}


def is_user_authorised(
    user_id: str,
    action: str,
    company_code: str,
) -> bool:
    """
    Check whether a finance user is authorised
    for an action and Company Code.
    """
    user = FINANCE_USERS.get(user_id)

    if user is None:
        return False

    if company_code.upper() not in user["company_codes"]:
        return False

    allowed_roles = ACTION_ROLES.get(action, [])

    return any(
        role in allowed_roles
        for role in user["roles"]
    )