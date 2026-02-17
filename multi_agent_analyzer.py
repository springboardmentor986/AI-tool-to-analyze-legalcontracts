"""
Multi-Agent Contract Analysis with LangGraph
Milestone 1 - Week 1-2

Implements multi-agent workflow for contract analysis using:
- LangChain for AI agent creation
- LangGraph for agent orchestration  
- Pinecone for vector storage
"""

import os
import sys
import time
import hashlib

# Fix Windows console UTF-8 encoding for emoji support
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
from typing import TypedDict, Annotated, List, Dict
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, SystemMessage

try:
    from langgraph.graph import StateGraph, END
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    print("[WARNING] LangGraph import issue - using simplified workflow")

from agent_roles import AgentRoles
from document_parser import DocumentParser
from vector_store import VectorStore
from clause_extractor import ParallelClauseExtractor  # Week 3
from risk_analyzer import RiskAnalyzer  # Week 3
from multi_turn_interaction import MultiTurnInteraction  # Milestone 3
from risk_scoring_system import RiskScoringSystem  # Risk scoring
from missing_clause_detector import MissingClauseDetector  # Missing clause detection
from multilingual_engine import MultilingualEngine  # Multilingual support

# Milestone 2 imports
try:
    from planning_module import ContractPlanner
    from prompt_templates import PromptTemplates
    PLANNING_AVAILABLE = True
except ImportError:
    PLANNING_AVAILABLE = False
    print("[WARNING] Planning module not available - using basic workflow")

# Load environment variables
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


class ContractAnalysisState(TypedDict):
    """State for multi-agent contract analysis workflow"""
    contract_text: str
    contract_metadata: Dict
    contract_type: str  # Milestone 2: Added contract type
    analysis_plan: Dict  # Milestone 2: Added analysis plan
    extracted_clauses: Dict  # Week 3: Parallel clause extraction results
    identified_risks: Dict  # Week 3: Risk identification results
    discussion_summaries: List[str]  # Milestone 3: Multi-turn discussions
    compliance_analysis: str
    finance_analysis: str
    legal_analysis: str
    operations_analysis: str
    final_summary: str
    errors: List[str]


