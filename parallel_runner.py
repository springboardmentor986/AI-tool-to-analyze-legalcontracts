from concurrent.futures import ThreadPoolExecutor

def run_agents_parallel(agents, text):
    results = {}

    with ThreadPoolExecutor(max_workers=len(agents)) as executor:
        futures = {
            executor.submit(agent.analyze, text): agent.name
            for agent in agents
        }

        for future in futures:
            agent_name = futures[future]
            results[agent_name] = future.result()

    return results
