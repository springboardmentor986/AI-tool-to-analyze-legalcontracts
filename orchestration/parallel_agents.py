from agents.clause_extractor import extract_key_clauses
from agents.legal_agent import legal_agent
from agents.finance_agent import finance_agent
from agents.compliance_agent import compliance_agent
from agents.operations_agent import operations_agent

def run_parallel_agents(contract_text: str) -> dict:
    """
    Optimized execution:
    1. Extract clauses once
    2. Run agents on small text
    """

    clauses = extract_key_clauses(contract_text)

    return {
        "clauses": clauses,
        "legal": legal_agent(clauses),
        "finance": finance_agent(clauses),
        "compliance": compliance_agent(clauses),
        "operations": operations_agent(clauses),
    }
