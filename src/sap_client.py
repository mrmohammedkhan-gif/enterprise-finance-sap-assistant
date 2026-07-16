from typing import Any

import requests


class SAPClient:
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

    def get_vendors(self) -> list[dict]:
        return self._get("/vendors")

    def get_vendor(self, vendor_id: str) -> dict:
        return self._get(f"/vendors/{vendor_id}")

    def get_invoices(
        self,
        status: str | None = None,
        minimum_amount: float | None = None,
    ) -> list[dict]:
        params = {}

        if status:
            params["status"] = status

        if minimum_amount is not None:
            params["minimum_amount"] = minimum_amount

        return self._get("/invoices", params)

    def get_invoice(self, invoice_id: str) -> dict:
        invoices = self.get_invoices()

        invoice = next(
            (
                inv
                for inv in invoices
                if inv["invoice_id"].lower() == invoice_id.lower()
            ),
            None,
        )

        if invoice is None:
            raise ValueError(f"Invoice {invoice_id} not found.")

        return invoice

    def get_overdue_invoices(
        self,
        minimum_days: int = 1,
    ) -> list[dict]:
        return self._get(
            "/invoices/overdue",
            {"minimum_days": minimum_days},
        )

    def get_gl_balances(
        self,
        company_code: str | None = None,
    ) -> list[dict]:
        params = (
            {"company_code": company_code}
            if company_code
            else None
        )

        return self._get("/gl-balances", params)