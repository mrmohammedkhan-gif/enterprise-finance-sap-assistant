\# Enterprise SAP Finance AI Assistant — Demo Script



\## Demo Objective



Demonstrate how the Enterprise SAP Finance AI Assistant supports finance users through AI-assisted analysis, finance workflows, controls, approvals and explainability.



Target demo duration: 5–7 minutes.



\---



\## 1. Introduction — 30 seconds



This project demonstrates how generative AI and agentic workflow concepts can be applied to enterprise finance processes in an SAP-style environment.



The objective was not simply to build a chatbot. The focus was on combining AI with finance-domain logic, business controls, approvals, evaluation and traceability.



\---



\## 2. Architecture — 45 seconds



The solution is structured across several layers:



\- Finance users and user experience

\- FastAPI service layer

\- AI, retrieval and orchestration

\- Finance-domain services

\- SAP-style finance data

\- Governance, controls, evaluation and observability



Finance requests flow through the API and business-logic layers before controlled access to finance data.



AI functionality therefore operates inside the finance control framework rather than bypassing it.



\---



\## 3. Finance Manager Use Case — 1 minute



Demonstrate a Finance Manager requesting financial information or support with month-end close.



Example:



"Show me the current profit and loss position and highlight any areas requiring attention."



Explain that the system retrieves finance data through controlled service endpoints and returns finance-oriented information rather than relying only on unrestricted LLM generation.



Highlight:



\- Finance context

\- Company Code awareness

\- Period awareness

\- Explainability

\- Controlled data access



\---



\## 4. Vendor / Accounts Payable Workflow — 1 minute



Demonstrate vendor invoice or open invoice information.



Example endpoints:



GET /vendor-invoices



GET /vendor-invoices/open



Explain how this supports AP analysis including open items, overdue invoices, vendor exposure and finance review.



The key point is that AI assistance is connected to structured finance services and finance-domain logic.



\---



\## 5. Journal Entry and Posting Controls — 1 minute



Demonstrate the journal-entry workflow.



Example:



POST /journal-entries



Explain that a journal cannot simply be posted because an AI system requests it.



The workflow applies business controls such as:



\- Posting-period validation

\- Finance validation

\- Role-based permissions

\- Approval requirements



This demonstrates the difference between a generic AI assistant and an enterprise finance AI system.



\---



\## 6. Approval, Security and Guardrails — 45 seconds



Explain the governance layer.



The project includes concepts such as:



\- Role-Based Access Control

\- Least privilege

\- Trusted approval workflows

\- Human oversight

\- Input guardrails

\- Output guardrails

\- Auditability and traceability



The AI operates within these controls rather than having unrestricted authority over finance transactions.



\---



\## 7. Evaluation and Observability — 45 seconds



Explain that AI quality should be measured rather than judged only by whether the output sounds convincing.



The project covers evaluation concepts including:



\- Precision

\- Recall

\- Mean Reciprocal Rank

\- nDCG

\- Retrieval quality at K

\- Response evaluation



Observability and traceability concepts allow AI behaviour and system activity to be reviewed.



\---



\## 8. Closing — 30 seconds



The main lesson from this project is that enterprise AI in finance is not just an LLM integration problem.



A useful enterprise solution must combine:



AI + finance-domain knowledge + APIs + business controls + approvals + security + evaluation + observability.



The completed project demonstrates how those elements can be brought together into one finance-focused architecture.

