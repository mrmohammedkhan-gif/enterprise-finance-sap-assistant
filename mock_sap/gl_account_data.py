GL_ACCOUNTS = [
    {
        "gl_account": "100000",
        "description": "Bank",
        "chart_of_accounts": "YCOA",
        "account_type": "Balance Sheet",
        "category": "Asset",
        "posting_allowed": True,
    },
    {
        "gl_account": "110000",
        "description": "Accounts Receivable",
        "chart_of_accounts": "YCOA",
        "account_type": "Balance Sheet",
        "category": "Asset",
        "posting_allowed": True,
    },
    {
        "gl_account": "200000",
        "description": "Accounts Payable",
        "chart_of_accounts": "YCOA",
        "account_type": "Balance Sheet",
        "category": "Liability",
        "posting_allowed": True,
    },
    {
        "gl_account": "300000",
        "description": "Share Capital",
        "chart_of_accounts": "YCOA",
        "account_type": "Balance Sheet",
        "category": "Equity",
        "posting_allowed": True,
    },
    {
        "gl_account": "400000",
        "description": "Sales Revenue",
        "chart_of_accounts": "YCOA",
        "account_type": "Profit & Loss",
        "category": "Revenue",
        "posting_allowed": True,
    },
    {
        "gl_account": "500000",
        "description": "Office Expenses",
        "chart_of_accounts": "YCOA",
        "account_type": "Profit & Loss",
        "category": "Expense",
        "posting_allowed": True,
    },
    {
        "gl_account": "510000",
        "description": "Travel Expenses",
        "chart_of_accounts": "YCOA",
        "account_type": "Profit & Loss",
        "category": "Expense",
        "posting_allowed": True,
    },
]


def get_all_gl_accounts():
    return GL_ACCOUNTS


def get_gl_account_by_id(gl_account):
    gl_account = gl_account.upper()

    for account in GL_ACCOUNTS:
        if account["gl_account"] == gl_account:
            return account

    return None


def get_gl_accounts_for_chart(chart_of_accounts):
    chart_of_accounts = chart_of_accounts.upper()

    return [
        account
        for account in GL_ACCOUNTS
        if account["chart_of_accounts"] == chart_of_accounts
    ]