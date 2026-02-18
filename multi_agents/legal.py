from config import llm 

class LegalAgent:
    def __init__(self):
        self.role = "Legal Analyst"

    def _prepare_prompt(self, text_input: str) -> str:
        """Constructs the structured prompt for the LLM."""
        return (
            f"You are a {self.role}. Analyze the following legal contract text and "
            "identify key obligations, rights, governing law, liability clauses, and risks. "
            "Provide a structured summary with headings: Obligations, Rights, Risks, Key Clauses.\n\n"
            f"Contract Text:\n{text_input}"
        )

    def run(self, text_chunks):
        # 1. Combine the document chunks into one string
        # (Assumes text_chunks is a list of LangChain Document objects)
        text_input = "\n\n".join([chunk.page_content for chunk in text_chunks])
        
        # 2. Prepare the prompt
        prompt = self._prepare_prompt(text_input)

        try:
            # 3. RUN THE AGENT (Using the Failover System)
            # This single line attempts Groq -> Google -> OpenRouter -> HF -> Ollama
            response = llm.invoke(prompt)
            
            # 4. Extract the text (LangChain returns an object, we need .content)
            summary = response.content
            
            return {
                "agent": "Legal", 
                "role": self.role, 
                "task": "Analyze obligations and rights", 
                "summary": summary, 
                "status": "success"
            }
            
        except Exception as e:
            # This catches errors only if ALL 5 models failed
            return {"agent": "Legal", "status": "error", "message": str(e)}