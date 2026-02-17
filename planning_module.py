"""
Planning Module - Contract Analysis Coordinator
Milestone 2 - Week 3-4

Implements intelligent planning and agent coordination:
- Analyzes contract type and domain
- Determines which specialized agents to use
- Prioritizes agent execution based on contract characteristics
- Coordinates agent workflow dynamically
"""

import os
from typing import Dict, List, Tuple
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()


class OllamaLLMWrapper:
    """Wrapper to provide LangChain-like interface for local Ollama API"""
    def __init__(self, base_url, model):
        self.base_url = base_url
        self.model = model
        import requests
        self.requests = requests
    
    def invoke(self, messages):
        """Invoke Ollama API with LangChain-compatible message format"""
        # Convert LangChain messages to Ollama format
        ollama_messages = []
        for msg in messages:
            if isinstance(msg, SystemMessage):
                ollama_messages.append({"role": "system", "content": msg.content})
            elif isinstance(msg, HumanMessage):
                ollama_messages.append({"role": "user", "content": msg.content})
        
        if not ollama_messages:
            raise Exception("Failed to convert messages")
        
        # Call local Ollama API
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": ollama_messages,
            "stream": False,
            "temperature": 0.1
        }
        
        response = self.requests.post(url, json=payload, timeout=300)
        response.raise_for_status()
        
        # Wrap response in LangChain format
        class OllamaResponse:
            def __init__(self, content):
                self.content = content
        
        data = response.json()
        return OllamaResponse(data.get('message', {}).get('content', ''))


