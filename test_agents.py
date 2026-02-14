from CLAUSE_AI.compliance_agent import ComplianceAgent

# Load sample contract
with open("CLAUSE_AI/sample_contracts/sample1.txt", "r", encoding="utf-8") as f:
    contract_text = f.read()

agent = ComplianceAgent()
result = agent.analyze(contract_text)

print("\n--- COMPLIANCE ANALYSIS ---\n")
print(result)
