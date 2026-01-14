# Feasibility Check: Universal Middleware for Dishware Providers

**Project Name:** Multipath Dishware Integration
**CR Title:** Feasibility of Single Middleware Strategy
**Date:** 2026-01-14
**Author:** Lead Engineer

## 1. Questions for the System Architect
We want to integrate **multiple dishware providers** (UberEats, Lieferando, Wolt, etc.) via a **single Middleware/Gateway** component.
*   **Feasibility**: Is this architecture viable?
*   **Risks**: What are the bottlenecks of funneling all traffic through one middleware?
*   **Patterns**: Should we use an API Gateway (Kong/Tyk) or a custom "Adapter Service"?

## 2. Technical Context
*   **Goal**: Decouple the Core POS logic from provider-specific APIs.
*   **Volume**: approx. 50k transactions/day across all providers.
*   **Latency Requirement**: < 200ms for order ingestion.
*   **Current Stack**: Python FastAPI, Docker, PostgreSQL.
