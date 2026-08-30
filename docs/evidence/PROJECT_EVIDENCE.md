\# Enterprise SAP Finance AI Assistant — Project Evidence



\## 1. Project Objective



Build an enterprise-style SAP Finance AI assistant that combines natural-language finance interaction with deterministic finance controls, human-in-the-loop approval, governed workflows, and auditability.



This is a portfolio implementation using simulated SAP Finance services and data. It is not a production SAP deployment.



\## 2. Validated Finance Retrieval



\### General Ledger Balances



Validated natural-language query:



"Show GL balances for company code UK01."



Observed result:



\- GL Account 400000 — Sales Revenue — £425,000 GBP

\- GL Account 610000 — Operating Expenses — £172,000 GBP



\### Overdue Invoice Retrieval



Validated natural-language query:



"Show invoices overdue by more than 30 days."



Observed result:



\- INV-1001 — Vendor V1001 — £12,500 GBP — 41 days overdue

\- INV-1003 — Vendor V1002 — £24,500 GBP — 37 days overdue



\## 3. Invoice Approval Governance



\### Manual Review Scenario



Invoice INV-1001 was evaluated against a £10,000 approval limit.



Observed result:



\- Invoice amount: £12,500

\- Vendor active: PASSED

\- Within approval limit: FAILED

\- Invoice not overdue: FAILED

\- Recommendation: REVIEW



The application explicitly states that the result is an approval recommendation only. No invoice is automatically approved, posted, or paid in SAP.



\### Approval Recommendation Scenario



Invoice INV-1002 was evaluated against a £10,000 approval limit.



Observed result:



\- Invoice amount: £7,800

\- Vendor active: PASSED

\- Within approval limit: PASSED

\- Invoice not overdue: PASSED

\- Recommendation: APPROVE



The recommendation does not automatically execute an SAP transaction.



\## 4. Governed Month-End Close



Validated scenario:



\- Company Code: UK01

\- Fiscal Year: 2026

\- Period: 7

\- Posting Period Status before close: OPEN

\- Close Readiness: READY



Validated close-readiness controls:



\- CLOSE\_CHECKLIST\_COMPLETE — PASSED

\- POSTING\_PERIOD\_OPEN — PASSED

\- TRIAL\_BALANCE\_BALANCED — PASSED

\- AP\_EXCEPTIONS — PASSED

\- JOURNAL\_ACTIVITY — PASSED



The accounting period could only be closed when the period was OPEN and close readiness was READY.



A human approver was required before execution.



Validated close:



\- Action: PERIOD\_CLOSED

\- Approved By: Finance Manager

\- Readiness at Close: READY

\- Audit ID: 8

\- Closed At: 2026-08-29T08:31:30.219627



The resulting close event was persisted in the close audit log.



\## 5. Governance Evidence



The validated implementation demonstrates:



\- deterministic finance controls around AI-assisted workflows;

\- human-in-the-loop approval;

\- separation between AI recommendations and transactional execution;

\- controlled accounting-period close;

\- persisted audit trail;

\- company-code and accounting-period context;

\- explicit control results and failure reasons.



\## 6. Demonstrated End-to-End Flow



Finance data

→ natural-language interaction

→ deterministic finance controls

→ readiness/recommendation

→ human approval where required

→ governed execution

→ persisted audit evidence



\## 7. Evidence Status



Runtime validation: COMPLETE



End-to-end governance validation: COMPLETE



Repository restored after validation: CLEAN



Project evidence packaging: IN PROGRESS

