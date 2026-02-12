from agents.legal import analyze_legal
from agents.finance import analyze_finance
from agents.Compliance import analyze_compliance
from agents.Operations import analyze_operations

AGENT_REGISTRY = {
    "legal": analyze_legal,
    "finance": analyze_finance,
    "compliance": analyze_compliance,
    "operations": analyze_operations
}