class ContractPlanner:
    """
    Planning module that analyzes contracts and coordinates agent execution
    Acts as the coordinator/manager for multi-agent analysis
    """
    
    def __init__(self, api_key: str = None):
        """Initialize the contract planner with local Ollama"""
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "gemma3:1b")
        
        if not self.ollama_base_url or not self.ollama_model:
            raise ValueError("Ollama configuration missing. Set OLLAMA_BASE_URL and OLLAMA_MODEL in .env file.")
        
        # Create wrapper for local Ollama
        self.llm = OllamaLLMWrapper(self.ollama_base_url, self.ollama_model)
        
        # Define contract types and their characteristics
        self.contract_types = {
            'employment': {
                'keywords': ['employment', 'employee', 'salary', 'benefits', 'termination', 'notice period'],
                'priority_agents': ['legal', 'compliance', 'finance', 'operations']
            },
            'nda': {
                'keywords': ['confidential', 'non-disclosure', 'proprietary', 'trade secret'],
                'priority_agents': ['legal', 'compliance']
            },
            'service_agreement': {
                'keywords': ['services', 'deliverables', 'sla', 'service level', 'performance'],
                'priority_agents': ['operations', 'legal', 'finance', 'compliance']
            },
            'sales_contract': {
                'keywords': ['purchase', 'sale', 'goods', 'products', 'delivery', 'invoice'],
                'priority_agents': ['finance', 'operations', 'legal']
            },
            'partnership': {
                'keywords': ['partnership', 'joint venture', 'collaboration', 'equity', 'revenue sharing'],
                'priority_agents': ['finance', 'legal', 'compliance', 'operations']
            },
            'lease': {
                'keywords': ['lease', 'rent', 'premises', 'landlord', 'tenant', 'property'],
                'priority_agents': ['finance', 'legal', 'operations']
            },
            'license': {
                'keywords': ['license', 'intellectual property', 'royalty', 'ip rights', 'trademark'],
                'priority_agents': ['legal', 'finance', 'compliance']
            },
            'general': {
                'keywords': ['agreement', 'contract', 'parties', 'terms'],
                'priority_agents': ['compliance', 'finance', 'legal', 'operations']
            }
        }
    
    def classify_contract(self, contract_text: str) -> Dict:
        """
        Classify the contract type using AI analysis
        
        Args:
            contract_text: Full text of the contract
            
        Returns:
            Dictionary with contract type, confidence, and metadata
        """
        # Create classification prompt
        classification_prompt = f"""Analyze this contract excerpt and classify its type.

Contract Excerpt (first 2000 characters):
{contract_text[:2000]}

Classify this contract into ONE of these categories:
1. Employment Agreement
2. Non-Disclosure Agreement (NDA)
3. Service Agreement
4. Sales Contract
5. Partnership Agreement
6. Lease Agreement
7. License Agreement
8. General Contract

Respond in this exact format:
CONTRACT_TYPE: [type]
CONFIDENCE: [high/medium/low]
KEY_CHARACTERISTICS: [brief description]
CRITICAL_AREAS: [comma-separated list of what to focus on]
"""
        
        try:
            messages = [
                SystemMessage(content="You are a legal document classifier expert."),
                HumanMessage(content=classification_prompt)
            ]
            
            response = self.llm.invoke(messages)
            result = self._parse_classification_response(response.content)
            
            # Add keyword-based validation
            keyword_match = self._keyword_based_classification(contract_text)
            result['keyword_match'] = keyword_match
            
            return result
            
        except Exception as e:
            print(f"⚠️  Classification error: {str(e)}")
            return {
                'contract_type': 'general',
                'confidence': 'low',
                'key_characteristics': 'Unknown',
                'critical_areas': ['all'],
                'keyword_match': 'general'
            }
    
    def _parse_classification_response(self, response: str) -> Dict:
        """Parse the AI classification response"""
        result = {
            'contract_type': 'general',
            'confidence': 'medium',
            'key_characteristics': '',
            'critical_areas': []
        }
        
        lines = response.strip().split('\n')
        for line in lines:
            if 'CONTRACT_TYPE:' in line:
                contract_type = line.split('CONTRACT_TYPE:')[1].strip().lower()
                # Map to our contract type keys
                if 'employment' in contract_type:
                    result['contract_type'] = 'employment'
                elif 'nda' in contract_type or 'non-disclosure' in contract_type:
                    result['contract_type'] = 'nda'
                elif 'service' in contract_type:
                    result['contract_type'] = 'service_agreement'
                elif 'sales' in contract_type or 'purchase' in contract_type:
                    result['contract_type'] = 'sales_contract'
                elif 'partnership' in contract_type:
                    result['contract_type'] = 'partnership'
                elif 'lease' in contract_type:
                    result['contract_type'] = 'lease'
                elif 'license' in contract_type:
                    result['contract_type'] = 'license'
                    
            elif 'CONFIDENCE:' in line:
                result['confidence'] = line.split('CONFIDENCE:')[1].strip().lower()
                
            elif 'KEY_CHARACTERISTICS:' in line:
                result['key_characteristics'] = line.split('KEY_CHARACTERISTICS:')[1].strip()
                
            elif 'CRITICAL_AREAS:' in line:
                areas = line.split('CRITICAL_AREAS:')[1].strip()
                result['critical_areas'] = [a.strip() for a in areas.split(',')]
        
        return result
    
    def _keyword_based_classification(self, contract_text: str) -> str:
        """
        Fallback keyword-based classification
        Returns the contract type with the most keyword matches
        """
        text_lower = contract_text.lower()
        scores = {}
        
        for contract_type, info in self.contract_types.items():
            score = sum(1 for keyword in info['keywords'] if keyword in text_lower)
            scores[contract_type] = score
        
        # Return type with highest score
        return max(scores, key=scores.get)
    
    def generate_analysis_plan(self, classification: Dict) -> Dict:
        """
        Generate an analysis plan based on contract classification
        
        Args:
            classification: Contract classification result
            
        Returns:
            Analysis plan with agent priority and focus areas
        """
        contract_type = classification.get('contract_type', 'general')
        contract_info = self.contract_types.get(contract_type, self.contract_types['general'])
        
        plan = {
            'contract_type': contract_type,
            'confidence': classification.get('confidence', 'medium'),
            'agent_priority': contract_info['priority_agents'],
            'focus_areas': classification.get('critical_areas', ['all']),
            'execution_strategy': self._determine_execution_strategy(contract_type),
            'key_characteristics': classification.get('key_characteristics', ''),
            'recommended_depth': self._get_analysis_depth(contract_type)
        }
        
        return plan
    
    def _determine_execution_strategy(self, contract_type: str) -> str:
        """Determine the execution strategy based on contract type"""
        high_risk_types = ['employment', 'partnership', 'license']
        
        if contract_type in high_risk_types:
            return 'comprehensive'  # All agents with detailed analysis
        elif contract_type == 'nda':
            return 'focused'  # Only legal and compliance
        else:
            return 'standard'  # All agents, standard depth
    
    def _get_analysis_depth(self, contract_type: str) -> str:
        """Get recommended analysis depth"""
        critical_types = ['employment', 'partnership', 'license']
        
        if contract_type in critical_types:
            return 'deep'
        else:
            return 'standard'
    
    def select_agents(self, plan: Dict) -> List[str]:
        """
        Select which agents to run based on the analysis plan
        
        Args:
            plan: Analysis plan from generate_analysis_plan()
            
        Returns:
            List of agent names to execute
        """
        strategy = plan['execution_strategy']
        
        if strategy == 'comprehensive':
            # Run all agents in priority order
            return plan['agent_priority']
        
        elif strategy == 'focused':
            # Run only top 2 priority agents
            return plan['agent_priority'][:2]
        
        else:  # standard
            # Run all agents
            return plan['agent_priority']
    
    def create_agent_instructions(self, plan: Dict, agent_name: str) -> str:
        """
        Create customized instructions for each agent based on the plan
        
        Args:
            plan: Analysis plan
            agent_name: Name of the agent
            
        Returns:
            Customized instruction string
        """
        base_instruction = f"""
Contract Type: {plan['contract_type'].replace('_', ' ').title()}
Analysis Depth: {plan['recommended_depth']}
Focus Areas: {', '.join(plan['focus_areas'])}

"""
        
        if plan['recommended_depth'] == 'deep':
            base_instruction += "Provide detailed, in-depth analysis with specific examples and citations from the contract.\n"
        else:
            base_instruction += "Provide standard analysis covering key points.\n"
        
        if plan['contract_type'] == 'employment' and agent_name == 'compliance':
            base_instruction += "Pay special attention to labor law compliance and employee rights.\n"
        
        elif plan['contract_type'] == 'nda' and agent_name == 'legal':
            base_instruction += "Focus on confidentiality scope, obligations, and breach consequences.\n"
        
        elif plan['contract_type'] == 'service_agreement' and agent_name == 'operations':
            base_instruction += "Emphasize SLAs, deliverables, timelines, and performance metrics.\n"
        
        return base_instruction


