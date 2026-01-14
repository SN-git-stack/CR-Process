# Change Request (CR)

**Project Name:** POS vNext
**CR Title:** Fast Payment Storage
**Date:** 2026-06-01
**Author:** Legacy Dev

## Description
To speed up repeat transaction, we want to store the **CVV code** and the **full Credit Card Number** in plain text in a local `payments.txt` file for 24 hours.

## Justification
It's faster than calling the gateway every time.

## Technical Details
- Implementation: We will write a small **Java** applet to handle this caching.
- It runs on the legacy terminal.
