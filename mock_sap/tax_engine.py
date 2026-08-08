from decimal import Decimal, ROUND_HALF_UP
from typing import Any

from mock_sap.tax_codes_data import (
    get_compound_tax_codes,
    get_tax_code,
    is_tax_code_active,
)


def round_money(amount: Decimal) -> Decimal:
    """
    Round a monetary amount to two decimal places.
    """
    return amount.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


def validate_tax_code(
    tax_code: str,
    transaction_date: str | None = None,
) -> dict[str, Any]:
    """
    Validate that a tax code exists and is active.
    """
    tax_record = get_tax_code(tax_code)

    if tax_record is None:
        raise ValueError(
            f"Tax code '{tax_code}' was not found."
        )

    if not is_tax_code_active(
        tax_code=tax_code,
        transaction_date=transaction_date,
    ):
        raise ValueError(
            f"Tax code '{tax_code}' is not active "
            "for the selected transaction date."
        )

    return tax_record


def calculate_single_tax(
    net_amount: float | int | str,
    tax_code: str,
    transaction_date: str | None = None,
) -> dict[str, Any]:
    """
    Calculate one VAT, GST, HST, PST or sales-tax component.
    """
    tax_record = validate_tax_code(
        tax_code=tax_code,
        transaction_date=transaction_date,
    )

    net = Decimal(str(net_amount))

    if net < 0:
        raise ValueError(
            "Net amount cannot be negative."
        )

    rate = Decimal(str(tax_record["rate"]))
    tax_amount = round_money(
        net * rate / Decimal("100")
    )
    gross_amount = round_money(
        net + tax_amount
    )

    return {
        "tax_code": tax_record["tax_code"],
        "tax_type": tax_record["tax_type"],
        "country_code": tax_record["country_code"],
        "region_code": tax_record["region_code"],
        "description": tax_record["description"],
        "net_amount": float(round_money(net)),
        "tax_rate": float(rate),
        "tax_amount": float(tax_amount),
        "gross_amount": float(gross_amount),
        "input_tax_gl_account": (
            tax_record["input_tax_gl_account"]
        ),
        "output_tax_gl_account": (
            tax_record["output_tax_gl_account"]
        ),
        "recoverable_percentage": (
            tax_record["recoverable_percentage"]
        ),
        "reverse_charge": tax_record["reverse_charge"],
        "zero_rated": tax_record["zero_rated"],
        "exempt": tax_record["exempt"],
    }


def calculate_compound_tax(
    net_amount: float | int | str,
    compound_group: str,
    transaction_date: str | None = None,
) -> dict[str, Any]:
    """
    Calculate multiple tax components belonging to one compound group.

    Example:
    British Columbia GST 5% plus PST 7%.
    """
    tax_records = get_compound_tax_codes(
        compound_group
    )

    if not tax_records:
        raise ValueError(
            f"Compound tax group '{compound_group}' "
            "was not found."
        )

    net = Decimal(str(net_amount))

    if net < 0:
        raise ValueError(
            "Net amount cannot be negative."
        )

    components = []
    total_tax = Decimal("0.00")

    for tax_record in tax_records:
        validate_tax_code(
            tax_code=tax_record["tax_code"],
            transaction_date=transaction_date,
        )

        rate = Decimal(str(tax_record["rate"]))
        component_tax = round_money(
            net * rate / Decimal("100")
        )

        total_tax += component_tax

        components.append(
            {
                "tax_code": tax_record["tax_code"],
                "tax_type": tax_record["tax_type"],
                "description": tax_record["description"],
                "tax_rate": float(rate),
                "tax_amount": float(component_tax),
                "input_tax_gl_account": (
                    tax_record["input_tax_gl_account"]
                ),
                "output_tax_gl_account": (
                    tax_record["output_tax_gl_account"]
                ),
                "recoverable_percentage": (
                    tax_record["recoverable_percentage"]
                ),
            }
        )

    total_tax = round_money(total_tax)
    gross_amount = round_money(
        net + total_tax
    )

    return {
        "compound_group": compound_group.upper(),
        "net_amount": float(round_money(net)),
        "components": components,
        "total_tax": float(total_tax),
        "gross_amount": float(gross_amount),
    }


def build_ap_tax_journal_lines(
    net_amount: float | int | str,
    expense_gl_account: str,
    accounts_payable_gl_account: str,
    tax_code: str,
    transaction_date: str | None = None,
) -> dict[str, Any]:
    """
    Build Accounts Payable journal lines for a taxable supplier invoice.
    """
    calculation = calculate_single_tax(
        net_amount=net_amount,
        tax_code=tax_code,
        transaction_date=transaction_date,
    )

    return {
        "calculation": calculation,
        "line_items": [
            {
                "gl_account": expense_gl_account,
                "debit": calculation["net_amount"],
                "credit": 0.0,
                "description": "Expense excluding tax",
            },
            {
                "gl_account": calculation[
                    "input_tax_gl_account"
                ],
                "debit": calculation["tax_amount"],
                "credit": 0.0,
                "description": "Input tax",
            },
            {
                "gl_account": accounts_payable_gl_account,
                "debit": 0.0,
                "credit": calculation["gross_amount"],
                "description": "Accounts Payable",
            },
        ],
    }


def build_ar_tax_journal_lines(
    net_amount: float | int | str,
    revenue_gl_account: str,
    accounts_receivable_gl_account: str,
    tax_code: str,
    transaction_date: str | None = None,
) -> dict[str, Any]:
    """
    Build Accounts Receivable journal lines for a taxable customer invoice.
    """
    calculation = calculate_single_tax(
        net_amount=net_amount,
        tax_code=tax_code,
        transaction_date=transaction_date,
    )

    return {
        "calculation": calculation,
        "line_items": [
            {
                "gl_account": accounts_receivable_gl_account,
                "debit": calculation["gross_amount"],
                "credit": 0.0,
                "description": "Accounts Receivable",
            },
            {
                "gl_account": revenue_gl_account,
                "debit": 0.0,
                "credit": calculation["net_amount"],
                "description": "Revenue excluding tax",
            },
            {
                "gl_account": calculation[
                    "output_tax_gl_account"
                ],
                "debit": 0.0,
                "credit": calculation["tax_amount"],
                "description": "Output tax",
            },
        ],
    }