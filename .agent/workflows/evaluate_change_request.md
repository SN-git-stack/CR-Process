---
description: How to evaluate a Change Request using the Agent System
---

# Evaluate Change Request Workflow

This workflow describes how to use the Dishware V1 Agent System to evaluate a new feature request.

1. **Check for Change Request File**
   - Look for a `.md` file in the `change_requests/` directory that describes the change.
   - If one does not exist, ask the user to provide the requirements and create one using `templates/cr_template.md` inside `change_requests/`.

2. **Run the Evaluation Script**
   - Execute the python script with the target file.
   - Command: `python evaluate.py <path_to_cr_file>`

3. **Read the Report**
   - The script will generate a `<filename>_REPORT.md`.
   - Read this file using `view_file`.

4. **Summarize for User**
   - Present the key findings (Approved/Rejected, Risks, Effort) to the user.
   - If the agents found critical issues (e.g., Security or Architecture violations from the `knowledge_base`), highlight them immediately.

// turbo
5. **Add to Memory (Optional)**
   - If the user provides new rules (e.g., "We are switching to GraphQL"), update the relevant file in `knowledge_base/` so future evaluations are accurate.
