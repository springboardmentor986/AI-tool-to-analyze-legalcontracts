from config import llm  # Import the Universal Failover System
from typing import List, Dict, Any

class OperationsAgent:
    """
    Analyzes the contract for operational requirements, such as 
    Service Level Agreements (SLAs), delivery timelines, and performance metrics.
    """

    def __init__(self):
        self.role = "Operations Manager"

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
        prompt = self._prepare_prompt(text_input)

        try:
            # Run with Universal LLM
            response = llm.invoke(prompt)
            summary = response.content

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