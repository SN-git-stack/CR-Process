# Change Request (CR)

**Project Name:** Engineering Velocity / Cloud Infrastructure
**CR Title:** Provisioning of Restricted Developer Sandboxes
**Date:** 2026-06-15
**Author:** Engineering Team
**To:** IT Infrastructure / Azure Platform Team
**CC:** CTO, Infrastructure & DevOps Architect

## 1. Problem Statement
Current restrictions on Entra ID and Tenant creation are preventing the Engineering team from testing modern authentication flows, service principal integrations, and automated deployment pipelines.
*   **Impact**: Bottleneck for the DACH Hospitality roadmap.
*   **Specific Blocker**: Unable to test plugin isolation and cloud-security patterns effectively.

## 2. Proposed Solution: The "Guardrail" Sandbox
Instead of total access restriction, we propose the creation of a **Restricted Dev-Sandbox Management Group**.

### Key Features
1.  **Scoped Entra ID Permissions**: Grant "Application Developer" roles within the Dev-Tenant only.
    *   *Goal*: Allow app registration without global directory impact.
2.  **Restricted Subscriptions**: Use Azure Policy to limit resource types.
    *   *Constraints*: No ExpressRoute, No Public IPs (approval required), Limited VM SKUs.
3.  **Isolated Networking**: Zero peering/connectivity to Production or Staging.

## 3. Business Value / Justification
*   **Velocity**: Unblocks the engineering team to test critical auth flows.
*   **Security**: Moving "shadow IT" experiments into a managed, monitored environment.
*   **Innovation**: Enables safe testing of new cloud patterns (DACH roadmap).

## 4. User Acceptance Criteria (UAC)
- [ ] Management Group "Dev-Sandbox" created in Azure.
- [ ] "Application Developer" role assigned to Engineers for this scope only.
- [ ] Azure Policy denies creating ExpressRoute circuits.
- [ ] Azure Policy denies creating Public IPs without exemption.
- [ ] Network Security Groups (NSG) verify isolation from Prod VNETs.

## 5. Technical Context & Safety Gates
*   See `knowledge_base/sandbox_policy_framework.md` for the full compliance framework.
*   **TTL**: All resources auto-delete after 30 days.
*   **Audit**: Connected to Azure Sentinel.
