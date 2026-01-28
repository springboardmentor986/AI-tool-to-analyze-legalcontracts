import openai
from openai import OpenAI
from typing import List, Dict, Any
from config import GEMINI_API_KEY

class ComplianceAgent:
    """
    Analyzes contracts for regulatory adherence, reporting obligations, 
    and data protection standards.
    """

    def __init__(self, model: str = "gemini-2.5-flash"):
        self.role = "Compliance Officer"
        self.model = model
        self.client = OpenAI(
            api_key=GEMINI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

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

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": self._prepare_prompt(text_input)}]
            )
            
            summary = response.choices[0].message.content

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