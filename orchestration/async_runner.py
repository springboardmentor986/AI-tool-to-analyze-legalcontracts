import asyncio

class AsyncRunner:
    def __init__(self):
        pass

    async def run_parallel(self, agents_map: dict, contract_text: str, user_instructions: str):
        """
        Executes agents in parallel with concurrency control (max 2) to avoid Rate Limits.
        agents_map: Dict[name, AgentInstance]
        """
        semaphore = asyncio.Semaphore(1)  # Strict limit to 1 concurrent agent
        results_map = {}
        
        async def run_agent_safe(name, agent):
            async with semaphore:
                try:
                    # random sleep to stagger slightly and respect RPM
                    await asyncio.sleep(4) 
                    return name, await asyncio.to_thread(agent.analyze, contract_text, user_instructions)
                except Exception as e:
                    return name, f"Error: {str(e)}"

        tasks = [run_agent_safe(name, agent) for name, agent in agents_map.items()]
        results = await asyncio.gather(*tasks)
        
        return {name: res for name, res in results}
