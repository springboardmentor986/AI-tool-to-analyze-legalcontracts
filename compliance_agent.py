from agent_base import BaseAgent

class ComplianceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Compliance Agent",
            role="Checks regulatory and policy compliance"
        )

    def analyze(self, text: str):
        issues = []

        if "data protection" not in text.lower():
            issues.append("⚠️ Data protection clause missing or weak.")

        if "law" not in text.lower() and "regulation" not in text.lower():
            issues.append("⚠️ Legal compliance references missing.")

        if not issues:
            issues.append("✅ Contract appears compliant.")

        return "\n".join(issues)
