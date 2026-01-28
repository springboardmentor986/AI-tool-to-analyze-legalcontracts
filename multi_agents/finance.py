import openai
from openai import OpenAI
from typing import List, Dict, Any
from config import GEMINI_API_KEY

class FinanceAgent:
    """
    Analyzes legal and commercial documents for financial implications, 
    including payment terms, penalties, and fiscal risks.
    """

    def __init__(self, model: str = "gemini-2.5-flash"):
        self.role = "Financial Analyst"
        self.model = model
        self.client = OpenAI(
            api_key=GEMINI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    def _prepare_prompt(self, text_input: str) -> str:
        """Constructs the financial analysis prompt."""
        return (
            f"You are a {self.role}. Extract and analyze the financial terms of this contract. "
            "Identify: Payment Schedules, Late Payment Penalties, Currency Requirements, "
            "Taxes, and Financial Exit Costs. "
            "Provide a structured summary with headings: Payment Terms, Penalties, Fiscal Risks.\n\n"
            f"Contract Text:\n{text_input}"
        )

    def run(self, text_chunks: List[Any]) -> Dict[str, Any]:
        """
        Processes document chunks to extract financial data.
        """
        text_input = "\n\n".join([chunk.page_content for chunk in text_chunks])

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": self._prepare_prompt(text_input)}]
            )
            
            summary = response.choices[0].message.content

            return {
                "agent": "Finance",
                "role": self.role,
                "task": "Financial Risk and Term Extraction",
                "summary": summary,
                "status": "success"
            }

        except Exception as e:
            return {
                "agent": "Finance",
                "status": "error",
                "message": str(e)
            }