# Dishware V1 - POS Change Request Evaluation System

This project implements a Multi-Agent System to evaluate Change Requests (CRs) for a Point of Sale (POS) application.

## 🧠 Project Memory / Context

**Goal**: Automate the initial review of features/requests using AI agents representing different stakeholders (Product Owner, Architect, Security, etc.).

### System Architecture
- **Orchestrator**: `evaluate.py` - Main script that loads a CR, queries agents, and generates an **Executive Summary**.
- **Agents**: Defined in `agents/definitions.py`.
    - **Product Owner**: Strategy & ROI.
    - **Business Analyst**: Requirements & Gaps.
    - **System Architect**: Tech Feasibility & RAG Compliance.
    - **Software Engineer**: Implementation Effort.
    - **Security Specialist**: PCI-DSS & Fraud.
    - **QA Strategist**: Edge Cases & Test Data.
    - **DevOps / SRE**: Operability & Rollback.
- **Knowledge Base (RAG)**: `knowledge_base/` containing policy docs (e.g., `architecture_rules.md`).
- **Input**: Markdown files in `change_requests/<CR_Name>/`.

### Current Status (Version 1 - Jan 2026)
- **Director-Ready Reporting**: Reports now start with a high-level "Go/No-Go" Executive Summary.
- **RAG Enabled**: Agents check against `knowledge_base` rules.
- **Local LLM**: configured to use `localhost:1234` by default.

## 🚀 How to Run

1. **Create a Request**:
   ```powershell
   python create_cr.py "My New Feature"
   ```
   This creates `change_requests/my_new_feature/my_new_feature.md`.

2. **Run Evaluation**:
   ```powershell
   python evaluate.py change_requests/my_new_feature/my_new_feature.md
   ```

3. **View Report**:
   Open `change_requests/my_new_feature/my_new_feature_REPORT.md` to see the Director's Summary and Agent details.

## Repository Structure
- `agents/`: Agent personas.
- `change_requests/`: Database of CRs (one folder per CR).
- `knowledge_base/`: RAG context files.
- `templates/`: Templates.

## Future Plans
- [ ] Integrate real LLM API.
- [ ] Add PDF parsing support for legacy CRs.
- [ ] Create a Web UI for submission.
