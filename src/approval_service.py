from datetime import datetime
from typing import Any
from uuid import uuid4

from src.close_persistence import get_connection


def create_approval_request(
    tool_name: str,
    company_code: str,
    requested_by: str,
) -> dict[str, Any]:
    """
    Create and persist a trusted approval request
    for a sensitive finance action.
    """

    request_id = str(uuid4())
    created_at = datetime.now().isoformat()

    approval_request = {
        "request_id": request_id,
        "tool_name": tool_name,
        "company_code": company_code.upper(),
        "requested_by": requested_by,
        "status": "PENDING",
        "approved_by": None,
        "created_at": created_at,
        "approved_at": None,
    }

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO approval_requests (
                request_id,
                tool_name,
                company_code,
                requested_by,
                status,
                approved_by,
                created_at,
                approved_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                approval_request["request_id"],
                approval_request["tool_name"],
                approval_request["company_code"],
                approval_request["requested_by"],
                approval_request["status"],
                approval_request["approved_by"],
                approval_request["created_at"],
                approval_request["approved_at"],
            ),
        )

        connection.commit()

    finally:
        connection.close()

    return approval_request


def get_approval_request(
    request_id: str,
) -> dict[str, Any] | None:
    """
    Return one persisted approval request.
    """

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                request_id,
                tool_name,
                company_code,
                requested_by,
                status,
                approved_by,
                created_at,
                approved_at
            FROM approval_requests
            WHERE request_id = ?
            """,
            (
                request_id,
            ),
        ).fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()


def approve_request(
    request_id: str,
    approved_by: str,
) -> dict[str, Any]:
    """
    Approve one persisted finance approval request.
    """

    approved_by = approved_by.strip()

    if not approved_by:
        raise ValueError(
            "An approver identity is required."
        )

    approval_request = get_approval_request(
        request_id
    )

    if approval_request is None:
        raise ValueError(
            f"Approval request {request_id} was not found."
        )

    approved_at = datetime.now().isoformat()

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE approval_requests
            SET
                status = ?,
                approved_by = ?,
                approved_at = ?
            WHERE request_id = ?
            """,
            (
                "APPROVED",
                approved_by,
                approved_at,
                request_id,
            ),
        )

        connection.commit()

    finally:
        connection.close()

    updated_request = get_approval_request(
        request_id
    )

    if updated_request is None:
        raise ValueError(
            f"Approval request {request_id} could not be reloaded."
        )

    return updated_request


def is_request_approved(
    request_id: str,
) -> bool:
    """
    Return True only when the persisted request exists
    and has status APPROVED.
    """

    approval_request = get_approval_request(
        request_id
    )

    if approval_request is None:
        return False

    return approval_request["status"] == "APPROVED"