from src.tools import (
    get_gl_balances,
    get_open_invoices,
    get_overdue_invoices,
    get_vendor,
)


print("Overdue invoices:")
print(get_overdue_invoices.invoke({"minimum_days": 30}))

print("\nOpen invoices above £5,000:")
print(get_open_invoices.invoke({"minimum_amount": 5000}))

print("\nVendor V1001:")
print(get_vendor.invoke({"vendor_id": "V1001"}))

print("\nGL balances:")
print(get_gl_balances.invoke({"company_code": "UK01"}))