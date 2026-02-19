import asyncio

class AsyncRunner:
    def __init__(self):
        pass

    async def run_parallel(self, agents_map: dict, contract_text: str, user_instructions: str):
        """
        Executes agents in parallel with concurrency control (max 2) to avoid Rate Limits.
        agents_map: Dict[name, AgentInstance]
        """
        semaphore = asyncio.Semaphore(4)  # Allow parallel execution (up to 4 agents)
        results_map = {}
        
        async def run_agent_safe(name, agent):
            async with semaphore:
                try:
                    print(f"▶️ Starting Agent: {name.capitalize()}...")
                    # removed artificial sleep to speed up execution
                    result = await asyncio.to_thread(agent.analyze, contract_text, user_instructions)
                    print(f"✅ Finished Agent: {name.capitalize()}")
                    return name, result
                except Exception as e:
                    print(f"❌ Error in Agent {name}: {e}")
                    return name, f"Error: {str(e)}"

        tasks = [run_agent_safe(name, agent) for name, agent in agents_map.items()]
        results = await asyncio.gather(*tasks)
        
        return {name: res for name, res in results}
