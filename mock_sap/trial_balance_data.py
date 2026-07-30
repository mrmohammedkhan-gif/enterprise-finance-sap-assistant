from collections import defaultdict

from mock_sap.journal_entries_data import get_all_journal_entries
from mock_sap.gl_account_data import get_gl_account_by_id


def calculate_trial_balance():
    """
    Calculate the Trial Balance from all Journal Entries.
    """

    balances = defaultdict(
        lambda: {
            "debit": 0.0,
            "credit": 0.0,
        }
    )

    # Read every Journal Entry
    for journal in get_all_journal_entries():

        # Read every line item
        for line in journal["line_items"]:

            account = line["gl_account"]

            balances[account]["debit"] += line["debit"]
            balances[account]["credit"] += line["credit"]

    trial_balance = []

    # Build the Trial Balance
    for account in sorted(balances.keys()):

        account_info = get_gl_account_by_id(account)

        debit = balances[account]["debit"]
        credit = balances[account]["credit"]

        balance = debit - credit

        if balance > 0:
            balance_type = "Debit"
        elif balance < 0:
            balance_type = "Credit"
        else:
            balance_type = "Balanced"

        trial_balance.append(
            {
                "gl_account": account,
                "description": account_info["description"],
                "account_type": account_info["account_type"],
                "total_debit": debit,
                "total_credit": credit,
                "balance": abs(balance),
                "balance_type": balance_type,
            }
        )

    # Calculate overall totals
    total_debits = sum(
        account["total_debit"]
        for account in trial_balance
    )

    total_credits = sum(
        account["total_credit"]
        for account in trial_balance
    )

    # Return full Trial Balance report
    return {
        "accounts": trial_balance,
        "total_debits": total_debits,
        "total_credits": total_credits,
        "balances": total_debits == total_credits,
    }

