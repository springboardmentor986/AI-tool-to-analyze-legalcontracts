from llm.gemini import call_gemini
from llm.prompts import SYNTHESIS_PROMPT

class SynthesisAgent:
    def synthesize(self, agent_outputs, user_instructions="None"):
        """
        Combines outputs from all agents into a final report.
        """
        # Format the inputs for the prompt
        formatted_outputs = "\n\n".join(
            [f"--- {role} ---\n{output}" for role, output in agent_outputs.items()]
        )

        try:
            # Construct the comprehensive prompt
            prompt = SYNTHESIS_PROMPT.format(
                agent_outputs=formatted_outputs,
                user_instructions=user_instructions
            )
            
            # Application of the synthesis logic via LLM
            report = call_gemini(prompt)
            
            # Validate that the LLM included all requested sections
            # Default sections
            default_sections = [
                "Executive Summary",
                "Compliance Analysis",
                "Financial Analysis",
                "Legal Risks",
                "Operational Notes"
            ]
            
            target_sections = default_sections
            
            # Parse dynamic sections from user_instructions if present
            if "Target Sections:" in user_instructions:
                try:
                    # Extract requested sections from instructions string
                    section_str = user_instructions.split("Target Sections:")[1].strip()
                    section_str = section_str.split("\n")[0]
                    if section_str:
                        target_sections = [s.strip() for s in section_str.split(",")]
                except:
                    pass # Fallback to default
            
            missing_sections = []
            for section in target_sections:
                # Verify the section name is present in the generated report output
                if section not in report: 
                    missing_sections.append(section)
            
            if missing_sections:
                warning_msg = "\n\n---\n**[SYSTEM WARNING] Validation Failed**: The following required sections were missing from the AI response:\n"
                warning_msg += "\n".join([f"- {s}" for s in missing_sections])
                warning_msg += "\n\nPlease try re-running the analysis."
                report += warning_msg
                
            return report
            
        except Exception as e:
            # Graceful degradation in case of synthesis failure
            return f"Error generation report: {e}. Please check agent outputs for raw details."
