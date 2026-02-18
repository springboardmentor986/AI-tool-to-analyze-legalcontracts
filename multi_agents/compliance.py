from config import llm  # Import the Universal Failover System
from typing import List, Dict, Any

class ComplianceAgent:
    """
    Analyzes contracts for regulatory adherence, reporting obligations, 
    and data protection standards.
    """

    def __init__(self):
        self.role = "Compliance Officer"

    def _prepare_prompt(self, text_input: str) -> str:
        """Constructs the compliance-specific analysis prompt."""
        return (
            f"You are a {self.role}. Evaluate this contract for regulatory compliance. "
            "Focus on: Data Privacy (GDPR/CCPA), Anti-Bribery (FCPA), Reporting Deadlines, "
            "Audit Rights, and Industry-specific regulations. "
            "Provide a structured summary with headings: Regulatory Risks, Audit Rights, Compliance Deadlines.\n\n"
            f"Contract Text:\n{text_input}"
        )

    def run(self, text_chunks: List[Any]) -> Dict[str, Any]:
        """
        Processes document chunks to identify compliance gaps.
        """
        text_input = "\n\n".join([chunk.page_content for chunk in text_chunks])
        prompt = self._prepare_prompt(text_input)

        try:
            # Run with Universal LLM
            response = llm.invoke(prompt)
            summary = response.content

            return {
                "agent": "Compliance",
                "role": self.role,
                "task": "Regulatory and Audit Analysis",
                "summary": summary,
                "status": "success"
            }

        except Exception as e:
            return {
                "agent": "Compliance",
                "status": "error",
                "message": str(e)
            }