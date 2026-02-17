"""
Prompt Templates Module
Milestone 2 - Week 3-4

Reusable, customizable prompt templates for agent communication.
Enables consistent, high-quality prompts across all agents.
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class PromptTemplate:
    """Structure for prompt templates"""
    name: str
    template: str
    variables: List[str]
    description: str


class PromptTemplates:
    """
    Central repository for all prompt templates used in agent communication
    Provides consistent, customizable prompts for different contract types
    """
    
    # ==================== AGENT SYSTEM PROMPTS ====================
    
    @staticmethod
    def get_compliance_system_prompt(contract_type: str = "general") -> str:
        """Get compliance agent system prompt based on contract type"""
        base_prompt = """You are an expert Compliance Analyst AI specializing in contract compliance review.

Your expertise includes:
- Regulatory compliance (GDPR, CCPA, SOX, HIPAA)
- Industry standards and best practices
- Risk identification and assessment
- Data protection and privacy laws
- Audit requirements"""
        
        type_specific = {
            'employment': """
Special Focus for Employment Contracts:
- Labor law compliance
- Equal employment opportunity requirements
- Wage and hour regulations
- Employee benefits compliance
- Workers' compensation requirements""",
            
            'nda': """
Special Focus for NDAs:
- Information classification standards
- Data protection regulations
- Trade secret laws
- Industry-specific confidentiality requirements""",
            
            'service_agreement': """
Special Focus for Service Agreements:
- Service industry regulations
- Data processing compliance
- Quality standards
- Insurance requirements"""
        }
        
        return base_prompt + type_specific.get(contract_type, "")
    
    @staticmethod
    def get_finance_system_prompt(contract_type: str = "general") -> str:
        """Get finance agent system prompt based on contract type"""
        base_prompt = """You are an expert Finance Analyst AI specializing in contract financial analysis.

Your expertise includes:
- Payment terms and schedules
- Pricing structures and models
- Financial risk assessment
- Cost-benefit analysis
- Budget impact evaluation"""
        
        type_specific = {
            'employment': """
Special Focus for Employment Contracts:
- Total compensation analysis
- Benefits valuation
- Bonus and incentive structures
- Stock options and equity
- Severance and termination costs""",
            
            'sales_contract': """
Special Focus for Sales Contracts:
- Revenue recognition
- Payment milestones
- Volume discounts
- Price adjustments
- Credit terms""",
            
            'partnership': """
Special Focus for Partnership Agreements:
- Capital contributions
- Profit/loss sharing
- Revenue distribution
- Investment returns
- Exit valuations"""
        }
        
        return base_prompt + type_specific.get(contract_type, "")
    
    @staticmethod
    def get_legal_system_prompt(contract_type: str = "general") -> str:
        """Get legal agent system prompt based on contract type"""
        base_prompt = """You are an expert Legal Analyst AI specializing in contract legal review.

Your expertise includes:
- Contract law and enforceability
- Liability and indemnification
- Termination and breach provisions
- Dispute resolution mechanisms
- Intellectual property rights"""
        
        type_specific = {
            'employment': """
Special Focus for Employment Contracts:
- At-will vs. fixed-term employment
- Non-compete and non-solicitation clauses
- Termination rights and procedures
- Confidentiality obligations
- Dispute resolution and arbitration""",
            
            'nda': """
Special Focus for NDAs:
- Scope of confidential information
- Permitted disclosures
- Term and survival clauses
- Breach remedies and injunctive relief
- Return/destruction obligations""",
            
            'license': """
Special Focus for License Agreements:
- License scope and limitations
- IP ownership and rights
- Sublicensing provisions
- Term and renewal
- Termination and post-termination rights"""
        }
        
        return base_prompt + type_specific.get(contract_type, "")
    
    @staticmethod
    def get_operations_system_prompt(contract_type: str = "general") -> str:
        """Get operations agent system prompt based on contract type"""
        base_prompt = """You are an expert Operations Analyst AI specializing in operational contract review.

Your expertise includes:
- Deliverables and milestones
- Service level agreements (SLAs)
- Performance metrics and KPIs
- Timeline and deadline management
- Resource requirements"""
        
        type_specific = {
            'service_agreement': """
Special Focus for Service Agreements:
- Service scope and specifications
- Response time requirements
- Uptime and availability commitments
- Support levels and escalation
- Change management procedures""",
            
            'employment': """
Special Focus for Employment Contracts:
- Job duties and responsibilities
- Work schedule and hours
- Performance expectations
- Review cycles and evaluation
- Training and development requirements""",
            
            'sales_contract': """
Special Focus for Sales Contracts:
- Delivery schedules and logistics
- Quality specifications
- Inspection and acceptance procedures
- Warranty terms
- Return and refund policies"""
        }
        
        return base_prompt + type_specific.get(contract_type, "")
    
    # ==================== ANALYSIS PROMPTS ====================
    
    @staticmethod
    def get_analysis_prompt_template(agent_type: str, depth: str = "standard") -> PromptTemplate:
        """Get analysis prompt template for specific agent"""
        
        templates = {
            'compliance': PromptTemplate(
                name="compliance_analysis",
                template="""Analyze this contract for compliance requirements and risks.

Contract Type: {contract_type}
Analysis Depth: {depth}

Contract Text:
{contract_text}

Provide analysis in the following structure:
1. **Regulatory Compliance Status**
   - Applicable regulations
   - Compliance level assessment
   
2. **Identified Risks**
   - Critical compliance risks
   - Potential violations
   
3. **Required Actions**
   - Immediate actions needed
   - Recommended changes
   
4. **Recommendations**
   - Best practices
   - Risk mitigation strategies""",
                variables=['contract_type', 'depth', 'contract_text'],
                description="Template for compliance analysis"
            ),
            
            'finance': PromptTemplate(
                name="finance_analysis",
                template="""Analyze this contract for financial terms, obligations, and risks.

Contract Type: {contract_type}
Analysis Depth: {depth}

Contract Text:
{contract_text}

Provide analysis in the following structure:
1. **Financial Summary**
   - Total financial commitment
   - Payment structure overview
   
2. **Payment Terms**
   - Payment schedule
   - Due dates and milestones
   - Payment methods
   
3. **Cost Analysis**
   - Direct costs
   - Hidden or indirect costs
   - Penalties and late fees
   
4. **Financial Risks**
   - Identified financial risks
   - Budget impact assessment
   
5. **Recommendations**
   - Cost optimization suggestions
   - Risk mitigation strategies""",
                variables=['contract_type', 'depth', 'contract_text'],
                description="Template for financial analysis"
            ),
            
            'legal': PromptTemplate(
                name="legal_analysis",
                template="""Analyze this contract for legal terms, obligations, and potential issues.

Contract Type: {contract_type}
Analysis Depth: {depth}

Contract Text:
{contract_text}

Provide analysis in the following structure:
1. **Key Legal Obligations**
   - Primary obligations of each party
   - Performance requirements
   
2. **Liability and Risk Exposure**
   - Liability limitations
   - Indemnification clauses
   - Insurance requirements
   
3. **Termination Provisions**
   - Termination rights
   - Notice requirements
   - Post-termination obligations
   
4. **Dispute Resolution**
   - Dispute resolution mechanism
   - Governing law and jurisdiction
   
5. **Legal Risks**
   - Identified legal risks
   - Unfavorable terms
   
6. **Recommendations**
   - Suggested modifications
   - Risk mitigation strategies""",
                variables=['contract_type', 'depth', 'contract_text'],
                description="Template for legal analysis"
            ),
            
            'operations': PromptTemplate(
                name="operations_analysis",
                template="""Analyze this contract for operational requirements, deliverables, and execution feasibility.

Contract Type: {contract_type}
Analysis Depth: {depth}

Contract Text:
{contract_text}

Provide analysis in the following structure:
1. **Deliverables and Milestones**
   - Key deliverables
   - Timeline and deadlines
   - Acceptance criteria
   
2. **Service Level Agreements (SLAs)**
   - Performance metrics
   - Service standards
   - Response time requirements
   
3. **Operational Requirements**
   - Resource needs
   - Implementation requirements
   - Ongoing operational obligations
   
4. **Execution Risks**
   - Timeline feasibility
   - Resource constraints
   - Dependency risks
   
5. **Recommendations**
   - Execution strategy
   - Risk mitigation
   - Resource optimization""",
                variables=['contract_type', 'depth', 'contract_text'],
                description="Template for operations analysis"
            )
        }
        
        return templates.get(agent_type)
    
    # ==================== SUMMARY PROMPTS ====================
    
    @staticmethod
    def get_summary_prompt_template() -> str:
        """Get executive summary prompt template"""
        return """Create a comprehensive executive summary of the contract analysis.

You have received analysis from multiple specialized agents:

**Compliance Analysis:**
{compliance_analysis}

**Financial Analysis:**
{finance_analysis}

**Legal Analysis:**
{legal_analysis}

**Operational Analysis:**
{operations_analysis}

Create an executive summary with the following structure:

## Executive Summary

### Contract Overview
[Brief description of contract type and purpose]

### Key Findings
1. [Most critical finding from all analyses]
2. [Second most important finding]
3. [Third most important finding]

### Critical Risks (High Priority)
- [List 3-5 most critical risks across all domains]

### Financial Impact
[Summary of total financial commitment and key cost factors]

### Action Items
1. [Immediate action required]
2. [Short-term actions]
3. [Long-term considerations]

### Overall Recommendation
[Clear recommendation: Sign as-is / Sign with modifications / Do not sign / Seek legal counsel]

### Risk Level Assessment
Overall Risk: [LOW / MEDIUM / HIGH / CRITICAL]

Keep the summary concise but comprehensive. Prioritize actionable insights."""
    
    # ==================== CLASSIFICATION PROMPTS ====================
    
    @staticmethod
    def get_classification_prompt() -> str:
        """Get contract classification prompt"""
        return """Analyze this contract excerpt and classify its type.

Contract Excerpt:
{contract_text}

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
KEY_CHARACTERISTICS: [brief description of what identifies this contract type]
CRITICAL_AREAS: [comma-separated list of areas that require special attention]
PRIMARY_PARTIES: [identify the main parties involved]
"""
    
    # ==================== HELPER METHODS ====================
    
    @staticmethod
    def format_prompt(template: PromptTemplate, **kwargs) -> str:
        """
        Format a prompt template with provided variables
        
        Args:
            template: PromptTemplate object
            **kwargs: Variable values to fill in the template
            
        Returns:
            Formatted prompt string
        """
        try:
            return template.template.format(**kwargs)
        except KeyError as e:
            print(f"⚠️  Missing variable in prompt template: {e}")
            return template.template
    
    @staticmethod
    def get_all_agent_prompts(contract_type: str = "general") -> Dict[str, str]:
        """Get all agent system prompts for a given contract type"""
        return {
            'compliance': PromptTemplates.get_compliance_system_prompt(contract_type),
            'finance': PromptTemplates.get_finance_system_prompt(contract_type),
            'legal': PromptTemplates.get_legal_system_prompt(contract_type),
            'operations': PromptTemplates.get_operations_system_prompt(contract_type)
        }


if __name__ == "__main__":
    print("Prompt Templates Module - Milestone 2")
    print("=" * 70)
    
    # Test prompt templates
    print("\n📝 Testing Compliance Agent Prompt (Employment Contract):")
    print("-" * 70)
    prompt = PromptTemplates.get_compliance_system_prompt('employment')
    print(prompt)
    
    print("\n\n📊 Testing Finance Analysis Template:")
    print("-" * 70)
    template = PromptTemplates.get_analysis_prompt_template('finance')
    print(f"Template Name: {template.name}")
    print(f"Variables: {', '.join(template.variables)}")
    print(f"Description: {template.description}")
    
    print("\n\n🎯 Testing Prompt Formatting:")
    print("-" * 70)
    formatted = PromptTemplates.format_prompt(
        template,
        contract_type="Sales Contract",
        depth="deep",
        contract_text="Sample contract text..."
    )
    print(formatted[:300] + "...")
    
    print("\n✅ Prompt Templates Module Ready!")
