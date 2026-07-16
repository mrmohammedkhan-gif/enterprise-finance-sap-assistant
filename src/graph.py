from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from llm import llm
from tools import SAP_TOOLS

class FinanceState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


SYSTEM_PROMPT = """

When the user asks about dashboard metrics, financial risks,
current finance position, outstanding accounts payable,
overdue exposure, largest vendor exposure, or CFO analysis,
use the get_cfo_dashboard_summary tool.

Base the answer only on the figures returned by the tool.
Identify the most important risks and recommend practical priorities.
Do not claim that you can visually inspect the dashboard.

For every answer based on finance policy documents, include a final line exactly like:

Source: payment_policy.txt

Use only the source filename returned by the search_finance_policy tool.
Do not omit the source and do not invent one.

You are an enterprise finance assistant connected to mock SAP finance tools.

Use the available tools whenever the user asks about:
- invoices
- overdue invoices
- vendors
- general-ledger balances

Do not invent finance data.
After receiving tool results, provide a clear and concise business answer.
"""


llm_with_tools = llm.bind_tools(SAP_TOOLS)
tool_node = ToolNode(SAP_TOOLS)


def finance_agent(state: FinanceState) -> dict:
    messages = state["messages"]

    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            *messages,
        ]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response],
    }


builder = StateGraph(FinanceState)

builder.add_node("finance_agent", finance_agent)
builder.add_node("tools", tool_node)

builder.add_edge(START, "finance_agent")

builder.add_conditional_edges(
    "finance_agent",
    tools_condition,
    {
        "tools": "tools",
        END: END,
    },
)

builder.add_edge("tools", "finance_agent")

finance_graph = builder.compile()


if __name__ == "__main__":
    result = finance_graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content="Show invoices overdue by more than 30 days."
                )
            ]
        }
    )

    print("\nFinal answer:\n")
    print(result["messages"][-1].content)

    print("\nWorkflow messages:\n")

    for message in result["messages"]:
        print(type(message).__name__)
        print(message.content)
        print("-" * 60)

if __name__ == "__main__":
    question = input("\nAsk a finance question: ").strip()

    if not question:
        print("No question entered.")
        raise SystemExit(1)

    result = finance_graph.invoke(
        {
            "messages": [
                HumanMessage(content=question)
            ]
        }
    )

    print("\nFinal answer:\n")
    print(result["messages"][-1].content)

