import sqlite3
from pathlib import Path
from typing import Any


DATABASE_PATH = Path("data") / "finance_controls.db"


def get_connection() -> sqlite3.Connection:
    """
    Return a SQLite connection for finance-control data.
    """
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialise_close_database() -> None:
    """
    Create persistent tables required for posting-period
    control and month-end close audit history.
    """
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS close_tasks (
                task_id TEXT PRIMARY KEY,
                company_code TEXT NOT NULL,
                fiscal_year INTEGER NOT NULL,
                period_number INTEGER NOT NULL,
                task_name TEXT NOT NULL,
                status TEXT NOT NULL,
                owner TEXT NOT NULL,
                completed_by TEXT,
                completed_at TEXT
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS close_audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_code TEXT NOT NULL,
                fiscal_year INTEGER NOT NULL,
                period_number INTEGER NOT NULL,
                action TEXT NOT NULL,
                approved_by TEXT NOT NULL,
                action_at TEXT NOT NULL,
                readiness_status TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS close_audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_code TEXT NOT NULL,
                fiscal_year INTEGER NOT NULL,
                period_number INTEGER NOT NULL,
                action TEXT NOT NULL,
                approved_by TEXT NOT NULL,
                action_at TEXT NOT NULL,
                readiness_status TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS approval_requests (
                request_id TEXT PRIMARY KEY,
                tool_name TEXT NOT NULL,
                company_code TEXT NOT NULL,
                requested_by TEXT NOT NULL,
                status TEXT NOT NULL,
                approved_by TEXT,
                created_at TEXT NOT NULL,
                approved_at TEXT
            )
            """
        )
    finally:
        connection.close()


def save_posting_period(
    company_code: str,
    fiscal_year: int,
    period_number: int,
    status: str,
    opened_at: str | None,
    closed_at: str | None,
) -> None:
    """
    Insert or update a posting-period record.
    """
    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO posting_periods (
                company_code,
                fiscal_year,
                period_number,
                status,
                opened_at,
                closed_at
            )
            VALUES (?, ?, ?, ?, ?, ?)

            ON CONFLICT (
                company_code,
                fiscal_year,
                period_number
            )
            DO UPDATE SET
                status = excluded.status,
                opened_at = excluded.opened_at,
                closed_at = excluded.closed_at
            """,
            (
                company_code.upper(),
                fiscal_year,
                period_number,
                status.upper(),
                opened_at,
                closed_at,
            ),
        )

        connection.commit()

    finally:
        connection.close()


def get_persisted_posting_period(
    company_code: str,
    fiscal_year: int,
    period_number: int,
) -> dict[str, Any] | None:
    """
    Return one persisted posting-period record.
    """
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                company_code,
                fiscal_year,
                period_number,
                status,
                opened_at,
                closed_at
            FROM posting_periods
            WHERE company_code = ?
              AND fiscal_year = ?
              AND period_number = ?
            """,
            (
                company_code.upper(),
                fiscal_year,
                period_number,
            ),
        ).fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()


def add_close_audit_record(
    company_code: str,
    fiscal_year: int,
    period_number: int,
    action: str,
    approved_by: str,
    action_at: str,
    readiness_status: str,
) -> int:
    """
    Persist one month-end close audit record.
    """
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO close_audit_log (
                company_code,
                fiscal_year,
                period_number,
                action,
                approved_by,
                action_at,
                readiness_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                company_code.upper(),
                fiscal_year,
                period_number,
                action,
                approved_by,
                action_at,
                readiness_status,
            ),
        )

        connection.commit()

        return int(cursor.lastrowid)

    finally:
        connection.close()


def get_close_audit_history(
    company_code: str | None = None,
) -> list[dict[str, Any]]:
    """
    Return persisted month-end close audit history.
    """
    connection = get_connection()

    try:
        if company_code:
            rows = connection.execute(
                """
                SELECT
                    id,
                    company_code,
                    fiscal_year,
                    period_number,
                    action,
                    approved_by,
                    action_at,
                    readiness_status
                FROM close_audit_log
                WHERE company_code = ?
                ORDER BY action_at DESC
                """,
                (
                    company_code.upper(),
                ),
            ).fetchall()

        else:
            rows = connection.execute(
                """
                SELECT
                    id,
                    company_code,
                    fiscal_year,
                    period_number,
                    action,
                    approved_by,
                    action_at,
                    readiness_status
                FROM close_audit_log
                ORDER BY action_at DESC
                """
            ).fetchall()

        return [
            dict(row)
            for row in rows
        ]

    finally:
        connection.close()

def save_close_task(
    task: dict[str, Any],
) -> None:
    """
    Insert or update one month-end close task.
    """
    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO close_tasks (
                task_id,
                company_code,
                fiscal_year,
                period_number,
                task_name,
                status,
                owner,
                completed_by,
                completed_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT (task_id)
            DO UPDATE SET
                company_code = excluded.company_code,
                fiscal_year = excluded.fiscal_year,
                period_number = excluded.period_number,
                task_name = excluded.task_name,
                status = excluded.status,
                owner = excluded.owner,
                completed_by = excluded.completed_by,
                completed_at = excluded.completed_at
            """,
            (
                task["task_id"],
                task["company_code"],
                task["fiscal_year"],
                task["period_number"],
                task["task_name"],
                task["status"],
                task["owner"],
                task["completed_by"],
                task["completed_at"],
            ),
        )

        connection.commit()

    finally:
        connection.close()


def get_persisted_close_tasks(
    company_code: str,
    fiscal_year: int,
    period_number: int,
) -> list[dict[str, Any]]:
    """
    Return persisted close tasks for one accounting period.
    """
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                task_id,
                company_code,
                fiscal_year,
                period_number,
                task_name,
                status,
                owner,
                completed_by,
                completed_at
            FROM close_tasks
            WHERE company_code = ?
              AND fiscal_year = ?
              AND period_number = ?
            ORDER BY task_id
            """,
            (
                company_code.upper(),
                fiscal_year,
                period_number,
            ),
        ).fetchall()

        return [
            dict(row)
            for row in rows
        ]

    finally:
        connection.close()

def get_persisted_close_task(
    task_id: str,
) -> dict[str, Any] | None:
    """
    Return one persisted month-end close task by task ID.
    """
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                task_id,
                company_code,
                fiscal_year,
                period_number,
                task_name,
                status,
                owner,
                completed_by,
                completed_at
            FROM close_tasks
            WHERE task_id = ?
            """,
            (
                task_id.upper(),
            ),
        ).fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()