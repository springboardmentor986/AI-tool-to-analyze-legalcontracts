from agent_base import BaseAgent

class LegalAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Legal Agent",
            role="Identifies legal risks and obligations"
        )

    def analyze(self, text: str):
        risks = []

        if "liability" in text.lower():
            risks.append("⚖️ Liability clause detected.")

        if "indemnity" in text.lower():
            risks.append("⚠️ Indemnity obligations present.")

        if "jurisdiction" in text.lower():
            risks.append("📍 Jurisdiction clause specified.")

        if not risks:
            risks.append("✅ No critical legal risks identified.")

        return "\n".join(risks)
