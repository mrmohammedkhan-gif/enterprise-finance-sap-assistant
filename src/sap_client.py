from typing import Any

import requests


class SAPClient:
    """Client for the Mock SAP Finance API."""

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8001",
    ) -> None:
        self.base_url = base_url.rstrip("/")

    def _get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = requests.get(
            f"{self.base_url}{path}",
            params=params,
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    def health(self) -> dict:
        return self._get("/health")

    # --------------------------------------------------
    # Chart of Accounts
    # --------------------------------------------------

    def get_charts_of_accounts(self) -> list[dict]:
        return self._get("/chart-of-accounts")

    def get_chart_of_accounts(self, chart_id: str) -> dict:
        return self._get(f"/chart-of-accounts/{chart_id}")

    def get_charts_for_company_code(
        self,
        company_code: str,
    ) -> list[dict]:
        return self._get(
            f"/company-codes/{company_code}/chart-of-accounts"
        )


    # -----------------------------------------------------
    # Vendors
    # -----------------------------------------------------

    def get_vendors(self) -> list[dict]:
        return self._get("/vendors")

    def get_vendor(self, vendor_id: str) -> dict:
        return self._get(f"/vendors/{vendor_id}")

    # -----------------------------------------------------
    # Legacy Invoices
    # -----------------------------------------------------

    def get_invoices(
        self,
        status: str | None = None,
        minimum_amount: float | None = None,
    ) -> list[dict]:
        params: dict[str, Any] = {}

        if status:
            params["status"] = status

        if minimum_amount is not None:
            params["minimum_amount"] = minimum_amount

        return self._get("/invoices", params)

    def get_invoice(self, invoice_id: str) -> dict:
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
        return self._get(
            "/invoices/overdue",
            {"minimum_days": minimum_days},
        )

    # -----------------------------------------------------
    # General Ledger
    # -----------------------------------------------------

    def get_gl_balances(
        self,
        company_code: str | None = None,
    ) -> list[dict]:
        params: dict[str, Any] = {}

        if company_code:
            params["company_code"] = company_code

        return self._get("/gl-balances", params)

    # -----------------------------------------------------
    # SAP Organisation
    # -----------------------------------------------------

    def get_company_codes(self) -> list[dict]:
        return self._get("/company-codes")

    def get_company_code(
        self,
        company_code: str,
    ) -> dict:
        return self._get(
            f"/company-codes/{company_code}"
        )

    def get_posting_period(
        self,
        company_code: str,
        fiscal_year: int,
        period: int,
    ) -> dict:
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
        posting_period = self.get_posting_period(
            company_code=company_code,
            fiscal_year=fiscal_year,
            period=period,
        )

        return posting_period["status"] == "OPEN"

    # -----------------------------------------------------
    # SAP Business Partners
    # -----------------------------------------------------

    def get_business_partners(
        self,
        partner_type: str | None = None,
        company_code: str | None = None,
        status: str | None = None,
    ) -> list[dict]:
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
        return self._get(
            f"/business-partners/{business_partner}"
        )

    def get_blocked_business_partners(
        self,
    ) -> list[dict]:
        return self._get(
            "/business-partners/blocked"
        )

    def can_business_partner_receive_payment(
        self,
        business_partner: str,
    ) -> bool:
        partner = self.get_business_partner(
            business_partner
        )

        return (
            partner["partner_type"] == "VENDOR"
            and partner["status"] == "ACTIVE"
            and partner["payment_block"] is False
        )

    # -----------------------------------------------------
    # SAP Purchase Orders
    # -----------------------------------------------------

    def get_purchase_orders(
        self,
        company_code: str | None = None,
        business_partner: str | None = None,
        approval_status: str | None = None,
        po_status: str | None = None,
    ) -> list[dict]:
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
        return self._get(
            f"/purchase-orders/{purchase_order}"
        )

    def get_open_purchase_orders(
        self,
    ) -> list[dict]:
        return self._get(
            "/purchase-orders/open"
        )

    # -----------------------------------------------------
    # SAP Accounts Payable
    # -----------------------------------------------------

    def get_ap_invoices(
        self,
        company_code: str | None = None,
        business_partner: str | None = None,
        invoice_status: str | None = None,
        payment_status: str | None = None,
        matching_status: str | None = None,
    ) -> list[dict]:
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
        return self._get(
            f"/ap-invoices/{invoice_document}"
        )

    def get_blocked_ap_invoices(
        self,
    ) -> list[dict]:
        return self._get(
            "/ap-invoices/blocked"
        )

    def get_duplicate_ap_invoices(
        self,
    ) -> list[dict]:
        return self._get(
            "/ap-invoices/duplicates"
        )

    def get_parked_ap_invoices(
        self,
    ) -> list[dict]:
        return self._get(
            "/ap-invoices/parked"
        )

    def is_ap_invoice_ready_for_payment(
        self,
        invoice_document: str,
    ) -> bool:
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