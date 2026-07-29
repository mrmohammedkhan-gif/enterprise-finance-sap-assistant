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

    for journal in get_all_journal_entries():

        for line in journal["line_items"]:

            account = line["gl_account"]

            balances[account]["debit"] += line["debit"]
            balances[account]["credit"] += line["credit"]

    trial_balance = []

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

    return trial_balance