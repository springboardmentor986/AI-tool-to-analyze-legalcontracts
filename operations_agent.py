from agent_base import BaseAgent

class OperationsAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Operations Agent",
            role="Analyzes operational feasibility"
        )

    def analyze(self, text: str):
        findings = []

        if "deadline" in text.lower():
            findings.append("⏰ Strict deadlines detected.")

        if "sla" in text.lower() or "service level" in text.lower():
            findings.append("📊 SLA commitments found.")

        if "responsibility" not in text.lower():
            findings.append("⚠️ Responsibilities are unclear.")

        if not findings:
            findings.append("✅ Operational terms look feasible.")

        return "\n".join(findings)
