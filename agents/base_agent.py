from llm.gemini import call_gemini
from llm.prompts import BASE_AGENT_PROMPT
from vectorstore.pinecone_client import PineconeClient

class BaseAgent:
    """
    Base class for all domain-specific agents.
    """
    
    def __init__(self, role, task):
        self.role = role
        self.task = task

    def retrieve_context(self, query):
        """
        Retrieves relevant chunks from Pinecone.
        """
        pc = PineconeClient()
        chunks_data = pc.query_relevant_chunks(query)
        
        formatted_chunks = []
        for item in chunks_data:
            text = item.get("text", "")
            page = item.get("page", "?")
            formatted_chunks.append(f"[Source: Page {page}]\n{text}")
            
        return "\n---\n".join(formatted_chunks)

    def analyze(self, contract_text: str, user_message: str = "None") -> str:
        """
        Conducts domain-specific analysis on the provided contract text.
        
        Args:
            contract_text (str): The full text or relevant section of the contract.
            user_message (str): Optional specific instructions from the user.
            
        Returns:
            str: The analysis result from the LLM.
        """
        # 1. Context Retrieval Strategy
        # We query the vector database to find the most relevant clauses for this specific agent's task.
        context_query = f"{self.task} {user_message}"
        retrieved_context = self.retrieve_context(context_query)
        
        # 2. Fallback Mechanism
        # If vector search returns insufficient data (e.g., short text or ingestion issue),
        # we fall back to processing the raw text directly, truncated to safe limits.
        if not retrieved_context.strip():
            # Log usage of fallback (professional logging)
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"[{self.role}] Context retrieval failed/empty. Using raw text fallback.")
            final_context = contract_text[:15000] # Safe token limit estimate
        else:
            final_context = retrieved_context

        # 3. Prompt Engineering & Execution
        prompt = BASE_AGENT_PROMPT.format(
            role=self.role,
            task=self.task,
            contract_text=final_context,
            user_instructions=user_message
        )
        
        try:
            response = call_gemini(prompt)
            return response
        except Exception as e:
            return f"[{self.role}] Analysis failed: {str(e)}"
