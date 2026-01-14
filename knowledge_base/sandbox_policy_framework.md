# Policy Framework: Restricted Developer Sandboxes

## 1. Overview
This framework defines the security, compliance, and lifecycle rules for the "Restricted Developer Sandboxes" initiative. These environments are strictly for **development and testing** of cloud-native patterns and must NOT house production data.

## 2. Identity & Access Management (IAM)
### Entra ID (Azure AD) Scope
*   **Role**: `Application Developer` (Custom Role if needed).
*   **Scope**: Strictly limit to the specific Dev-Tenant/Subscription. **NO** write access to the Root Tenant.
*   **MFA**: Enforced for all users accessing these subscriptions.

## 3. Azure Policy Guardrails
The following policies must be assigned at the Management Group level:

| Policy Area | Restriction | Justification |
| :--- | :--- | :--- |
| **Networking** | **Deny** ExpressRoute Creation | Prevent backdoors to corporate network. |
| **Networking** | **Deny** VPN Gateway Creation | detailed connectivity review required. |
| **Networking** | **Deny** Public IP Creation | Default closed; specific exemptions required. |
| **Compute** | **Allowed SKUs**: B-Series, D-Series (max 4 cores) | Cost control; prevent crypto-mining risks. |
| **Locations** | **Allowed**: West Europe | Data residency compliance. |

## 4. Compliance & Safety Gates
In alignment with our Safety & Compliance priority:

### A. Data Classification
*   **Strictly Prohibited**: Merchant PII, Customer Cardholder Data (PCI-DSS), Real ApplicationSecrets.
*   **Allowed**: Synthetic Data, Mock Data.

### B. Automated Lifecycle (TTL)
*   **Mechanism**: tailored Azure Automation Runbook or Logic App.
*   **Rule**: Tag `CreatedDate`. If `CurrentDate - CreatedDate > 30 days`:
    1.  Send Warning Email (Day 25).
    2.  Stop Resources (Day 29).
    3.  **Delete Resources (Day 30)**.

### C. Observability & Traceability
*   All Activity Logs exported to central **Azure Sentinel** workspace.
*   Alerts triggered on:
    *   Public IP creation attempts.
    *   Role Assignment changes.
    *   Security Group modification.

## 5. Violation Handling
Any attempt to bypass policies or upload Production Data will result in:
1.  Immediate revocation of sandbox access.
2.  Incident report to CISO.
