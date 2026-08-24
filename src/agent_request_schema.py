from dataclasses import dataclass
from typing import Union

from src.finance_context import (
    FinanceContext,
    validate_finance_context,
)
from src.request_parameter_schemas import (
    GLBalanceParameters,
    VendorInvoiceParameters,
    ClosePeriodParameters,
)


RequestParameters = Union[
    GLBalanceParameters,
    VendorInvoiceParameters,
    ClosePeriodParameters,
]


@dataclass(frozen=True)
class AgentRequest:
    """
    Structured request passed through the enterprise
    multi-agent routing layer.
    """

    domain: str
    request_type: str
    context: FinanceContext
    parameters: RequestParameters


def validate_agent_request(
    request: AgentRequest,
) -> dict[str, object]:
    """
    Validate the structured agent request before routing.
    """

    errors: list[str] = []

    context_validation = validate_finance_context(
        request.context
    )

    if context_validation["status"] != "VALID_CONTEXT":
        errors.extend(context_validation["errors"])

    if not request.domain.strip():
        errors.append("DOMAIN_REQUIRED")

    if not request.request_type.strip():
        errors.append("REQUEST_TYPE_REQUIRED")

    if (
        request.request_type == "gl_balances"
        and not isinstance(
            request.parameters,
            GLBalanceParameters,
        )
    ):
        errors.append(
            "INVALID_PARAMETERS_FOR_GL_BALANCES"
        )

    if (
        request.request_type == "vendor_invoices"
        and not isinstance(
            request.parameters,
            VendorInvoiceParameters,
        )
    ):
        errors.append(
            "INVALID_PARAMETERS_FOR_VENDOR_INVOICES"
        )

    if (
        request.request_type == "close_period"
        and not isinstance(
            request.parameters,
            ClosePeriodParameters,
        )
    ):
        errors.append(
            "INVALID_PARAMETERS_FOR_CLOSE_PERIOD"
        )

    parameter_company_code = getattr(
        request.parameters,
        "company_code",
        None,
    )

    if (
        parameter_company_code is not None
        and parameter_company_code.upper()
        != request.context.company_code.upper()
    ):
        errors.append(
            "PARAMETER_CONTEXT_COMPANY_CODE_MISMATCH"
        )

    if errors:
        return {
            "status": "INVALID_AGENT_REQUEST",
            "errors": errors,
        }

    return {
        "status": "VALID_AGENT_REQUEST",
        "errors": [],
    }