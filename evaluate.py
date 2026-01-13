import os
import argparse
from agents.definitions import ALL_AGENTS, AgentPersona

def read_file(filepath):
    """Reads the content of the CR file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def load_knowledge_base(kb_dir: str) -> str:
    """Reads all markdown files from the knowledge base directory."""
    if not os.path.exists(kb_dir):
        return ""
    
    print(f"Loading Knowledge Base from: {kb_dir}")
    kb_content = []
    for filename in os.listdir(kb_dir):
        if filename.endswith(".md"):
            path = os.path.join(kb_dir, filename)
            content = read_file(path)
            kb_content.append(f"--- DOCUMENT: {filename} ---\n{content}\n")
    
    return "\n".join(kb_content)

def simulate_llm_response(agent: AgentPersona, cr_content: str, kb_context: str) -> str:
    """
    Mocks an LLM response with Knowledge Base awareness.
    """
    print(f"\n--- [Simulating AI Evaluation for: {agent.role_name}] ---")
    
    # In a real scenario, the prompt would be:
    # System: agent.system_instruction + "\n\nCONTEXT:\n" + kb_context
    # User: cr_content
    
    # Mock logic checking for KB violations
    if "Architect" in agent.role_name:
        if "Java" in cr_content and "NO JAVA" in kb_context:
            return f"""
**Feasibility**: No
**Architectural Impact**: Critical
**Technical Constraints**:
* **VIOLATION**: The Knowledge Base explicitly states "NO JAVA". We must use Python or C#.
"""
        return f"""
**Feasibility**: Yes.
**Architectural Impact**: Low.
**Note**: Verified against Architecture Rules (Python/FastAPI compliant).
"""
        
    if "Product Owner" in agent.role_name:
        return f"""
**Decision**: Approve
**Reasoning**:
* Aligns with the roadmap.
**Priority**: High
"""

    return f"**Analysis**: Looks reasonable. Context checked."

def evaluate_cr(cr_filepath: str):
    print(f"Loading Change Request from: {cr_filepath}...")
    try:
        cr_content = read_file(cr_filepath)
    except Exception as e:
        print(f"Error: {e}")
        return

    # Load RAG Context
    kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base")
    kb_context = load_knowledge_base(kb_path)
    if kb_context:
        print(f"Loaded {len(kb_context)} characters of context context.")

    print("\nStarting Multi-Agent Evaluation...\n" + "="*40)

    results = {}
    
    for agent in ALL_AGENTS:
        print(f"\n> Agent: {agent.role_name}")
        print(f"> Focus: {', '.join(agent.focus_areas)}")
        
        # Here we invoke the "AI" with Context
        response = simulate_llm_response(agent, cr_content, kb_context)
        
        results[agent.role_name] = response
        print(f"\n{response}\n" + "-"*40)

    print("\nEvaluation Complete.")
    
    # Save Report
    base, _ = os.path.splitext(cr_filepath)
    output_path = f"{base}_REPORT.md"
    
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(f"# Evaluation Report for {os.path.basename(cr_filepath)}\n\n")
        f.write(f"**Date**: {os.getcwd()}\n\n")
        
        for role, analysis in results.items():
            f.write(f"## {role}\n")
            f.write(analysis + "\n\n")
            
    print(f"Report saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate a POS Change Request using AI Agents.")
    parser.add_argument("file", help="Path to the Change Request markdown file.")
    
    args = parser.parse_args()
    evaluate_cr(args.file)
