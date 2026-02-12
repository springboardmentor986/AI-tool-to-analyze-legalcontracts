import asyncio
import streamlit as st

from agents.registry import AGENT_REGISTRY
from embeddings.pinecone_client import retrieve_context_by_vector
from embeddings.embedder import get_embedding_model

# Initialize embedder once
embedder = get_embedding_model()

# Limit concurrent API calls
semaphore = asyncio.Semaphore(5)


async def run_single_agent(domain: str):
    agent = AGENT_REGISTRY.get(domain)
    if not agent:
        return domain, None

    async with semaphore:

        query = f"Find clauses related to {domain} in this contract"

        query_vector = await asyncio.to_thread(
            embedder.embed_query,
            query
        )

        context = await asyncio.to_thread(
            retrieve_context_by_vector,
            query_vector,
            st.session_state.contract_id,
            3
        )

        # 🔥 FIX HERE
        result = await asyncio.to_thread(agent, context)

        return domain, result



async def run_agents(domains: list[str]) -> dict:
    tasks = [run_single_agent(domain) for domain in domains]

    results = await asyncio.gather(*tasks)

    return {
        domain: result
        for domain, result in results
        if result
    }
