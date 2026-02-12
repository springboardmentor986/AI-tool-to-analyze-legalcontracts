from config import llm  # Import the Universal Failover System
from typing import List, Dict, Any

class FinanceAgent:
    """
    Analyzes legal and commercial documents for financial implications, 
    including payment terms, penalties, and fiscal risks.
    """

    def __init__(self):
        self.role = "Financial Analyst"
        # Removed hardcoded OpenAI client. 'llm' from config handles everything.

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
        # 1. Combine chunks
        text_input = "\n\n".join([chunk.page_content for chunk in text_chunks])
        
        # 2. Prepare Prompt
        prompt = self._prepare_prompt(text_input)

        try:
            # 3. RUN WITH FAILOVER (Groq -> Google -> OpenRouter -> HF -> Ollama)
            response = llm.invoke(prompt)
            
            # 4. Extract Text
            summary = response.content

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