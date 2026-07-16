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