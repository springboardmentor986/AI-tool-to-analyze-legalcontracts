from llm.gemini import call_gemini
from llm.prompts import SYNTHESIS_PROMPT

class SynthesisAgent:
    def synthesize(self, agent_outputs):
        """
        Combines outputs from all agents into a final report.
        """
        # Format the inputs for the prompt
        formatted_outputs = "\n\n".join(
            [f"--- {role} ---\n{output}" for role, output in agent_outputs.items()]
        )

        try:
            # Construct the comprehensive prompt
            prompt = SYNTHESIS_PROMPT.format(agent_outputs=formatted_outputs)
            
            # Application of the synthesis logic via LLM
            report = call_gemini(prompt)
            return report
            
        except Exception as e:
            # Graceful degradation in case of synthesis failure
            return f"Error generation report: {e}. Please check agent outputs for raw details."