if __name__ == "__main__":
    print("Contract Planning Module - Milestone 2")
    print("=" * 70)
    
    # Test the planner
    planner = ContractPlanner()
    
    # Sample contract text for testing
    sample_text = """
    EMPLOYMENT AGREEMENT
    
    This Employment Agreement is entered into between TechCorp Inc. (the "Employer")
    and John Doe (the "Employee") on January 1, 2026.
    
    1. Position and Duties
    The Employee is hired as Senior Software Engineer and will report to the CTO.
    
    2. Compensation
    The Employee will receive an annual salary of $120,000, payable bi-weekly.
    Benefits include health insurance, 401(k) matching, and 20 days PTO.
    
    3. Termination
    Either party may terminate this agreement with 30 days written notice.
    """
    
    print("\n📝 Testing Contract Classification...")
    classification = planner.classify_contract(sample_text)
    print(f"Contract Type: {classification['contract_type']}")
    print(f"Confidence: {classification['confidence']}")
    print(f"Key Characteristics: {classification['key_characteristics']}")
    
    print("\n🎯 Generating Analysis Plan...")
    plan = planner.generate_analysis_plan(classification)
    print(f"Execution Strategy: {plan['execution_strategy']}")
    print(f"Analysis Depth: {plan['recommended_depth']}")
    print(f"Agent Priority: {', '.join(plan['agent_priority'])}")
    
    print("\n🤖 Selected Agents:")
    agents = planner.select_agents(plan)
    for i, agent in enumerate(agents, 1):
        print(f"  {i}. {agent.title()} Agent")
    
    print("\n✅ Planning Module Ready!")
