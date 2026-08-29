\# Enterprise SAP Finance AI Assistant — Interview Story



\## 30-Second Summary



I built an Enterprise SAP Finance AI Assistant portfolio project to explore how generative AI can be integrated into realistic finance processes rather than operating as a standalone chatbot.



I combined Python and FastAPI with SAP-style finance domain logic, RAG and agentic workflow concepts, while incorporating controls such as posting-period validation, approvals, RBAC, guardrails, evaluation and traceability.



The main lesson was that enterprise finance AI is as much a governance and systems-integration problem as it is an LLM problem.



\---



\## 2–3 Minute Interview Story



\### Situation



My background is in finance, and I wanted to understand how generative AI could realistically operate inside an enterprise finance environment.



A basic chatbot was not sufficient because finance processes require structured data, business rules, permissions, approvals and auditability.



I therefore created an Enterprise SAP Finance AI Assistant portfolio project using an SAP-style finance environment.



\### Task



My objective was to design and build an end-to-end prototype that could support finance use cases while respecting enterprise controls.



I focused on areas including:



\- Accounts Payable

\- Accounts Receivable

\- General Ledger

\- Tax

\- Journal entries

\- Month-end close

\- Finance analysis



The challenge was to connect AI capabilities to finance-domain services without allowing the AI to bypass financial controls.



\### Action



I built the application primarily using Python and FastAPI.



I created finance-domain services and REST endpoints covering areas such as profit and loss, vendor invoices, open items, company codes, posting periods and journal entries.



I then incorporated AI and retrieval concepts so that finance users could interact with those services through an AI-assisted workflow.



I added controls including:



\- Posting-period validation

\- Role-Based Access Control

\- Approval workflows

\- Input and output guardrails

\- Human oversight



I also worked on retrieval and response evaluation using concepts including Precision, Recall, Mean Reciprocal Rank and nDCG.



Finally, I structured the solution into a layered architecture covering the user experience, APIs, AI orchestration, finance services, data, governance and observability.



\### Result



The result was a completed 24-module portfolio implementation demonstrating how AI can be combined with finance-domain logic and enterprise controls.



The most important outcome for me was understanding that a finance AI solution cannot simply give an LLM unrestricted access to financial systems.



The AI layer needs to operate through controlled services with validation, permissions, approvals, evaluation and traceability.



\---



\## What I Personally Built



I personally worked through the implementation of:



\- Python application logic

\- FastAPI finance services

\- SAP-style finance domain models

\- AP and AR workflows

\- Journal-entry processing

\- Posting-period controls

\- Approval workflows

\- RBAC and guardrails

\- Retrieval/evaluation concepts

\- Agentic workflow patterns

\- Git-based development and version control

\- Architecture and portfolio documentation



\---



\## Important Scope Clarification



This is a hands-on portfolio implementation and not a live client SAP deployment.



The SAP environment and finance entities are modelled to reflect enterprise finance concepts.



Production SAP integration, enterprise-scale deployment and commercial user adoption would be subsequent implementation stages.



\---



\## Key Interview Message



The project allowed me to combine my finance background with hands-on AI engineering.



Rather than approaching the problem purely as an AI developer, I approached it from both sides:



\*\*What can the AI do?\*\*



and



\*\*What should a controlled finance system allow the AI to do?\*\*



That distinction drove the architecture of the project.

