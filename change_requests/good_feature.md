# Change Request (CR)

**Project Name:** POS vNext
**CR Title:** Integration with UberEats
**Date:** 2026-06-01
**Author:** Product Team

## Description
Integrate UberEats orders directly into the POS queue.
We will use the **Python** backend service to poll the UberEats API.
Customer PII (Name, Address) will be encrypted at rest and masked in the UI.

## Justification
High demand from restaurant partners.

## Technical Details
- Tech Stack: Python, FastAPI.
- Database: PostgreSQL.
- Security: No raw card data touched (handled by Uber).
