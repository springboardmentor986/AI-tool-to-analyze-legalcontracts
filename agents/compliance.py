from agents.base_agent import BaseAgent
from config import AGENT_OBJECTIVES
from llm.gemini import call_gemini

class ComplianceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Compliance Officer",
            task=AGENT_OBJECTIVES["compliance"]
        )

    def analyze(self, contract_text, user_message="None"):
        # Step 1: Retrieval
        context = self.retrieve_context(f"{self.task}. Regulations, GDPR, CCPA, governing law, compliance requirements.")
        if not context:
            context = contract_text[:10000]

        # Step 2: Risk Identification
        ident_prompt = f"""
        You are a {self.role}.
        Based on the following contract excerpts:
        {context}
        
        Task: Identify all specific compliance obligations, regulatory requirements (e.g., GDPR, HIPAA), and potential non-compliance risks.
        User Instructions: {user_message}
        
        Return a list of identified points.
        """
        risks = call_gemini(ident_prompt)

        # Step 3: Mitigation & Recommendation (Multi-turn)
        mitigation_prompt = f"""
        You are a {self.role}.
        Based on the identified risks below:
        {risks}
        
        Task: Provide specific, actionable mitigation strategies for each risk. Rate the severity (High/Medium/Low) of each.
        Format: Return ONLY the mitigation strategies. Do NOT include an Executive Summary or analysis of other domains (Legal/Finance).
        """
        final_report = call_gemini(mitigation_prompt)
        
        return final_report
