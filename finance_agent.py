from agent_base import BaseAgent

class FinanceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Finance Agent",
            role="Analyzes financial risks and obligations"
        )

    def analyze(self, text: str):
        insights = []

        if "payment" in text.lower():
            insights.append("💰 Payment terms detected.")

        if "penalty" in text.lower() or "late fee" in text.lower():
            insights.append("⚠️ Penalty or late payment charges found.")

        if "termination" in text.lower():
            insights.append("📉 Termination may have financial impact.")

        if not insights:
            insights.append("✅ No major financial risks detected.")

        return "\n".join(insights)
