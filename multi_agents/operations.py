import openai
from openai import OpenAI
from typing import List, Dict, Any
from config import GEMINI_API_KEY

class OperationsAgent:
    """
    Analyzes the contract for operational requirements, such as 
    Service Level Agreements (SLAs), delivery timelines, and performance metrics.
    """

    def __init__(self, model: str = "gemini-2.5-flash"):
        self.role = "Operations Manager"
        self.model = model
        self.client = OpenAI(
            api_key=GEMINI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    def _prepare_prompt(self, text_input: str) -> str:
        return (
            f"You are a {self.role}. Analyze this contract for operational details. "
            "Identify: Service Level Agreements (SLAs), Delivery Timelines, "
            "Performance Benchmarks, Reporting Requirements, and Support Obligations. "
            "Provide a structured summary with headings: SLAs, Timelines, Deliverables.\n\n"
            f"Contract Text:\n{text_input}"
        )

    def run(self, text_chunks: List[Any]) -> Dict[str, Any]:
        text_input = "\n\n".join([chunk.page_content for chunk in text_chunks])

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": self._prepare_prompt(text_input)}]
            )
            
            summary = response.choices[0].message.content

            return {
                "agent": "Operations",
                "role": self.role,
                "task": "SLA and Timeline Analysis",
                "summary": summary,
                "status": "success"
            }

        except Exception as e:
            return {
                "agent": "Operations",
                "status": "error",
                "message": str(e)
            }