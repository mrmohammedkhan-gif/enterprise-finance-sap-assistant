import json

import pandas as pd

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from graph import finance_graph
from sap_client import SAPClient
from tools import review_invoice_for_approval



st.set_page_config(
    page_title="Enterprise Finance AI Assistant",
    page_icon="💼",
    layout="wide",
)

st.title("💼 Enterprise Finance AI Assistant")
st.caption("LangChain + LangGraph + Mock SAP Finance API")


sap_client = SAPClient()


def load_dashboard_data() -> dict:
    invoices = sap_client.get_invoices()
    overdue_invoices = sap_client.get_overdue_invoices(1)

    open_invoices = [
        invoice
        for invoice in invoices
        if invoice["status"] == "OPEN"
    ]

    outstanding_ap = sum(
        invoice["amount"]
        for invoice in invoices
        if invoice["status"] in {"OPEN", "OVERDUE"}
    )

    vendor_exposure: dict[str, float] = {}

    for invoice in invoices:
        if invoice["status"] in {"OPEN", "OVERDUE"}:
            vendor_id = invoice["vendor_id"]
            vendor_exposure[vendor_id] = (
                vendor_exposure.get(vendor_id, 0.0)
                + invoice["amount"]
            )

    largest_exposure = max(
        vendor_exposure.values(),
        default=0.0,
    )

    return {
        "outstanding_ap": outstanding_ap,
        "open_invoice_count": len(open_invoices),
        "overdue_invoice_count": len(overdue_invoices),
        "largest_exposure": largest_exposure,
    }

def run_finance_assistant(question: str) -> str:
    result = finance_graph.invoke(
        {
            "messages": [
                HumanMessage(content=question)
            ]
        }
    )

    final_message = result["messages"][-1]

    if isinstance(final_message, AIMessage):
        return str(final_message.content)

    return str(final_message)


try:
    dashboard_data = load_dashboard_data()

    st.subheader("CFO Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Outstanding AP",
            value=f"£{dashboard_data['outstanding_ap']:,.0f}",
        )

    with col2:
        st.metric(
            label="Open invoices",
            value=dashboard_data["open_invoice_count"],
        )

    with col3:
        st.metric(
            label="Overdue invoices",
            value=dashboard_data["overdue_invoice_count"],
        )

    with col4:
        st.metric(
            label="Largest vendor exposure",
            value=f"£{dashboard_data['largest_exposure']:,.0f}",
        )

except Exception:
    st.warning(
        "Dashboard data is unavailable. "
        "Check that the Mock SAP API is running."
    )


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


with st.sidebar:
    st.header("Example questions")

    st.markdown(
        """
- Show invoices overdue by more than 30 days.
- Show open invoices above £5,000.
- Who is vendor V1001?
- Show GL balances for company code UK01.
"""
    )

    if st.button("Clear conversation"):
        st.session_state.chat_history = []
        st.rerun()


for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a finance question")

if question:
    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Querying finance data..."):
                answer = run_finance_assistant(question)

            st.markdown(answer)

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

        except Exception as exc:
            st.error(
                "The finance request failed. "
                "Check that the Mock SAP API is running."
            )
            st.exception(exc)


st.subheader("Invoice Overview")

