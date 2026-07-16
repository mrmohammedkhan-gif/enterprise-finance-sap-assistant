from src.tools import search_finance_policy


result = search_finance_policy.invoke(
    {
        "question": (
            "What is the company policy for approving "
            "invoices above £10,000?"
        )
    }
)

print(result)