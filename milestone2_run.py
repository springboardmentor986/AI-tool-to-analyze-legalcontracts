import os
import docx2txt
from PyPDF2 import PdfReader

from planning.planner import plan_agents
from planning.graph import build_graph


def load_contract(file_path: str) -> str:
    if file_path.lower().endswith(".pdf"):
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    elif file_path.lower().endswith(".docx"):
        return docx2txt.process(file_path)

    elif file_path.lower().endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    else:
        raise ValueError("Unsupported file format")


if __name__ == "__main__":

    raw_path = input("Enter contract file path (.pdf / .docx / .txt): ").strip()

    # 🔥 Normalize Windows path safely
    file_path = os.path.normpath(raw_path.strip('"').strip("'"))

    print(f"\n🔎 Checking path: {file_path}")

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found at: {file_path}")

    print("\n📄 Loading contract...")
    contract_text = load_contract(file_path)

    print("✅ Contract loaded successfully")
    print(f"📏 Contract length: {len(contract_text)} characters\n")

    task = "Analyze compliance, legal, financial, and operational risks"

    print("🧠 Planning agents...")
    plan = plan_agents(task)
    print("✅ Selected agents:", plan)

    print("\n⚙️ Running LangGraph execution...\n")
    graph = build_graph()

    state = {
        "text": contract_text,
        "plan": plan,
        "results": []
    }

    output = graph.invoke(state)

    print("\n===== ANALYSIS RESULTS =====\n")
    for result in output["results"]:
        print(f"[{result['agent']}]")
        print(result["output"])
        print("-" * 60)
