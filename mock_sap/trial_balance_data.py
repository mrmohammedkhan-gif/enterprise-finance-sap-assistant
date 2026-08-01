from collections import defaultdict

from mock_sap.gl_account_data import get_gl_account_by_id
from mock_sap.journal_entries_data import get_all_journal_entries
from mock_sap.opening_balances_data import get_all_opening_balances


def calculate_trial_balance() -> dict:
    """
    Calculate the Trial Balance from opening balances
    and current-period journal entries.
    """

    balances = defaultdict(
        lambda: {
            "debit": 0.0,
            "credit": 0.0,
        }
    )

    # Add opening balances first.
    for opening_balance in get_all_opening_balances():
        account = opening_balance["gl_account"]
        amount = float(opening_balance["balance"])
        balance_type = opening_balance["balance_type"]

        if balance_type == "Debit":
            balances[account]["debit"] += amount

        elif balance_type == "Credit":
            balances[account]["credit"] += amount

    # Add current-period journal-entry movements.
    for journal in get_all_journal_entries():
        for line in journal["line_items"]:
            account = line["gl_account"]

            balances[account]["debit"] += float(line["debit"])
            balances[account]["credit"] += float(line["credit"])

    trial_balance = []

    for account in sorted(balances.keys()):
        account_info = get_gl_account_by_id(account)

        if account_info is None:
            continue

        debit = balances[account]["debit"]
        credit = balances[account]["credit"]
        net_balance = debit - credit

        if net_balance > 0:
            balance_type = "Debit"
        elif net_balance < 0:
            balance_type = "Credit"
        else:
            balance_type = "Balanced"

        trial_balance.append(
            {
                "gl_account": account,
                "description": account_info["description"],
                "account_type": account_info["account_type"],
                "category": account_info["category"],
                "total_debit": debit,
                "total_credit": credit,
                "balance": abs(net_balance),
                "balance_type": balance_type,
            }
        )

    total_debits = sum(
        account["total_debit"]
        for account in trial_balance
    )

    total_credits = sum(
        account["total_credit"]
        for account in trial_balance
    )

    return {
        "accounts": trial_balance,
        "total_debits": total_debits,
        "total_credits": total_credits,
        "balances": round(total_debits, 2) == round(total_credits, 2),
    }