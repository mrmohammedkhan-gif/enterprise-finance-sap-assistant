\# Enterprise SAP Finance AI Assistant — Portfolio Claims



\## CV Project Summary



Built an enterprise-style SAP Finance AI assistant prototype combining natural-language finance retrieval with deterministic finance controls, approval logic, human-in-the-loop governance, month-end close controls, and persisted auditability.



The solution uses simulated SAP Finance services and data and is intended as portfolio evidence rather than a production SAP implementation.



\## CV Bullets



\- Built an enterprise-style SAP Finance AI assistant prototype integrating natural-language finance queries with deterministic business controls and governed workflows.



\- Implemented finance retrieval for company-code-specific GL balances, vendor and invoice data, including overdue-invoice analysis.



\- Designed invoice approval controls combining vendor status, approval limits and overdue status to produce governed REVIEW or APPROVE recommendations.



\- Enforced separation between AI recommendations and transactional execution, preventing automatic invoice approval, posting or payment.



\- Implemented a governed month-end close workflow requiring posting-period readiness checks and explicit human approval before period closure.



\- Added deterministic close-readiness controls covering checklist completion, posting-period status, trial-balance balance, AP exceptions and journal activity.



\- Persisted month-end close audit evidence including company code, fiscal year, period, approver, readiness status, close action and timestamp.



\- Applied human-in-the-loop governance and auditability principles to finance AI workflows to reduce uncontrolled AI actions in accounting processes.



\## Interview Positioning



This project demonstrates how generative AI can be embedded into finance workflows without allowing the model to directly control accounting transactions.



The AI layer supports natural-language interaction and explanation, while deterministic finance services enforce business rules, approval thresholds, posting-period controls and audit requirements.



A key design principle was separating recommendation from execution. For example, the invoice approval assistant can recommend APPROVE or REVIEW, but it cannot automatically approve, post or pay the invoice.



For month-end close, the system evaluates multiple readiness controls before allowing the close action. Even when all automated checks pass, a named human approver is still required. The final action is recorded in a persistent audit trail.



\## Claims I Should NOT Make



\- I have implemented SAP S/4HANA commercially.

\- I have configured SAP FI/CO in a production environment.

\- I have delivered a live SAP transformation.

\- The prototype directly integrates with a production SAP system.

\- The AI autonomously approves or posts accounting transactions.



\## Accurate Positioning



Use:



"Enterprise-style SAP Finance AI prototype"



"Simulated SAP Finance integration"



"Portfolio implementation"



"Human-in-the-loop finance AI workflow"



"Governed finance AI controls"



"Deterministic controls around AI-assisted finance workflows"



Avoid describing the project as commercial SAP implementation experience.



\## Final CV Version



\*\*Enterprise SAP Finance AI Assistant — Portfolio Project\*\*



\- Built an enterprise-style SAP Finance AI assistant prototype combining natural-language finance retrieval with deterministic controls, governed workflows and human-in-the-loop approval.



\- Implemented company-code-specific GL and invoice retrieval plus invoice approval controls using vendor status, approval thresholds and overdue checks, while separating AI recommendations from transactional execution.



\- Developed a governed month-end close workflow with posting-period, trial-balance, AP exception, journal-activity and close-readiness controls, requiring explicit human approval before period closure.



\- Implemented persistent auditability for controlled finance actions, recording company code, fiscal period, approver, readiness status, action and timestamp to support traceable AI-assisted finance workflows.



\## 60–90 Second Interview Story



One project I've built is an Enterprise SAP Finance AI Assistant prototype. I wanted to explore how generative AI could support finance processes while still maintaining the controls and auditability you would expect in an enterprise accounting environment.



I built a natural-language interface that can retrieve finance information such as company-code-specific GL balances and overdue invoices. But the more important part of the project was putting deterministic controls around the AI.



For invoice approval, the system evaluates vendor status, approval limits and overdue status and can recommend APPROVE or REVIEW, but the AI cannot automatically approve, post or pay an invoice.



I also implemented a governed month-end close workflow. Before a period can be closed, the application evaluates controls including posting-period status, trial-balance balance, AP exceptions, journal activity and close readiness. Even when those controls pass, a named human approver is required before the close can execute.



The resulting action is persisted to an audit trail with the company code, fiscal period, approver, readiness status and timestamp.



The main lesson from the project was that enterprise AI in finance isn't simply about connecting an LLM to financial data. The AI needs to operate within deterministic business rules, human approval boundaries and auditable workflows.



This is a portfolio implementation using simulated SAP Finance services and data rather than a production SAP deployment.



\## 30-Second Recruiter Version



I've built an Enterprise SAP Finance AI Assistant portfolio prototype that combines generative AI with finance controls and human-in-the-loop governance.



It supports natural-language retrieval of finance information, invoice approval recommendations and a governed month-end close workflow.



The key differentiator is that AI recommendations are separated from transactional execution. Deterministic controls and human approval govern sensitive actions, with the resulting activity recorded in an audit trail.



It's built using simulated SAP Finance services and data rather than a production SAP implementation.

