import json
import os
from datetime import datetime

HISTORY_FILE = "analysis_history.json"

def load_history():
    """Loads analysis history from a local JSON file."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading history: {e}")
        return []

def save_to_history(contract_text, final_report, agent_outputs, risk_level):
    """Saves the analysis result to the history JSON file."""
    history = load_history()
    
    # Generate a brief summary snippet for the history card
    summary_snippet = final_report[:200] + "..." if final_report else "No report generated."
    
    entry = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "risk_level": risk_level,
        "summary": summary_snippet,
        "final_report": final_report,
        "agent_outputs": agent_outputs
    }
    
    # Keep newest edits at the top of the list
    history.insert(0, entry)
    
    # Cap history at the last 50 entries to prevent infinite growth
    if len(history) > 50:
        history = history[:50]

    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving history: {e}")
