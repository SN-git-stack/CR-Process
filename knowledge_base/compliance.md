# Security & Compliance Rules (PCI-DSS)

## 1. Card Data Storage
- **NEVER** store CVV/CVC codes.
- **NEVER** store full PAN (Primary Account Number) unencrypted.
- Mask PAN everywhere except for authorized backend processors (display only last 4).

## 2. PII (GDPR/CCPA)
- Customer data (Name, Email, Phone) must be encrypted at rest.
- Right to be Forgotten: System must support hard-deletion of customer profiles.
