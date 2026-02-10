from agents.base_agent import BaseAgent
from config import AGENT_OBJECTIVES
from llm.gemini import call_gemini

class FinanceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Financial Auditor",
            task=AGENT_OBJECTIVES["finance"]
        )

    def analyze(self, contract_text, user_message="None"):
        # Step 1: Retrieval
        context = self.retrieve_context(f"{self.task}. Payments, penalties, interest, fees, indemnity, liability caps, warranties.")
        if not context:
            context = contract_text[:10000]

        # Step 2: Extraction
        extract_prompt = f"""
        You are a {self.role}.
        Based on these contract excerpts:
        {context}
        
        Task: Extract all financial terms, including payment schedules, penalties, late fees, liability caps, and indemnity obligations.
        User Instructions: {user_message}
        """
        extracted_data = call_gemini(extract_prompt)

        # Step 3: Analysis
        analysis_prompt = f"""
        You are a {self.role}.
        Analyze the following financial terms for risks:
        {extracted_data}
        
        Task: Highlight any unfavorable terms, missing protections, or ambiguous financial clauses. Calculate potential maximum liability if possible.
        """
        report = call_gemini(analysis_prompt)
        
        return report
