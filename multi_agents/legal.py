from openai import OpenAI
from config import GEMINI_API_KEY

class LegalAgent:
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.role = "Legal Analyst"
        self.model = model
        self.client = OpenAI(
            api_key=GEMINI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    def _prepare_prompt(self, text_input: str) -> str:
        """Constructs the structured prompt for the LLM."""
        return (
            f"You are a {self.role}. Analyze the following legal contract text and "
            "identify key obligations, rights, governing law, liability clauses, and risks. "
            "Provide a structured summary with headings: Obligations, Rights, Risks, Key Clauses.\n\n"
            f"Contract Text:\n{text_input}"
        )

    def run(self, text_chunks):
        text_input = "\n\n".join([chunk.page_content for chunk in text_chunks])
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": self._prepare_prompt(text_input)}]
            )
            summary = response.choices[0].message.content
            return {
                "agent": "Legal", 
                "role": self.role, 
                "task": "Analyze obligations and rights", 
                "summary": summary, 
                "status": "success"
            }
        except Exception as e:
            return {"agent": "Legal", "status": "error", "message": str(e)}