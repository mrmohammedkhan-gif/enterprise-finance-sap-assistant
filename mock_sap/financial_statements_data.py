from mock_sap.gl_account_data import get_gl_account_by_id
from mock_sap.trial_balance_data import calculate_trial_balance


def get_signed_balance(account: dict) -> float:
    """
    Convert the displayed account balance into a signed amount.

    Debit balances are positive.
    Credit balances are negative.
    Balanced accounts are zero.
    """

    balance = float(account["balance"])
    balance_type = account["balance_type"]

    if balance_type == "Debit":
        return balance

    if balance_type == "Credit":
        return -balance

    return 0.0


def build_balance_sheet(accounts: list[dict]) -> dict:
    """
    Build the Balance Sheet from Trial Balance accounts.
    """

    assets = []
    liabilities = []
    equity = []

    for account in accounts:
        if account["account_type"] != "Balance Sheet":
            continue

        gl_master = get_gl_account_by_id(account["gl_account"])

        if gl_master is None:
            continue

        category = gl_master["category"]

        report_line = {
            "gl_account": account["gl_account"],
            "description": account["description"],
            "category": category,
            "balance": account["balance"],
            "balance_type": account["balance_type"],
        }

        if category == "Asset":
            assets.append(report_line)

        elif category == "Liability":
            liabilities.append(report_line)

        elif category == "Equity":
            equity.append(report_line)

    total_assets = sum(
        get_signed_balance(account)
        for account in assets
    )

    # Liabilities and equity normally have credit balances.
    # Multiplying by -1 presents normal credit balances as positive totals.
    total_liabilities = -sum(
        get_signed_balance(account)
        for account in liabilities
    )

    total_equity = -sum(
        get_signed_balance(account)
        for account in equity
    )

    total_liabilities_and_equity = (
        total_liabilities + total_equity
    )

    return {
        "assets": assets,
        "liabilities": liabilities,
        "equity": equity,
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "total_equity": total_equity,
        "total_liabilities_and_equity": total_liabilities_and_equity,
        "balances": (
            round(total_assets, 2)
            == round(total_liabilities_and_equity, 2)
        ),
    }


def build_profit_and_loss(accounts: list[dict]) -> dict:
    """
    Build the Profit and Loss Statement from Trial Balance accounts.
    """

    revenue = []
    expenses = []

    for account in accounts:
        if account["account_type"] != "Profit & Loss":
            continue

        gl_master = get_gl_account_by_id(account["gl_account"])

        if gl_master is None:
            continue

        category = gl_master["category"]

        report_line = {
            "gl_account": account["gl_account"],
            "description": account["description"],
            "category": category,
            "balance": account["balance"],
            "balance_type": account["balance_type"],
        }

        if category == "Revenue":
            revenue.append(report_line)

        elif category == "Expense":
            expenses.append(report_line)

    # Revenue normally has a credit balance.
    total_revenue = -sum(
        get_signed_balance(account)
        for account in revenue
    )

    # Expenses normally have debit balances.
    total_expenses = sum(
        get_signed_balance(account)
        for account in expenses
    )

    net_profit = total_revenue - total_expenses

    if net_profit > 0:
        result_type = "Profit"
    elif net_profit < 0:
        result_type = "Loss"
    else:
        result_type = "Break-even"

    return {
        "revenue": revenue,
        "expenses": expenses,
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "net_profit": net_profit,
        "result_type": result_type,
    }


def calculate_financial_statements() -> dict:
    """
    Generate the Balance Sheet and Profit and Loss Statement
    from the calculated Trial Balance.
    """

    trial_balance = calculate_trial_balance()
    accounts = trial_balance["accounts"]

    balance_sheet = build_balance_sheet(accounts)
    profit_and_loss = build_profit_and_loss(accounts)

    return {
        "trial_balance_balances": trial_balance["balances"],
        "balance_sheet": balance_sheet,
        "profit_and_loss": profit_and_loss,
    }


def get_balance_sheet() -> dict:
    """
    Return only the Balance Sheet.
    """

    statements = calculate_financial_statements()
    return statements["balance_sheet"]


def get_profit_and_loss() -> dict:
    """
    Return only the Profit and Loss Statement.
    """

    statements = calculate_financial_statements()
    return statements["profit_and_loss"]