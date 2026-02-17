"""
Contract Chat System with RAG (Retrieval-Augmented Generation)
Interactive Q&A for contract analysis using vector database and agents
"""

import os
import sys
from typing import Dict, List, Any

# Fix Windows console UTF-8 encoding for emoji support
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
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


class ContractChatbot:
    """
    Interactive chatbot for contract Q&A
    Uses RAG with vector store and multi-agent analysis
    """
    
    def __init__(self, google_api_key: str = None):
        """Initialize chatbot with local Ollama and vector store"""
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "qwen3:8b")
        
        if not self.ollama_base_url or not self.ollama_model:
            raise ValueError("Ollama configuration missing")
        
        # Create wrapper for local Ollama
        self.llm = OllamaLLMWrapper(self.ollama_base_url, self.ollama_model)
        
        # Store contract context
        self.contract_context = {}
        self.conversation_history = []
        
        print("[OK] Contract Chatbot initialized")
    
    def load_contract_context(self, contract_id: str, analysis_results: Dict):
        """
        Load contract analysis results into chatbot context
        
        Args:
            contract_id: Unique contract identifier
            analysis_results: Full analysis results from multi-agent analyzer
        """
        self.contract_context[contract_id] = {
            'contract_text': analysis_results.get('contract_metadata', {}).get('text', ''),
            'final_summary': analysis_results.get('final_summary', ''),
            'compliance_analysis': analysis_results.get('compliance_analysis', ''),
            'finance_analysis': analysis_results.get('finance_analysis', ''),
            'legal_analysis': analysis_results.get('legal_analysis', ''),
            'operations_analysis': analysis_results.get('operations_analysis', ''),
            'extracted_clauses': analysis_results.get('extracted_clauses', {}),
            'identified_risks': analysis_results.get('identified_risks', {}),
            'risk_scores': analysis_results.get('risk_scores', {}),
            'missing_clauses': analysis_results.get('missing_clauses', [])
        }
        
        print(f"[OK] Contract context loaded for {contract_id}")
    
    def answer_question(self, contract_id: str, question: str, language: str = 'en') -> Dict[str, Any]:
        """
        Answer user question about the contract
        
        Args:
            contract_id: Contract identifier
            question: User's question
            language: Target language for response
            
        Returns:
            Dictionary with answer and relevant context
        """
        if contract_id not in self.contract_context:
            return {
                'answer': 'Contract not found. Please analyze a contract first.',
                'sources': [],
                'confidence': 'low'
            }
        
        context = self.contract_context[contract_id]
        
        # Build comprehensive context for LLM
        contract_summary = f"""
CONTRACT ANALYSIS SUMMARY:
==========================

EXECUTIVE SUMMARY:
{context['final_summary'][:500]}

COMPLIANCE ANALYSIS:
{context['compliance_analysis'][:500]}

FINANCIAL ANALYSIS:
{context['finance_analysis'][:500]}

LEGAL ANALYSIS:
{context['legal_analysis'][:500]}

OPERATIONS ANALYSIS:
{context['operations_analysis'][:500]}

RISK SCORES:
Overall Risk: {context['risk_scores'].get('overall_score', 'N/A')} ({context['risk_scores'].get('overall_level', 'N/A')})

IDENTIFIED RISKS:
{self._format_risks(context['identified_risks'])}

MISSING CLAUSES:
{self._format_missing_clauses(context['missing_clauses'])}
"""
        
        # Create system prompt
        system_prompt = f"""You are a professional legal contract analyst assistant.

Your role: Answer questions about the analyzed contract based ONLY on the provided contract analysis.

Guidelines:
1. Answer based ONLY on the analyzed contract information provided
2. Be specific and cite relevant sections when available
3. If information is not in the analysis, clearly state "This information is not available in the current analysis"
4. For legal questions, provide clear, actionable answers
5. For payment/financial questions, refer to the financial analysis
6. For termination questions, refer to legal and extracted clauses
7. For risk questions, refer to risk analysis and scores
8. Use professional but clear language
9. Keep answers concise (2-4 sentences) unless more detail is needed
10. Always cite confidence level (High/Medium/Low) based on available information

CONTRACT ANALYSIS:
{contract_summary}
"""
        
        # Get answer from LLM
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"USER QUESTION: {question}")
        ]
        
        try:
            response = self.llm.invoke(messages)
            answer = response.content.strip()
            
            # Extract relevant sources
            sources = self._extract_relevant_sources(question, context)
            
            # Determine confidence
            confidence = self._assess_confidence(answer, context)
            
            # Store in conversation history
            self.conversation_history.append({
                'question': question,
                'answer': answer,
                'contract_id': contract_id
            })
            
            result = {
                'answer': answer,
                'sources': sources,
                'confidence': confidence,
                'language': language
            }
            
            # Translate if needed
            if language != 'en':
                from multilingual_engine import MultilingualEngine
                engine = MultilingualEngine()
                result['answer'] = engine.translate_text(answer, language)
            
            return result
            
        except Exception as e:
            print(f"[ERROR] Error answering question: {str(e)}")
            return {
                'answer': f'Error processing question: {str(e)}',
                'sources': [],
                'confidence': 'low'
            }
    
    def _format_risks(self, identified_risks: Dict) -> str:
        """Format identified risks for context"""
        formatted = []
        for domain, risks in identified_risks.items():
            if risks:
                formatted.append(f"\n{domain.upper()} RISKS:")
                for risk in risks[:3]:  # Top 3 per domain
                    if hasattr(risk, 'description'):
                        formatted.append(f"  - {risk.description}")
                    elif isinstance(risk, dict):
                        formatted.append(f"  - {risk.get('description', 'Unknown risk')}")
        return '\n'.join(formatted) if formatted else 'No significant risks identified'
    
    def _format_missing_clauses(self, missing_clauses: List) -> str:
        """Format missing clauses for context"""
        if not missing_clauses:
            return 'All critical clauses present'
        
        formatted = []
        for clause in missing_clauses[:5]:  # Top 5
            if isinstance(clause, dict):
                name = clause.get('clause_name', 'Unknown')
                importance = clause.get('importance', 'N/A')
                formatted.append(f"  - {name} ({importance})")
        
        return '\n'.join(formatted) if formatted else 'All critical clauses present'
    
    def _extract_relevant_sources(self, question: str, context: Dict) -> List[str]:
        """Extract relevant analysis sections based on question"""
        sources = []
        question_lower = question.lower()
        
        # Payment-related
        if any(word in question_lower for word in ['payment', 'pay', 'money', 'financial', 'cost', 'fee']):
            sources.append('Financial Analysis')
        
        # Termination-related
        if any(word in question_lower for word in ['terminate', 'termination', 'end', 'cancel', 'exit']):
            sources.append('Legal Analysis')
        
        # Risk-related
        if any(word in question_lower for word in ['risk', 'danger', 'concern', 'issue', 'problem']):
            sources.append('Risk Analysis')
        
        # Compliance-related
        if any(word in question_lower for word in ['comply', 'compliance', 'regulation', 'legal', 'law']):
            sources.append('Compliance Analysis')
        
        # Penalty-related
        if any(word in question_lower for word in ['penalty', 'fine', 'penalize', 'violation']):
            sources.append('Financial Analysis')
            sources.append('Legal Analysis')
        
        return list(set(sources)) if sources else ['General Analysis']
    
    def _assess_confidence(self, answer: str, context: Dict) -> str:
        """Assess confidence level of the answer"""
        answer_lower = answer.lower()
        
        # Low confidence indicators
        if any(phrase in answer_lower for phrase in [
            'not available', 'unclear', 'not mentioned', 'cannot determine',
            'insufficient information', 'not specified'
        ]):
            return 'low'
        
        # High confidence indicators
        if any(phrase in answer_lower for phrase in [
            'clearly states', 'specifically mentions', 'explicitly', 'defined as',
            'according to', 'clause indicates'
        ]):
            return 'high'
        
        # Default to medium
        return 'medium'
    
    def get_suggested_questions(self, contract_id: str) -> List[str]:
        """
        Generate suggested questions based on contract analysis
        
        Args:
            contract_id: Contract identifier
            
        Returns:
            List of suggested questions
        """
        if contract_id not in self.contract_context:
            return []
        
        context = self.contract_context[contract_id]
        suggestions = []
        
        # Always suggest these
        suggestions.extend([
            "What are the main risks in this contract?",
            "What is my payment obligation?",
            "When can I terminate this contract?"
        ])
        
        # Add based on missing clauses
        if context['missing_clauses']:
            suggestions.append("What important clauses are missing?")
        
        # Add based on risk level
        risk_level = context['risk_scores'].get('overall_level', '')
        if 'High' in risk_level or 'Critical' in risk_level:
            suggestions.append("What are the critical issues I should address immediately?")
        
        # Add based on identified risks
        if context['identified_risks']:
            suggestions.append("Are there any compliance concerns?")
            suggestions.append("What are the financial risks?")
        
        return suggestions[:6]  # Return top 6
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("[OK] Conversation history cleared")


# Test function
if __name__ == "__main__":
    print("Contract Chatbot Test")
    print("=" * 60)
    
    # Create mock analysis results
    mock_analysis = {
        'final_summary': 'This is an employment contract with moderate risk level.',
        'compliance_analysis': 'Contract complies with basic employment regulations.',
        'finance_analysis': 'Monthly payment of $5,000. Payment terms are clear.',
        'legal_analysis': 'Termination clause allows termination with 30 days notice.',
        'operations_analysis': 'Standard employment responsibilities.',
        'risk_scores': {'overall_score': 5.5, 'overall_level': 'Medium Risk'},
        'identified_risks': {},
        'missing_clauses': []
    }
    
    # Test chatbot
    chatbot = ContractChatbot()
    chatbot.load_contract_context('test123', mock_analysis)
    
    # Test questions
    questions = [
        "What is my payment obligation?",
        "When can I terminate?",
        "Is there a penalty clause?"
    ]
    
    for q in questions:
        print(f"\n❓ Q: {q}")
        result = chatbot.answer_question('test123', q)
        print(f"💬 A: {result['answer']}")
        print(f"📊 Sources: {', '.join(result['sources'])}")
        print(f"[OK] Confidence: {result['confidence']}")
