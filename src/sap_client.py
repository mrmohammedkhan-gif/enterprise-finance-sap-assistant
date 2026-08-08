from typing import Any

import requests


class SAPClient:

       # -----------------------------------------------------
    # ENTERPRISE TAX ENGINE
    # -----------------------------------------------------

    def get_tax_codes(self) -> list[dict]:
        """Return all configured tax codes."""
        return self._get("/tax-codes")

    def get_tax_code(
        self,
        tax_code: str,
    ) -> dict:
        """Return one tax code."""
        return self._get(
            f"/tax-codes/{tax_code}"
        )

    def get_tax_codes_for_country(
        self,
        country_code: str,
    ) -> list[dict]:
        """Return active tax codes for one country."""
        return self._get(
            f"/tax-codes/country/{country_code}"
        )

    def get_tax_codes_for_region(
        self,
        country_code: str,
        region_code: str,
    ) -> list[dict]:
        """Return active tax codes for one country and region."""
        return self._get(
            f"/tax-codes/country/{country_code}/"
            f"region/{region_code}"
        )

    def get_compound_tax_codes(
        self,
        compound_group: str,
    ) -> list[dict]:
        """Return tax codes in one compound group."""
        return self._get(
            f"/tax-codes/compound/{compound_group}"
        )

    def calculate_tax(
        self,
        net_amount: float,
        tax_code: str,
        transaction_date: str | None = None,
    ) -> dict:
        """Calculate one VAT, GST, HST, PST or sales-tax component."""
        payload = {
            "net_amount": net_amount,
            "tax_code": tax_code,
            "transaction_date": transaction_date,
        }

        return self._post(
            "/tax/calculate",
            json=payload,
        )

    def calculate_compound_tax(
        self,
        net_amount: float,
        compound_group: str,
        transaction_date: str | None = None,
    ) -> dict:
        """Calculate multiple tax components in one compound group."""
        payload = {
            "net_amount": net_amount,
            "compound_group": compound_group,
            "transaction_date": transaction_date,
        }

        return self._post(
            "/tax/calculate-compound",
            json=payload,
        )

    def build_ap_tax_journal_lines(
        self,
        net_amount: float,
        expense_gl_account: str,
        accounts_payable_gl_account: str,
        tax_code: str,
        transaction_date: str | None = None,
    ) -> dict:
        """Build supplier-invoice journal lines including tax."""
        payload = {
            "net_amount": net_amount,
            "expense_gl_account": expense_gl_account,
            "accounts_payable_gl_account": (
                accounts_payable_gl_account
            ),
            "tax_code": tax_code,
            "transaction_date": transaction_date,
        }

        return self._post(
            "/tax/ap-journal-lines",
            json=payload,
        )

    def build_ar_tax_journal_lines(
        self,
        net_amount: float,
        revenue_gl_account: str,
        accounts_receivable_gl_account: str,
        tax_code: str,
        transaction_date: str | None = None,
    ) -> dict:
        """Build customer-invoice journal lines including tax."""
        payload = {
            "net_amount": net_amount,
            "revenue_gl_account": revenue_gl_account,
            "accounts_receivable_gl_account": (
                accounts_receivable_gl_account
            ),
            "tax_code": tax_code,
            "transaction_date": transaction_date,
        }

        return self._post(
            "/tax/ar-journal-lines",
            json=payload,
        )
    

    """
    Client for communicating with the Mock SAP Finance API.

    This class separates HTTP communication from finance business logic.
    """

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8001",
    ) -> None:
        self.base_url = base_url.rstrip("/")

    # -----------------------------------------------------
    # HTTP HELPERS
    # -----------------------------------------------------

    def _get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """
        Send a GET request to the Mock SAP API.
        """
        response = requests.get(
            f"{self.base_url}{path}",
            params=params,
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    def _post(
        self,
        path: str,
        json: dict[str, Any],
    ) -> Any:
        """
        Send a POST request to the Mock SAP API.
        """
        response = requests.post(
            f"{self.base_url}{path}",
            json=json,
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    def health(self) -> dict:
        """
        Check whether the Mock SAP API is running.
        """
        return self._get("/health")

    # -----------------------------------------------------
    # CHART OF ACCOUNTS
    # -----------------------------------------------------

    def get_charts_of_accounts(self) -> list[dict]:
        """
        Return all Charts of Accounts.
        """
        return self._get("/chart-of-accounts")

    def get_chart_of_accounts(
        self,
        chart_id: str,
    ) -> dict:
        """
        Return one Chart of Accounts.
        """
        return self._get(
            f"/chart-of-accounts/{chart_id}"
        )

    def get_charts_for_company_code(
        self,
        company_code: str,
    ) -> list[dict]:
        """
        Return Charts of Accounts assigned to a Company Code.
        """
        return self._get(
            f"/company-codes/{company_code}/chart-of-accounts"
        )

    # -----------------------------------------------------
    # GENERAL LEDGER ACCOUNTS
    # -----------------------------------------------------

    def get_gl_accounts(self) -> list[dict]:
        """
        Return all General Ledger accounts.
        """
        return self._get("/gl-accounts")

    def get_gl_account(
        self,
        gl_account: str,
    ) -> dict:
        """
        Return one General Ledger account.
        """
        return self._get(
            f"/gl-accounts/{gl_account}"
        )

    def get_gl_accounts_for_chart(
        self,
        chart_of_accounts: str,
    ) -> list[dict]:
        """
        Return G/L accounts assigned to a Chart of Accounts.
        """
        return self._get(
            f"/chart-of-accounts/"
            f"{chart_of_accounts}/gl-accounts"
        )

    def get_gl_balances(
        self,
        company_code: str | None = None,
    ) -> list[dict]:
        """
        Return General Ledger balances.

        Optionally filter by Company Code.
        """
        params: dict[str, Any] = {}

        if company_code:
            params["company_code"] = company_code

        return self._get(
            "/gl-balances",
            params,
        )

    # -----------------------------------------------------
    # JOURNAL ENTRIES
    # -----------------------------------------------------

    def get_journal_entries(self) -> list[dict]:
        """
        Return all journal entries.
        """
        return self._get("/journal-entries")

    def get_journal_entry(
        self,
        document_number: str,
    ) -> dict:
        """
        Return one journal entry.
        """
        return self._get(
            f"/journal-entries/{document_number}"
        )

    def get_company_journal_entries(
        self,
        company_code: str,
    ) -> list[dict]:
        """
        Return journal entries for one Company Code.
        """
        return self._get(
            f"/company-codes/"
            f"{company_code}/journal-entries"
        )

    def post_journal_entry(
        self,
        company_code: str,
        debit_gl_account: str,
        credit_gl_account: str,
        amount: float,
        reference: str,
        document_type: str = "SA",
        currency: str | None = None,
        posting_date: str | None = None,
    ) -> dict:
        """
        Create a balanced two-line journal entry.
        """
        payload = {
            "company_code": company_code,
            "debit_gl_account": debit_gl_account,
            "credit_gl_account": credit_gl_account,
            "amount": amount,
            "reference": reference,
            "document_type": document_type,
            "currency": currency,
            "posting_date": posting_date,
        }

        return self._post(
            "/journal-entries",
            json=payload,
        )

    # -----------------------------------------------------
    # TRIAL BALANCE AND FINANCIAL STATEMENTS
    # -----------------------------------------------------

    def get_trial_balance(self) -> dict:
        """
        Return the calculated Trial Balance.
        """
        return self._get("/trial-balance")

    def get_financial_statements(self) -> dict:
        """
        Return the complete Financial Statements report.
        """
        return self._get("/financial-statements")

    def get_balance_sheet(self) -> dict:
        """
        Return the calculated Balance Sheet.
        """
        return self._get("/balance-sheet")

    def get_profit_and_loss(self) -> dict:
        """
        Return the calculated Profit and Loss Statement.
        """
        return self._get("/profit-and-loss")

    # -----------------------------------------------------
    # SAP ORGANISATION
    # -----------------------------------------------------

    def get_company_codes(self) -> list[dict]:
        """
        Return all Company Codes.
        """
        return self._get("/company-codes")

    def get_company_code(
        self,
        company_code: str,
    ) -> dict:
        """
        Return one Company Code.
        """
        return self._get(
            f"/company-codes/{company_code}"
        )

    def get_posting_period(
        self,
        company_code: str,
        fiscal_year: int,
        period: int,
    ) -> dict:
        """
        Return one posting-period record.
        """
        return self._get(
            f"/posting-periods/{company_code}",
            {
                "fiscal_year": fiscal_year,
                "period": period,
            },
        )

    def is_posting_period_open(
        self,
        company_code: str,
        fiscal_year: int,
        period: int,
    ) -> bool:
        """
        Check whether a posting period is open.
        """
        posting_period = self.get_posting_period(
            company_code=company_code,
            fiscal_year=fiscal_year,
            period=period,
        )

        return posting_period["status"] == "OPEN"

    # -----------------------------------------------------
    # VENDORS
    # -----------------------------------------------------

    def get_vendors(self) -> list[dict]:
        """
        Return all vendors.
        """
        return self._get("/vendors")

    def get_vendor(
        self,
        vendor_id: str,
    ) -> dict:
        """
        Return one vendor.
        """
        return self._get(
            f"/vendors/{vendor_id}"
        )

    # -----------------------------------------------------
    # VENDOR INVOICES
    # -----------------------------------------------------

    def get_vendor_invoices(self) -> list[dict]:
        """
        Return all vendor invoices.
        """
        return self._get("/vendor-invoices")

    def get_vendor_invoice(
        self,
        invoice_number: str,
    ) -> dict:
        """
        Return one vendor invoice.
        """
        return self._get(
            f"/vendor-invoices/{invoice_number}"
        )

    def get_open_vendor_invoices(
        self,
        company_code: str | None = None,
    ) -> list[dict]:
        """
        Return open vendor invoices.

        Optionally filter by Company Code.
        """
        params: dict[str, Any] = {}

        if company_code:
            params["company_code"] = company_code

        return self._get(
            "/vendor-invoices/open",
            params,
        )

    def get_overdue_vendor_invoices(
        self,
        as_of_date: str | None = None,
        company_code: str | None = None,
    ) -> list[dict]:
        """
        Return overdue vendor invoices.
        """
        params: dict[str, Any] = {}

        if as_of_date:
            params["as_of_date"] = as_of_date

        if company_code:
            params["company_code"] = company_code

        return self._get(
            "/vendor-invoices/overdue",
            params,
        )

    def get_vendor_open_balance(
        self,
        vendor_id: str,
    ) -> dict:
        """
        Return the open invoice balance for one vendor.
        """
        return self._get(
            f"/vendors/{vendor_id}/open-balance"
        )

    # -----------------------------------------------------
    # VENDOR PAYMENTS
    # -----------------------------------------------------

    def get_vendor_payments(self) -> list[dict]:
        """
        Return all vendor payments.
        """
        return self._get("/vendor-payments")

    def get_vendor_payment(
        self,
        payment_number: str,
    ) -> dict:
        """
        Return one vendor payment.
        """
        return self._get(
            f"/vendor-payments/{payment_number}"
        )

    def get_vendor_payments_for_vendor(
        self,
        vendor_id: str,
    ) -> list[dict]:
        """
        Return payment history for one vendor.
        """
        return self._get(
            f"/vendors/{vendor_id}/payments"
        )

    def get_vendor_payments_for_invoice(
        self,
        invoice_number: str,
    ) -> list[dict]:
        """
        Return payments linked to one vendor invoice.
        """
        return self._get(
            f"/vendor-invoices/"
            f"{invoice_number}/payments"
        )

    def post_vendor_payment(
        self,
        invoice_number: str,
        payment_method: str = "BANK_TRANSFER",
        bank_gl_account: str = "100000",
        payment_date: str | None = None,
    ) -> dict:
        """
        Post payment for one open vendor invoice.
        """
        payload = {
            "invoice_number": invoice_number,
            "payment_method": payment_method,
            "bank_gl_account": bank_gl_account,
            "payment_date": payment_date,
        }

        return self._post(
            "/vendor-payments",
            json=payload,
        )

    # -----------------------------------------------------
    # LEGACY INVOICES
    # -----------------------------------------------------

    def get_invoices(
        self,
        status: str | None = None,
        minimum_amount: float | None = None,
    ) -> list[dict]:
        """
        Return legacy invoice records.
        """
        params: dict[str, Any] = {}

        if status:
            params["status"] = status

        if minimum_amount is not None:
            params["minimum_amount"] = minimum_amount

        return self._get(
            "/invoices",
            params,
        )

    def get_invoice(
        self,
        invoice_id: str,
    ) -> dict:
        """
        Return one legacy invoice.
        """
        invoices = self.get_invoices()

        invoice = next(
            (
                item
                for item in invoices
                if item["invoice_id"].lower()
                == invoice_id.lower()
            ),
            None,
        )

        if invoice is None:
            raise ValueError(
                f"Invoice {invoice_id} was not found."
            )

        return invoice

    def get_overdue_invoices(
        self,
        minimum_days: int = 1,
    ) -> list[dict]:
        """
        Return overdue legacy invoices.
        """
        return self._get(
            "/invoices/overdue",
            {
                "minimum_days": minimum_days,
            },
        )

    # -----------------------------------------------------
    # SAP BUSINESS PARTNERS
    # -----------------------------------------------------

    def get_business_partners(
        self,
        partner_type: str | None = None,
        company_code: str | None = None,
        status: str | None = None,
    ) -> list[dict]:
        """
        Return Business Partners using optional filters.
        """
        params: dict[str, Any] = {}

        if partner_type:
            params["partner_type"] = partner_type

        if company_code:
            params["company_code"] = company_code

        if status:
            params["status"] = status

        return self._get(
            "/business-partners",
            params,
        )

    def get_business_partner(
        self,
        business_partner: str,
    ) -> dict:
        """
        Return one Business Partner.
        """
        return self._get(
            f"/business-partners/{business_partner}"
        )

    def get_blocked_business_partners(
        self,
    ) -> list[dict]:
        """
        Return blocked Business Partners.
        """
        return self._get(
            "/business-partners/blocked"
        )

    def can_business_partner_receive_payment(
        self,
        business_partner: str,
    ) -> bool:
        """
        Check whether a vendor can receive payment.
        """
        partner = self.get_business_partner(
            business_partner
        )

        return (
            partner["partner_type"] == "VENDOR"
            and partner["status"] == "ACTIVE"
            and partner["payment_block"] is False
        )

    # -----------------------------------------------------
    # SAP PURCHASE ORDERS
    # -----------------------------------------------------

    def get_purchase_orders(
        self,
        company_code: str | None = None,
        business_partner: str | None = None,
        approval_status: str | None = None,
        po_status: str | None = None,
    ) -> list[dict]:
        """
        Return Purchase Orders using optional filters.
        """
        params: dict[str, Any] = {}

        if company_code:
            params["company_code"] = company_code

        if business_partner:
            params["business_partner"] = business_partner

        if approval_status:
            params["approval_status"] = approval_status

        if po_status:
            params["po_status"] = po_status

        return self._get(
            "/purchase-orders",
            params,
        )

    def get_purchase_order(
        self,
        purchase_order: str,
    ) -> dict:
        """
        Return one Purchase Order.
        """
        return self._get(
            f"/purchase-orders/{purchase_order}"
        )

    def get_open_purchase_orders(
        self,
    ) -> list[dict]:
        """
        Return open Purchase Orders.
        """
        return self._get(
            "/purchase-orders/open"
        )

    # -----------------------------------------------------
    # SAP ACCOUNTS PAYABLE
    # -----------------------------------------------------

    def get_ap_invoices(
        self,
        company_code: str | None = None,
        business_partner: str | None = None,
        invoice_status: str | None = None,
        payment_status: str | None = None,
        matching_status: str | None = None,
    ) -> list[dict]:
        """
        Return Accounts Payable invoices using optional filters.
        """
        params: dict[str, Any] = {}

        if company_code:
            params["company_code"] = company_code

        if business_partner:
            params["business_partner"] = business_partner

        if invoice_status:
            params["invoice_status"] = invoice_status

        if payment_status:
            params["payment_status"] = payment_status

        if matching_status:
            params["matching_status"] = matching_status

        return self._get(
            "/ap-invoices",
            params,
        )

    def get_ap_invoice(
        self,
        invoice_document: str,
    ) -> dict:
        """
        Return one Accounts Payable invoice.
        """
        return self._get(
            f"/ap-invoices/{invoice_document}"
        )

    def get_blocked_ap_invoices(
        self,
    ) -> list[dict]:
        """
        Return blocked Accounts Payable invoices.
        """
        return self._get(
            "/ap-invoices/blocked"
        )

    def get_duplicate_ap_invoices(
        self,
    ) -> list[dict]:
        """
        Return duplicate Accounts Payable invoices.
        """
        return self._get(
            "/ap-invoices/duplicates"
        )

    def get_parked_ap_invoices(
        self,
    ) -> list[dict]:
        """
        Return parked Accounts Payable invoices.
        """
        return self._get(
            "/ap-invoices/parked"
        )

    def is_ap_invoice_ready_for_payment(
        self,
        invoice_document: str,
    ) -> bool:
        """
        Check whether an AP invoice is ready for payment.
        """
        invoice = self.get_ap_invoice(
            invoice_document
        )

        partner = self.get_business_partner(
            invoice["business_partner"]
        )

        return (
            invoice["invoice_status"] == "POSTED"
            and invoice["payment_status"] == "UNPAID"
            and invoice["payment_block"] is False
            and invoice["duplicate_check_status"] == "UNIQUE"
            and invoice["matching_status"] in {
                "MATCHED",
                "NON_PO",
            }
            and partner["status"] == "ACTIVE"
            and partner["payment_block"] is False
        )