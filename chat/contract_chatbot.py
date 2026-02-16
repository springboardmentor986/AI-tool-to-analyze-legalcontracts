from agents.gemini_agent import run_gemini

class ContractChatbot:
    def __init__(self):
        self.chat_history = []

    def ask(self, user_query: str, analysis_output: dict = None):
        """
        Conversational assistant using existing contract analysis
        (NO re-running LangGraph)
        """

        if not analysis_output:
            return "⚠️ Please upload and analyze a contract first."

        # Build context from existing analysis
        context = ""
        for section, content in analysis_output.items():
            context += f"{section.upper()}:\n{content}\n\n"

        # Use last 3 chat turns for conversational memory
        history_text = ""
        for turn in self.chat_history[-3:]:
            history_text += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n\n"

        prompt = f"""
You are ClauseAI, an intelligent contract assistant.

You already have the full contract analysis below.
DO NOT re-analyze the document.
ONLY answer based on the provided analysis.

{context}

Conversation so far:
{history_text}

User question:
{user_query}

Answer clearly, professionally, and concisely.
"""

        response = run_gemini(prompt)

        self.chat_history.append({
            "user": user_query,
            "assistant": response
        })

        return response