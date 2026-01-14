# Change Request (CR)

**Project Name:** POS vNext
**CR Title:** Offline Payment Processing (Store-and-Forward)
**Date:** 2026-05-12
**Author:** Jane Doe

## 1. Description
Allow the POS terminal to accept credit card payments even when the internet connection is lost. The transactions should be stored locally (encrypted) and forwarded to the payment gateway once connectivity is restored.

## 2. Business Value / Justification
*   **Reduced Lost Sales**: Currently, we cannot accept cards during outages, losing approx €5k/month per store in unstable regions.
*   **Customer Satisfaction**: Faster checkout during minor flickers.

## 3. User Acceptance Criteria (UAC)
- [ ] Cashier sees a "Offline Mode" indicator.
- [ ] Transaction is approved locally below a configurable floor limit (e.g., $50).
- [ ] Data is encrypted at rest using AES-256.
- [ ] Auto-sync triggers when connection is restored.

## 4. Technical Context
*   Target Hardware: Elo TouchPOS & iPad.
*   Gateway: Adyen (supports offline authorization).

## 5. Mockups / Visuals
*   N/A
