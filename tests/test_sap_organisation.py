from src.sap_client import SAPClient


client = SAPClient()

print("Company code UK01:")
print(client.get_company_code("UK01"))

print("\nPosting period 07/2026:")
print(
    client.get_posting_period(
        company_code="UK01",
        fiscal_year=2026,
        period=7,
    )
)

print("\nIs period 7 open?")
print(
    client.is_posting_period_open(
        company_code="UK01",
        fiscal_year=2026,
        period=7,
    )
)

print("\nIs period 9 open?")
print(
    client.is_posting_period_open(
        company_code="UK01",
        fiscal_year=2026,
        period=9,
    )
)