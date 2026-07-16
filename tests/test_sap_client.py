from src.sap_client import SAPClient


client = SAPClient()

print("Health:")
print(client.health())

print("\nOverdue invoices over 30 days:")
print(client.get_overdue_invoices(30))

print("\nVendor V1001:")
print(client.get_vendor("V1001"))

print("\nGL balances for UK01:")
print(client.get_gl_balances("UK01"))