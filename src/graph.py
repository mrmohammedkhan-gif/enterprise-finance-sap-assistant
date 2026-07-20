from typing import Annotated, TypedDict

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

try:
    from src.llm import llm
    from src.tools import SAP_TOOLS
except ModuleNotFoundError:
    from llm import llm
    from tools import SAP_TOOLS

class FinanceState(TypedDict):
    """
    State passed between nodes in the finance workflow.

    add_messages keeps the existing conversation and appends
    new assistant and tool messages.
    """

    messages: Annotated[list[BaseMessage], add_messages]


SYSTEM_PROMPT = """
You are an Enterprise Finance AI Assistant connected to mock SAP Finance
systems and finance-policy documents.

Your role is to help finance users understand SAP Finance data, identify
financial risks, explain exceptions and provide recommendations.

Use the available tools whenever the user asks about:

- invoices
- overdue invoices
- invoice approval
- vendors
- business partners
- supplier status
- payment blocks
- company codes
- posting periods
- general-ledger balances
- purchase orders
- purchase-order approval
- goods receipts
- invoice receipts
- three-way matching
- Accounts Payable invoices
- blocked AP invoices
- duplicate invoices
- parked invoices
- invoice payment readiness
- payment proposals
- CFO dashboard metrics
- financial risks
- finance policies

ACCOUNTS PAYABLE RULES

When the user asks why an AP invoice is blocked, cannot be paid,
or is not ready for payment:

- Use explain_ap_invoice_status.
- Explain each failed check in clear finance language.
- Consider invoice status, invoice payment block, duplicate status,
  matching status, supplier status, supplier payment block,
  purchase-order approval and goods receipt.

When the user asks whether an invoice is ready for payment:

- Use explain_ap_invoice_status.
- Do not rely only on the invoice amount or due date.
- State either READY FOR PAYMENT or NOT READY FOR PAYMENT.

When the user asks which invoices are ready for payment,
requests a payment run or asks for a payment proposal:

- Use generate_payment_proposal.
- Make clear that the result is a simulated proposal.
- Never state that a real payment has been executed.
- Never claim that money has been transferred.

When the user asks about duplicate AP invoices:

- Use the available AP invoice or duplicate-invoice tools.
- Treat duplicate invoices as requiring investigation.
- Never recommend paying an invoice flagged as DUPLICATE.

PURCHASE ORDER AND MATCHING RULES

When the user asks about a purchase order:

- Use get_purchase_order or list_purchase_orders.

When the user asks whether a purchase order is ready for invoice matching:

- Use check_purchase_order_invoice_match.
- Consider PO approval, goods receipt, invoice-receipt status,
  supplier status and supplier payment block.

When discussing three-way matching, compare:

1. Purchase order
2. Goods receipt
3. Supplier invoice

Do not describe an invoice as successfully matched unless the tool result
supports that conclusion.

BUSINESS PARTNER RULES

When the user asks whether a supplier can receive payment:

- Use check_business_partner_payment.
- Consider whether the partner is a vendor, whether it is active,
  and whether it has a payment block.

SAP ORGANISATION RULES

When the user asks about a company code:

- Use get_company_code.

When the user asks whether a journal, invoice or finance document can
be posted in a period:

- Use check_posting_period.
- Do not recommend posting into a closed period.

CFO AND FINANCE ANALYSIS RULES

When the user asks about:

- dashboard metrics
- financial risks
- current finance position
- outstanding Accounts Payable
- overdue exposure
- largest vendor exposure
- CFO analysis

use get_cfo_dashboard_summary.

Base the answer only on figures returned by the tool.

Identify the most important risks and recommend practical priorities.

Do not claim that you visually inspected a dashboard unless the relevant
data was returned by a tool.

FINANCE POLICY RULES

When the user asks about company finance policies, approval policies,
payment policies, travel policies or finance procedures:

- Use search_finance_policy.
- Base the answer only on the returned policy content.
- Include a final source line using the filename returned by the tool.

The final line must use this format:

Source: <source filename>

Do not invent a source filename.

GENERAL SAFETY AND RESPONSE RULES

- Use tools instead of guessing whenever relevant SAP or finance data is
  required.
- Do not invent invoices, vendors, company codes, balances, purchase
  orders, business partners or policy information.
- Do not approve, post or pay transactions.
- Approval decisions and payment proposals are recommendations or
  simulations only.
- Clearly distinguish facts returned by tools from recommendations.
- Explain exceptions and failed checks in plain business language.
- Provide a clear and concise final answer after receiving tool results.
"""


llm_with_tools = llm.bind_tools(SAP_TOOLS)

tool_node = ToolNode(SAP_TOOLS)


def finance_agent(
    state: FinanceState,
) -> dict[str, list[BaseMessage]]:
    """
    Send the conversation to the language model.

    The system prompt gives the model its finance role and tells it
    which SAP tools to use for different types of questions.
    """

    conversation: list[BaseMessage] = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"],
    ]

    response = llm_with_tools.invoke(conversation)

    return {
        "messages": [response],
    }


workflow = StateGraph(FinanceState)

workflow.add_node(
    "finance_agent",
    finance_agent,
)

workflow.add_node(
    "tools",
    tool_node,
)

workflow.add_edge(
    START,
    "finance_agent",
)

workflow.add_conditional_edges(
    "finance_agent",
    tools_condition,
    {
        "tools": "tools",
        END: END,
    },
)

workflow.add_edge(
    "tools",
    "finance_agent",
)

finance_graph = workflow.compile()


def ask_finance_assistant(
    question: str,
) -> str:
    """
    Run a natural-language finance question through LangGraph.

    The graph allows the model to call one or more SAP tools before
    returning its final business answer.
    """

    clean_question = question.strip()

    if not clean_question:
        raise ValueError(
            "A finance question must be provided."
        )

    result = finance_graph.invoke(
        {
            "messages": [
                HumanMessage(content=clean_question),
            ]
        }
    )

    final_message = result["messages"][-1]

    return str(final_message.content)


def run_interactive_chat() -> None:
    """
    Run the finance assistant from PowerShell.

    Type a finance question and the graph will choose and execute
    the appropriate SAP tools.
    """

    print("\nEnterprise Finance AI Assistant")
    print("-" * 40)
    print("Type 'exit' to stop.\n")

    while True:
        question = input(
            "Ask a finance question: "
        ).strip()

        if question.lower() in {
            "exit",
            "quit",
            "stop",
        }:
            print("Finance assistant stopped.")
            break

        if not question:
            print("Please enter a finance question.\n")
            continue

        try:
            answer = ask_finance_assistant(question)

            print("\nFinal answer:\n")
            print(answer)
            print("\n" + "-" * 60 + "\n")

        except Exception as error:
            print(
                "\nThe finance assistant encountered an error:"
            )
            print(str(error))
            print()


if __name__ == "__main__":
    run_interactive_chat()