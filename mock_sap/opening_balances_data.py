"""
Mock SAP Opening Balances.

Represents the balances carried forward at the beginning of the financial year.
"""

OPENING_BALANCES = [
    {
        "gl_account": "100000",
        "description": "Bank",
        "balance": 20000.00,
        "balance_type": "Debit",
    },
    {
        "gl_account": "110000",
        "description": "Accounts Receivable",
        "balance": 5000.00,
        "balance_type": "Debit",
    },
    {
        "gl_account": "200000",
        "description": "Accounts Payable",
        "balance": 3000.00,
        "balance_type": "Credit",
    },
    {
        "gl_account": "300000",
        "description": "Share Capital",
        "balance": 22000.00,
        "balance_type": "Credit",
    },
]


def get_all_opening_balances():
    """
    Return all opening balances.
    """
    return OPENING_BALANCES


def get_opening_balance(gl_account: str):
    """
    Return one opening balance by G/L Account.
    """
    for account in OPENING_BALANCES:
        if account["gl_account"] == gl_account:
            return account

    return None