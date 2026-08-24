from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class FinanceContext:
    """
    Shared enterprise finance context passed between
    agents and governed finance services.
    """

    company_code: str
    fiscal_year: int
    period_number: int
    user_id: str
    user_role: str
    request_id: str


def create_finance_context(
    company_code: str,
    fiscal_year: int,
    period_number: int,
    user_id: str,
    user_role: str,
) -> FinanceContext:
    """
    Create a controlled finance context for one request.
    """

    return FinanceContext(
        company_code=company_code,
        fiscal_year=fiscal_year,
        period_number=period_number,
        user_id=user_id,
        user_role=user_role,
        request_id=str(uuid4()),
    )


def validate_finance_context(
    context: FinanceContext,
) -> dict[str, object]:
    """
    Validate the shared finance context before it is
    passed to agents or governed finance services.
    """

    errors: list[str] = []

    if not context.company_code.strip():
        errors.append("COMPANY_CODE_REQUIRED")

    if context.fiscal_year <= 0:
        errors.append("INVALID_FISCAL_YEAR")

    if context.period_number < 1 or context.period_number > 16:
        errors.append("INVALID_PERIOD_NUMBER")

    if not context.user_id.strip():
        errors.append("USER_ID_REQUIRED")

    if not context.user_role.strip():
        errors.append("USER_ROLE_REQUIRED")

    if not context.request_id.strip():
        errors.append("REQUEST_ID_REQUIRED")

    if errors:
        return {
            "status": "INVALID_CONTEXT",
            "errors": errors,
        }

    return {
        "status": "VALID_CONTEXT",
        "errors": [],
    }