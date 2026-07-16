from src.tools import review_invoice_for_approval


print("Review INV-1002:")
print(
    review_invoice_for_approval.invoke(
        {
            "invoice_id": "INV-1002",
            "approval_limit": 10000,
        }
    )
)

print("\nReview INV-1003:")
print(
    review_invoice_for_approval.invoke(
        {
            "invoice_id": "INV-1003",
            "approval_limit": 10000,
        }
    )
)