try:
    invoice_data = sap_client.get_invoices()

    invoice_table = pd.DataFrame(invoice_data)

    if not invoice_table.empty:
        invoice_table = invoice_table.rename(
            columns={
                "invoice_id": "Invoice",
                "vendor_id": "Vendor",
                "amount": "Amount",
                "currency": "Currency",
                "invoice_date": "Invoice Date",
                "due_date": "Due Date",
                "status": "Status",
                "days_overdue": "Days Overdue",
            }
        )

        invoice_table["Amount"] = invoice_table["Amount"].map(
            lambda value: f"£{value:,.2f}"
        )

        st.dataframe(
            invoice_table,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No invoice data is available.")

except Exception:
    st.warning(
        "Invoice data is unavailable. "
        "Check that the Mock SAP API is running."
    )

st.subheader("Finance Analytics")

try:
    chart_data = sap_client.get_invoices()
    chart_df = pd.DataFrame(chart_data)

    if not chart_df.empty:
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("#### Outstanding Amount by Vendor")

            vendor_amounts = (
                chart_df.groupby("vendor_id", as_index=False)["amount"]
                .sum()
                .rename(
                    columns={
                        "vendor_id": "Vendor",
                        "amount": "Outstanding Amount",
                    }
                )
            )

            st.bar_chart(
                vendor_amounts,
                x="Vendor",
                y="Outstanding Amount",
                use_container_width=True,
            )

        with chart_col2:
            st.markdown("#### Invoice Count by Status")

            status_counts = (
                chart_df.groupby("status")
                .size()
                .reset_index(name="Invoice Count")
                .rename(columns={"status": "Status"})
            )

            st.bar_chart(
                status_counts,
                x="Status",
                y="Invoice Count",
                use_container_width=True,
            )

    else:
        st.info("No finance data is available for charts.")

except Exception:
    st.warning(
        "Finance charts are unavailable. "
        "Check that the Mock SAP API is running."
    )

st.subheader("Invoice Approval Review")

try:
    approval_invoices = sap_client.get_invoices()

    invoice_options = [
        invoice["invoice_id"]
        for invoice in approval_invoices
    ]

    approval_col1, approval_col2 = st.columns(2)

    with approval_col1:
        selected_invoice = st.selectbox(
            "Select invoice",
            options=invoice_options,
        )

    with approval_col2:
        approval_limit = st.number_input(
            "Approval limit (£)",
            min_value=0.0,
            value=10000.0,
            step=1000.0,
        )

    if st.button(
        "Review invoice",
        type="primary",
        use_container_width=True,
    ):
        raw_result = review_invoice_for_approval.invoke(
            {
                "invoice_id": selected_invoice,
                "approval_limit": approval_limit,
            }
        )

        approval_result = json.loads(raw_result)

        recommendation = approval_result["recommendation"]
        reason = approval_result["reason"]
        invoice = approval_result["invoice"]
        vendor = approval_result["vendor"]
        checks = approval_result["checks"]

        st.markdown("#### Approval recommendation")

        if recommendation == "APPROVE":
            st.success(f"APPROVE — {reason}")
        elif recommendation == "REJECT":
            st.error(f"REJECT — {reason}")
        else:
            st.warning(f"REVIEW — {reason}")

        result_col1, result_col2, result_col3 = st.columns(3)

        with result_col1:
            st.metric(
                "Invoice amount",
                f"£{invoice['amount']:,.2f}",
            )

        with result_col2:
            st.metric(
                "Vendor",
                vendor["name"],
            )

        with result_col3:
            st.metric(
                "Invoice status",
                invoice["status"],
            )

        check_table = pd.DataFrame(
            [
                {
                    "Check": "Vendor is active",
                    "Result": (
                        "Passed"
                        if checks["vendor_active"]
                        else "Failed"
                    ),
                },
                {
                    "Check": "Within approval limit",
                    "Result": (
                        "Passed"
                        if checks["within_approval_limit"]
                        else "Failed"
                    ),
                },
                {
                    "Check": "Invoice is not overdue",
                    "Result": (
                        "Passed"
                        if checks["invoice_not_overdue"]
                        else "Failed"
                    ),
                },
            ]
        )

        st.dataframe(
            check_table,
            use_container_width=True,
            hide_index=True,
        )

        st.info(
            "This is an approval recommendation only. "
            "No invoice has been approved, posted or paid in SAP."
        )

except Exception as exc:
    st.warning(
        "The approval panel is unavailable. "
        "Check that the Mock SAP API is running."
    )

# ---------------------------------------------------------
# MONTH-END CLOSE MANAGER
# ---------------------------------------------------------

st.divider()
st.subheader("Month-End Close Manager")

close_col1, close_col2, close_col3 = st.columns(3)

with close_col1:
    close_company_code = st.text_input(
        "Company Code",
        value="UK01",
        key="close_company_code",
    ).upper()

with close_col2:
    close_fiscal_year = st.number_input(
        "Fiscal Year",
        min_value=2020,
        max_value=2100,
        value=2027,
        step=1,
        key="close_fiscal_year",
    )

with close_col3:
    close_period_number = st.number_input(
        "Period",
        min_value=1,
        max_value=12,
        value=1,
        step=1,
        key="close_period_number",
    )


try:
    posting_period = sap_client.get_posting_period(
        company_code=close_company_code,
        fiscal_year=int(close_fiscal_year),
        period=int(close_period_number),
    )

    posting_status = posting_period["status"]

except Exception:
    posting_status = "NOT CONFIGURED"


try:
    readiness = sap_client.get_close_readiness(
        company_code=close_company_code,
        fiscal_year=int(close_fiscal_year),
        period_number=int(close_period_number),
    )

    readiness_status = readiness["status"]

except Exception:
    readiness = {
        "status": "UNAVAILABLE",
        "checks": [],
        "blockers": [],
    }

    readiness_status = "UNAVAILABLE"


status_col1, status_col2 = st.columns(2)

with status_col1:
    st.metric(
        "Posting Period Status",
        posting_status,
    )

with status_col2:
    st.metric(
        "Close Readiness",
        readiness_status,
    )


if readiness_status == "READY":
    st.success(
        "All close-readiness controls have passed."
    )

elif readiness_status == "NOT_READY":
    st.warning(
        "The accounting period is not ready to close."
    )

else:
    st.info(
        "Close-readiness information is currently unavailable."
    )


st.markdown("#### Close Readiness Controls")

checks = readiness.get("checks", [])

if checks:
    checks_table = pd.DataFrame(
        [
            {
                "Control": check["check"],
                "Result": (
                    "PASSED"
                    if check["passed"]
                    else "FAILED"
                ),
                "Message": check["message"],
            }
            for check in checks
        ]
    )

    st.dataframe(
        checks_table,
        use_container_width=True,
        hide_index=True,
    )

else:
    st.info(
        "No close-readiness controls are available "
        "for the selected period."
    )


blockers = readiness.get("blockers", [])

if posting_status.upper() == "CLOSED":
    st.info(
        "This period is already closed. "
        "Current close-readiness blockers are not applicable."
    )

elif blockers:
    st.markdown("#### Close Blockers")

    for blocker in blockers:
        st.error(
            f"{blocker['check']}: {blocker['message']}"
        )

st.markdown("#### Month-End Close Checklist")

try:
    close_task_response = sap_client.get_close_tasks(
        company_code=close_company_code,
        fiscal_year=int(close_fiscal_year),
        period_number=int(close_period_number),
    )

    close_tasks = close_task_response.get(
        "tasks",
        [],
    )

    if close_tasks:
        for task in close_tasks:
            task_col1, task_col2, task_col3 = st.columns(
                [4, 2, 2]
            )

            with task_col1:
                st.write(
                    f"**{task['task_name']}**"
                )

                st.caption(
                    f"Owner: {task['owner']}"
                )

            with task_col2:
                if task["status"] == "COMPLETED":
                    st.success("COMPLETED")
                else:
                    st.warning(task["status"])

            with task_col3:
                if task["status"] != "COMPLETED":
                    if st.button(
                        "Complete",
                        key=f"complete_{task['task_id']}",
                    ):
                        try:
                            sap_client.complete_close_task(
                                task_id=task["task_id"],
                                completed_by=task["owner"],
                            )

                            st.success(
                                f"{task['task_name']} completed."
                            )

                            st.rerun()

                        except Exception as exc:
                            st.error(
                                "The close task could not "
                                "be completed."
                            )

                            st.exception(exc)

                else:
                    completed_by = (
                        task.get("completed_by")
                        or "Unknown"
                    )

                    st.caption(
                        f"Completed by: {completed_by}"
                    )

    else:
        st.info(
            "No close tasks are configured "
            "for this accounting period."
        )

except Exception as exc:
    st.warning(
        "Close checklist data is unavailable."
    )

    st.exception(exc)


st.markdown("#### Human Approval and Period Close")

if posting_status.upper() == "CLOSED":
    st.success(
        "This accounting period is already closed."
    )

    try:
        audit_response = sap_client.get_close_audit(
            close_company_code
        )

        audit_history = audit_response.get(
            "audit_history",
            [],
        )

        matching_close = next(
            (
                record
                for record in audit_history
                if record["company_code"] == close_company_code
                and record["fiscal_year"] == int(close_fiscal_year)
                and record["period_number"] == int(close_period_number)
                and record["action"] == "PERIOD_CLOSED"
            ),
            None,
        )

        if matching_close:
            summary_col1, summary_col2, summary_col3 = st.columns(3)

            with summary_col1:
                st.metric(
                    "Approved By",
                    matching_close["approved_by"],
                )

            with summary_col2:
                st.metric(
                    "Readiness at Close",
                    matching_close["readiness_status"],
                )

            with summary_col3:
                st.metric(
                    "Audit ID",
                    matching_close["id"],
                )

            st.caption(
                f"Closed at: {matching_close['action_at']}"
            )

    except Exception:
        st.info(
            "The period is closed, but the close summary "
            "could not be loaded."
        )

else:
    approver = st.text_input(
        "Approved By",
        placeholder="Finance Manager",
        key="period_close_approver",
    )

    close_disabled = (
        readiness_status != "READY"
        or posting_status.upper() != "OPEN"
    )

    if st.button(
        "Close Accounting Period",
        type="primary",
        disabled=close_disabled,
        key="close_accounting_period",
    ):
        try:
            if not approver.strip():
                st.error(
                    "A human approver is required."
                )

            else:
                close_result = (
                    sap_client.close_accounting_period(
                        company_code=close_company_code,
                        fiscal_year=int(close_fiscal_year),
                        period_number=int(
                            close_period_number
                        ),
                        approved_by=approver,
                    )
                )

                st.success(
                    "Accounting period closed successfully."
                )

                st.json(close_result)

                st.rerun()

        except Exception as exc:
            st.error(
                "The accounting period could not be closed."
            )

            st.exception(exc)