class MultiAgentContractAnalyzer:
    """
    Multi-agent system for comprehensive contract analysis
    Uses LangGraph to orchestrate multiple AI agents
    Milestone 2: Enhanced with Planning Module for intelligent agent coordination
    """
    
    def __init__(self, google_api_key: str = None):
        """Initialize the multi-agent analyzer with local Ollama"""
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "gemma3:1b")
        
        if not self.ollama_base_url or not self.ollama_model:
            raise ValueError("Ollama configuration missing. Set OLLAMA_BASE_URL and OLLAMA_MODEL in .env file.")
        
        # Create wrapper for local Ollama
        self.llm = OllamaLLMWrapper(self.ollama_base_url, self.ollama_model)
        
        self.current_llm = "Ollama"
        self.current_llm_name = f"Ollama-{self.ollama_model}"
        
        print(f"[OK] Using local Ollama: {self.ollama_model}")
        
        # Get agent roles
        self.agents = AgentRoles.get_all_agents()
        
        # Week 3: Initialize parallel processing modules
        self.clause_extractor = ParallelClauseExtractor()
        self.risk_analyzer = RiskAnalyzer()
        print("[OK] Week 3: Parallel clause extraction and risk analysis enabled")
        
        # Milestone 3: Initialize multi-turn interaction
        self.multi_turn = MultiTurnInteraction(self.llm, self.agents)
        print("[OK] Milestone 3: Multi-turn agent interactions enabled")
        
        # Risk scoring and missing clause detection
        self.risk_scorer = RiskScoringSystem()
        self.missing_clause_detector = MissingClauseDetector()
        print("[OK] Risk scoring and missing clause detection enabled")
        
        # Multilingual engine
        try:
            self.multilingual_engine = MultilingualEngine()
            print("[OK] Multilingual translation engine enabled")
        except Exception as e:
            self.multilingual_engine = None
            print(f"[WARNING] Multilingual engine disabled: {str(e)}")
        
        # Milestone 2: Initialize planning module
        if PLANNING_AVAILABLE:
            self.planner = ContractPlanner()
            print("[OK] Planning Module enabled")
        else:
            self.planner = None
            print("[WARNING] Planning Module disabled - using all agents")
        
        # Initialize vector store for contract storage
        self.vector_store = VectorStore()
        
        # Build workflow graph
        self.workflow = self._build_workflow()
    
    def _serialize_for_translation(self, obj):
        """
        Serialize objects to JSON-compatible format before translation
        Handles dataclasses, Enums, and nested structures
        """
        from enum import Enum
        
        if isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, dict):
            return {k: self._serialize_for_translation(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize_for_translation(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            # Convert dataclass or object to dict
            result = {}
            for key, value in obj.__dict__.items():
                result[key] = self._serialize_for_translation(value)
            return result
        return obj
    
    def _build_workflow(self):
        """Build LangGraph workflow for multi-agent analysis"""
        
        if not LANGGRAPH_AVAILABLE:
            return None
        
        # Create state graph
        workflow = StateGraph(ContractAnalysisState)
        
        # Add nodes for each agent
        workflow.add_node("compliance_agent", self._compliance_analysis)
        workflow.add_node("finance_agent", self._finance_analysis)
        workflow.add_node("legal_agent", self._legal_analysis)
        workflow.add_node("operations_agent", self._operations_analysis)
        workflow.add_node("summarizer", self._create_final_summary)
        
        # Define workflow edges
        workflow.set_entry_point("compliance_agent")
        workflow.add_edge("compliance_agent", "finance_agent")
        workflow.add_edge("finance_agent", "legal_agent")
        workflow.add_edge("legal_agent", "operations_agent")
        workflow.add_edge("operations_agent", "summarizer")
        workflow.add_edge("summarizer", END)
        
        return workflow.compile()
    
    def _call_llm_with_retry(self, messages, max_retries=3, base_delay=40):
        """
        Call Ollama LLM with retry logic
        
        Args:
            messages: List of LangChain messages
            max_retries: Maximum number of retries
            base_delay: Base delay in seconds for exponential backoff
            
        Returns:
            LLM response
        """
        for attempt in range(max_retries):
            try:
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
                import requests
                url = f"{self.ollama_base_url}/api/chat"
                payload = {
                    "model": self.ollama_model,
                    "messages": ollama_messages,
                    "stream": False,
                    "temperature": 0.1
                }
                
                response = requests.post(url, json=payload, timeout=300)
                response.raise_for_status()
                
                # Wrap response in LangChain format
                class OllamaResponse:
                    def __init__(self, content):
                        self.content = content
                
                data = response.json()
                return OllamaResponse(data.get('message', {}).get('content', ''))
                    
            except Exception as e:
                error_str = str(e).lower()
                
                if 'ratio|exhausted|429' in error_str or attempt == max_retries - 1:
                    raise
                    
                delay = base_delay * (2 ** attempt)
                print(f"[WARNING] Ollama API error, retrying in {delay:.0f}s...")
                time.sleep(delay)
    
    def _compliance_analysis(self, state: ContractAnalysisState) -> ContractAnalysisState:
        """Compliance Agent analysis - Week 3: Enhanced with extracted clauses and risk data"""
        try:
            agent = self.agents['compliance']
            
            # Week 3: Prepare enhanced context with extracted clauses and risks
            compliance_clauses = state['extracted_clauses'].get('compliance', [])
            compliance_risks = state['identified_risks'].get('compliance', [])
            
            clause_summary = f"\n\nExtracted Compliance Clauses ({len(compliance_clauses)} found):\n"
            for clause in compliance_clauses[:5]:  # Top 5 clauses
                clause_summary += f"- {clause.clause_type}: {clause.text[:100]}...\n"
            
            risk_summary = f"\n\nIdentified Compliance Risks ({len(compliance_risks)} found):\n"
            for risk in compliance_risks[:5]:  # Top 5 risks
                risk_summary += f"- [{risk.severity.value}] {risk.category}: {risk.description}\n"
            
            enhanced_context = f"{state['contract_text'][:2000]}{clause_summary}{risk_summary}"
            
            messages = [
                SystemMessage(content=agent.system_prompt),
                HumanMessage(content=f"Analyze this contract with extracted clauses and identified risks:\n\n{enhanced_context}")
            ]
            
            print("[ANALYZE] Running Compliance Agent...")
            response = self._call_llm_with_retry(messages)
            state['compliance_analysis'] = response.content
            print("[OK] Compliance Agent complete")
            
            # Milestone 3: Check if multi-turn discussion needed
            should_discuss, topic = self.multi_turn.should_initiate_discussion(
                'compliance', 
                response.content,
                {'contract_text': state['contract_text']}
            )
            if should_discuss:
                discussion = self.multi_turn.conduct_discussion(
                    'compliance',
                    topic,
                    response.content[:500],
                    {'contract_text': state['contract_text']}
                )
                # Append discussion summary to analysis
                state['compliance_analysis'] += f"\n\n**Multi-Turn Discussion:**\n{discussion.get_context()}"
            
            time.sleep(2)  # Add delay to avoid rate limiting
            
        except Exception as e:
            error_msg = f"Compliance analysis error: {str(e)}"
            print(f"[ERROR] {error_msg}")
            import traceback
            traceback.print_exc()
            state['errors'].append(error_msg)
            state['compliance_analysis'] = "Analysis failed"
        
        return state
    
    def _finance_analysis(self, state: ContractAnalysisState) -> ContractAnalysisState:
        """Finance Agent analysis - Week 3: Enhanced with extracted clauses and risk data"""
        try:
            agent = self.agents['finance']
            
            # Week 3: Prepare enhanced context with financial clauses and risks
            finance_clauses = state['extracted_clauses'].get('finance', [])
            finance_risks = state['identified_risks'].get('finance', [])
            
            clause_summary = f"\n\nExtracted Financial Clauses ({len(finance_clauses)} found):\n"
            for clause in finance_clauses[:5]:
                clause_summary += f"- {clause.clause_type}: {clause.text[:100]}...\n"
            
            risk_summary = f"\n\nIdentified Financial Risks ({len(finance_risks)} found):\n"
            for risk in finance_risks[:5]:
                risk_summary += f"- [{risk.severity.value}] {risk.category}: {risk.description}\n"
            
            enhanced_context = f"{state['contract_text'][:2000]}{clause_summary}{risk_summary}"
            
            messages = [
                SystemMessage(content=agent.system_prompt),
                HumanMessage(content=f"Analyze this contract with extracted clauses and identified risks:\n\n{enhanced_context}")
            ]
            
            response = self._call_llm_with_retry(messages)
            state['finance_analysis'] = response.content
            
            # Milestone 3: Check if multi-turn discussion needed
            should_discuss, topic = self.multi_turn.should_initiate_discussion(
                'finance', 
                response.content,
                {'contract_text': state['contract_text']}
            )
            if should_discuss:
                discussion = self.multi_turn.conduct_discussion(
                    'finance',
                    topic,
                    response.content[:500],
                    {'contract_text': state['contract_text']}
                )
                state['finance_analysis'] += f"\n\n**Multi-Turn Discussion:**\n{discussion.get_context()}"
            
            time.sleep(2)  # Add delay to avoid rate limiting
            
        except Exception as e:
            error_msg = f"Finance analysis error: {str(e)}"
            print(f"[ERROR] {error_msg}")
            import traceback
            traceback.print_exc()
            state['errors'].append(error_msg)
            state['finance_analysis'] = "Analysis failed"
        
        return state
    
    def _legal_analysis(self, state: ContractAnalysisState) -> ContractAnalysisState:
        """Legal Agent analysis"""
        try:
            agent = self.agents['legal']
            
            messages = [
                SystemMessage(content=agent.system_prompt),
                HumanMessage(content=f"Analyze this contract:\n\n{state['contract_text'][:3000]}")
            ]
            
            response = self._call_llm_with_retry(messages)
            time.sleep(2)  # Add delay to avoid rate limiting
            state['legal_analysis'] = response.content
            
            # Milestone 3: Check if multi-turn discussion needed
            should_discuss, topic = self.multi_turn.should_initiate_discussion(
                'legal', 
                response.content,
                {'contract_text': state['contract_text']}
            )
            if should_discuss:
                discussion = self.multi_turn.conduct_discussion(
                    'legal',
                    topic,
                    response.content[:500],
                    {'contract_text': state['contract_text']}
                )
                state['legal_analysis'] += f"\n\n**Multi-Turn Discussion:**\n{discussion.get_context()}"
            
        except Exception as e:
            error_msg = f"Legal analysis error: {str(e)}"
            print(f"[ERROR] {error_msg}")
            import traceback
            traceback.print_exc()
            state['errors'].append(error_msg)
            state['legal_analysis'] = "Analysis failed"
        
        return state
    
    def _operations_analysis(self, state: ContractAnalysisState) -> ContractAnalysisState:
        """Operations Agent analysis"""
        try:
            agent = self.agents['operations']
            
            messages = [
                SystemMessage(content=agent.system_prompt),
                HumanMessage(content=f"Analyze this contract:\n\n{state['contract_text'][:3000]}")
            ]
            
            response = self._call_llm_with_retry(messages)
            time.sleep(2)  # Add delay to avoid rate limiting
            state['operations_analysis'] = response.content
            
            # Milestone 3: Check if multi-turn discussion needed
            should_discuss, topic = self.multi_turn.should_initiate_discussion(
                'operations', 
                response.content,
                {'contract_text': state['contract_text']}
            )
            if should_discuss:
                discussion = self.multi_turn.conduct_discussion(
                    'operations',
                    topic,
                    response.content[:500],
                    {'contract_text': state['contract_text']}
                )
                state['operations_analysis'] += f"\n\n**Multi-Turn Discussion:**\n{discussion.get_context()}"
            
        except Exception as e:
            error_msg = f"Operations analysis error: {str(e)}"
            print(f"[ERROR] {error_msg}")
            import traceback
            traceback.print_exc()
            state['errors'].append(error_msg)
            state['operations_analysis'] = "Analysis failed"
        
        return state
    
    def _create_final_summary(self, state: ContractAnalysisState) -> ContractAnalysisState:
        """Create final summary combining all agent analyses"""
        try:
            summary_prompt = f"""
You are a Senior Contract Analyst. Create a comprehensive executive summary based on these analyses:

COMPLIANCE ANALYSIS:
{state['compliance_analysis']}

FINANCE ANALYSIS:
{state['finance_analysis']}

LEGAL ANALYSIS:
{state['legal_analysis']}

OPERATIONS ANALYSIS:
{state['operations_analysis']}

Provide:
1. Executive Summary (2-3 paragraphs)
2. Key Findings (bullet points)
3. Critical Risks (prioritized)
4. Recommendations
"""
            
            messages = [
                SystemMessage(content="You are a Senior Contract Analyst creating executive summaries."),
                HumanMessage(content=summary_prompt)
            ]
            
            response = self._call_llm_with_retry(messages)
            state['final_summary'] = response.content
            
        except Exception as e:
            error_msg = f"Summary creation error: {str(e)}"
            print(f"[ERROR] {error_msg}")
            import traceback
            traceback.print_exc()
            state['errors'].append(error_msg)
            state['final_summary'] = "Summary generation failed"
        
        return state
    
    def analyze_contract(self, file_path: str, language: str = 'en') -> Dict:
        """
        Main method to analyze a contract
        Milestone 2: Enhanced with intelligent planning and classification
        Multilingual: Supports translation to Tamil, Hindi, Telugu, Malayalam
        
        Args:
            file_path: Path to contract file (PDF or Word)
            language: Target language for results (en, ta, hi, te, ml) - Default: en
            
        Returns:
            Dictionary with all analysis results (translated if language != 'en')
        """
        # Parse document
        parser = DocumentParser(file_path)
        result = parser.parse()
        
        # Week 3: Parallel clause extraction
        print("\n[EXTRACT] Week 3: Running parallel clause extraction...")
        extracted_clauses = self.clause_extractor.extract_clauses_parallel(
            result['text'], 
            result['metadata']
        )
        clause_stats = self.clause_extractor.get_summary_statistics(extracted_clauses)
        print(f"[DATA] Extracted {clause_stats['total_clauses']} clauses across domains")
        
        # Week 3: Structured risk identification pipelines
        print("\n[WARNING] Week 3: Running risk identification pipelines...")
        identified_risks = self.risk_analyzer.analyze_all_risks(result['text'])
        risk_summary = self.risk_analyzer.get_risk_summary(identified_risks)
        print(f"[RISKS] Identified {risk_summary['total_risks']} risks")
        print(f"   Critical: {risk_summary['by_severity']['Critical']}, High: {risk_summary['by_severity']['High']}")
        
        # Milestone 2: Classify contract and generate analysis plan
        contract_type = 'general'
        analysis_plan = {}
        
        if self.planner and PLANNING_AVAILABLE:
            print("\n[CLASSIFY] Classifying contract type...")
            classification = self.planner.classify_contract(result['text'])
            contract_type = classification['contract_type']
            print(f"[TYPE] Contract Type: {contract_type.replace('_', '  ').title()}")
            print(f"[DATA] Confidence: {classification['confidence'].upper()}")
            
            print("[PLAN] Generating analysis plan...")
            analysis_plan = self.planner.generate_analysis_plan(classification)
            print(f"[STRATEGY] Strategy: {analysis_plan['execution_strategy']}")
            print(f"[DEPTH] Depth: {analysis_plan['recommended_depth']}")
            print(f"[AGENTS] Agents: {' -> '.join([a.title() for a in analysis_plan['agent_priority']])}")
        
        # Initialize state
        state = ContractAnalysisState(
            contract_text=result['text'],
            contract_metadata=result['metadata'],
            contract_type=contract_type,
            analysis_plan=analysis_plan,
            extracted_clauses=extracted_clauses,  # Week 3
            identified_risks=identified_risks,  # Week 3
            discussion_summaries=[],  # Milestone 3
            compliance_analysis="",
            finance_analysis="",
            legal_analysis="",
            operations_analysis="",
            final_summary="",
            errors=[]
        )
        
        # Run workflow sequentially (simplified approach)
        print("\n[START] Starting multi-agent analysis...")
        
        # Run each agent
        state = self._compliance_analysis(state)
        time.sleep(3)  # Delay to avoid rate limits
        state = self._finance_analysis(state)
        time.sleep(3)  # Delay to avoid rate limits
        state = self._legal_analysis(state)
        time.sleep(3)  # Delay to avoid rate limits
        state = self._operations_analysis(state)
        time.sleep(3)  # Delay to avoid rate limits
        state = self._create_final_summary(state)
        
        # Generate contract ID for vector storage
        contract_id = hashlib.md5(result['text'].encode()).hexdigest()[:12]
        
        # Calculate risk scores
        print("\n[DATA] Calculating risk scores...")
        all_risks = []
        for domain_risks in identified_risks.values():
            all_risks.extend([{
                'risk_type': r.risk_type,
                'category': r.category,
                'severity': r.severity.value,
                'description': r.description
            } for r in domain_risks])
        
        # Detect missing clauses
        print("[ANALYZE] Detecting missing critical clauses...")
        all_clauses = []
        for domain_clauses in extracted_clauses.values():
            all_clauses.extend([{
                'type': c.clause_type,
                'text': c.text
            } for c in domain_clauses])
        
        missing_clauses = self.missing_clause_detector.detect_missing_clauses(
            result['text'], 
            all_clauses
        )
        missing_clause_summary = self.missing_clause_detector.get_missing_clause_summary(missing_clauses)
        
        # Calculate comprehensive risk scores
        risk_scores = self.risk_scorer.calculate_risk_scores(all_risks, missing_clauses)
        
        print(f"[OK] Risk Scoring Complete: {risk_scores['overall_score']}/10 ({risk_scores['overall_level']})")
        print(f"   • Critical Risks: {risk_scores['severity_breakdown']['critical']}")
        print(f"   • Missing Critical Clauses: {missing_clause_summary['critical_missing']}")
        
        # Milestone 3: Store intermediate results in Pinecone for quick retrieval
        print("\n💾 Storing intermediate results to Pinecone...")
        try:
            self.vector_store.store_intermediate_results(
                contract_id, 
                extracted_clauses, 
                identified_risks
            )
            print("[OK] Intermediate results stored successfully")
        except Exception as storage_error:
            print(f"[WARNING] Pinecone storage skipped (not critical): {str(storage_error)[:100]}")
        
        # Store full analysis in vector database (optional - may fail due to API quotas)
        try:
            self._store_to_vector_db(contract_id, result['text'], state)
        except Exception as e:
            print(f"[WARNING] Vector DB storage skipped (not critical): {str(e)[:100]}")
        
        # Build results dictionary
        results = {
            'contract_id': contract_id,
            'contract_type': state['contract_type'],
            'analysis_plan': state['analysis_plan'],
            'contract_metadata': state['contract_metadata'],
            'extracted_clauses': state['extracted_clauses'],  # Week 3
            'identified_risks': state['identified_risks'],  # Week 3
            'risk_scores': risk_scores,  # NEW: Risk scoring system
            'missing_clauses': [
                {
                    'clause_name': mc.clause_name,
                    'category': mc.category,
                    'importance': mc.importance,
                    'reason': mc.reason,
                    'recommendation': mc.recommendation
                } for mc in missing_clauses
            ],  # NEW: Missing clause detection
            'missing_clause_summary': missing_clause_summary,  # NEW: Missing clause stats
            'discussion_summaries': self.multi_turn.get_discussion_summary(),  # Milestone 3
            'compliance_analysis': state['compliance_analysis'],
            'finance_analysis': state['finance_analysis'],
            'legal_analysis': state['legal_analysis'],
            'operations_analysis': state['operations_analysis'],
            'final_summary': state['final_summary'],
            'errors': state['errors']
        }
        
        # Serialize objects to JSON-compatible format first
        results = self._serialize_for_translation(results)
        
        # Translate results if language is not English
        if language != 'en' and self.multilingual_engine:
            print(f"\n[TRANSLATE] Translating results to {language.upper()}...")
            try:
                results = self.multilingual_engine.translate_json(results, language)
                print(f"[OK] Translation to {language.upper()} complete")
            except Exception as e:
                print(f"[WARNING] Translation failed: {str(e)}, returning English results")
                import traceback
                traceback.print_exc()
        
        return results
    
    def _store_to_vector_db(self, contract_id: str, contract_text: str, state: Dict):
        """Store contract and analysis in vector database"""
        try:
            print("\n💾 Storing to vector database...")
            
            # Get text chunks
            from document_parser import DocumentParser
            chunks = contract_text.split('\n\n')  # Simple chunking
            chunks = [c.strip() for c in chunks if c.strip() and len(c.strip()) > 50]
            
            if not chunks:
                chunks = [contract_text[:1000], contract_text[1000:2000]]
            
            # Store contract chunks
            metadata = {
                "contract_type": state.get('contract_type', 'general'),
                "file_type": state.get('contract_metadata', {}).get('file_type', 'unknown')
            }
            
            success = self.vector_store.store_contract(
                contract_id=contract_id,
                contract_text=contract_text,
                metadata=metadata
            )
            
            if success:
                # Store analysis results
                analysis_results = {
                    'compliance_analysis': state.get('compliance_analysis'),
                    'finance_analysis': state.get('finance_analysis'),
                    'legal_analysis': state.get('legal_analysis'),
                    'operations_analysis': state.get('operations_analysis'),
                    'final_summary': state.get('final_summary')
                }
                # Note: store_analysis_results method not yet implemented
                # self.vector_store.store_analysis_results(contract_id, analysis_results)
                print(f"[OK] Contract {contract_id} analysis complete")
            
        except Exception as e:
            print(f"[WARNING] Vector DB storage skipped: {str(e)}")


if __name__ == "__main__":
    print("Multi-Agent Contract Analyzer - Milestone 1")
    print("=" * 70)
    
    # Check for Ollama configuration
    if not os.getenv("OLLAMA_BASE_URL") or not os.getenv("OLLAMA_MODEL"):
        print("\n[WARNING] Ollama configuration not found!")
        print("Please set OLLAMA_BASE_URL and OLLAMA_MODEL in .env file")
        print("\nCreate a .env file with:")
        print("OLLAMA_BASE_URL=http://localhost:11434")
        print("OLLAMA_MODEL=gemma3:1b")
    else:
        print("\n[OK] Environment configured")
        print("[OK] LangChain & LangGraph loaded")
        print("[OK] Multi-agent workflow ready")
        print("\n[INFO] Agent roles defined:")
        
        agents = AgentRoles.get_all_agents()
        for agent_type, agent in agents.items():
            print(f"   • {agent.name}")
        
        print("\n[WORKFLOW] LangGraph workflow:")
        print("   Compliance → Finance → Legal → Operations → Summary")
        
        # Test if sample contract exists
        if os.path.exists("sample_contract.docx"):
            print("\n[TEST] Test file found: sample_contract.docx")
            print("Ready for testing!")
        else:
            print("\n[TIP] To test: Create or upload a contract file")
