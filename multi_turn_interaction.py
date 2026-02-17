"""
Multi-Turn Agent Interaction Module
Milestone 3 - Week 5-6

Enables agents to have discussions and ask follow-up questions
for deeper analysis and clarification.
"""

import time
from typing import Dict, List, Tuple
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


class AgentDiscussion:
    """Represents a discussion thread between agents"""
    
    def __init__(self, topic: str, initiator: str):
        self.topic = topic
        self.initiator = initiator
        self.messages = []
        self.participants = [initiator]
        self.resolved = False
    
    def add_message(self, agent: str, message: str):
        """Add a message to the discussion"""
        self.messages.append({
            'agent': agent,
            'message': message,
            'timestamp': time.time()
        })
        if agent not in self.participants:
            self.participants.append(agent)
    
    def get_context(self) -> str:
        """Get full discussion context"""
        context = f"Discussion Topic: {self.topic}\n\n"
        for msg in self.messages:
            context += f"{msg['agent']}: {msg['message']}\n\n"
        return context


class MultiTurnInteraction:
    """
    Manages multi-turn interactions between agents
    Enables agents to discuss findings and clarify ambiguities
    """
    
    def __init__(self, llm: ChatGoogleGenerativeAI, agents: Dict):
        self.llm = llm
        self.agents = agents
        self.discussions = []
        self.interaction_limit = 3  # Max turns per discussion
    
    def should_initiate_discussion(self, agent_name: str, analysis: str, 
                                   context: Dict) -> Tuple[bool, str]:
        """
        Determine if an agent should start a discussion with another agent
        
        Returns:
            (should_discuss, topic)
        """
        # Check for ambiguity indicators in analysis
        ambiguity_keywords = [
            'unclear', 'ambiguous', 'needs clarification', 'not specified',
            'vague', 'uncertain', 'conflicting', 'inconsistent'
        ]
        
        analysis_lower = analysis.lower()
        has_ambiguity = any(keyword in analysis_lower for keyword in ambiguity_keywords)
        
        if not has_ambiguity:
            return False, ""
        
        # Determine topic based on agent type and content
        if agent_name == 'compliance' and ('payment' in analysis_lower or 'financial' in analysis_lower):
            return True, "Clarification needed on compliance aspects of financial terms"
        elif agent_name == 'finance' and ('liability' in analysis_lower or 'legal' in analysis_lower):
            return True, "Financial implications of legal clauses need discussion"
        elif agent_name == 'legal' and ('deliverable' in analysis_lower or 'timeline' in analysis_lower):
            return True, "Legal review of operational commitments"
        elif agent_name == 'operations' and ('compliance' in analysis_lower or 'regulatory' in analysis_lower):
            return True, "Operational impact of compliance requirements"
        
        return False, ""
    
    def get_relevant_agent(self, topic: str) -> str:
        """Determine which agent should respond to a topic"""
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ['financial', 'payment', 'cost', 'price']):
            return 'finance'
        elif any(word in topic_lower for word in ['legal', 'liability', 'termination', 'ip']):
            return 'legal'
        elif any(word in topic_lower for word in ['compliance', 'regulatory', 'audit', 'gdpr']):
            return 'compliance'
        elif any(word in topic_lower for word in ['operational', 'deliverable', 'timeline', 'sla']):
            return 'operations'
        
        return 'legal'  # Default
    
    def conduct_discussion(self, initiator: str, topic: str, 
                          initial_context: str, contract_data: Dict) -> AgentDiscussion:
        """
        Conduct a multi-turn discussion between agents
        
        Args:
            initiator: Name of agent starting discussion
            topic: Discussion topic
            initial_context: Context that prompted the discussion
            contract_data: Contract text and extracted data
            
        Returns:
            AgentDiscussion with full conversation
        """
        print(f"\n🗣️  Multi-turn discussion initiated by {initiator.upper()}")
        print(f"   Topic: {topic}")
        
        discussion = AgentDiscussion(topic, initiator)
        
        # Initiating agent's question
        initiator_agent = self.agents.get(initiator)
        if not initiator_agent:
            return discussion
        
        initial_question = self._generate_question(
            initiator, 
            initiator_agent, 
            topic, 
            initial_context,
            contract_data
        )
        
        discussion.add_message(initiator, initial_question)
        print(f"   {initiator}: {initial_question[:100]}...")
        
        # Determine responding agent
        responder = self.get_relevant_agent(topic)
        if responder == initiator:
            # Find alternative responder
            all_agents = ['compliance', 'finance', 'legal', 'operations']
            all_agents.remove(initiator)
            responder = all_agents[0]
        
        # Multi-turn interaction
        current_turn = 0
        while current_turn < self.interaction_limit:
            time.sleep(2)  # Rate limiting
            
            # Responding agent's response
            responder_agent = self.agents.get(responder)
            if not responder_agent:
                break
            
            response = self._generate_response(
                responder,
                responder_agent,
                discussion.get_context(),
                contract_data
            )
            
            discussion.add_message(responder, response)
            print(f"   {responder}: {response[:100]}...")
            
            # Check if discussion resolved
            if self._is_discussion_resolved(response):
                discussion.resolved = True
                print(f"   ✅ Discussion resolved after {current_turn + 1} turns")
                break
            
            # Initiator's follow-up (if not resolved)
            if current_turn < self.interaction_limit - 1:
                time.sleep(2)
                follow_up = self._generate_followup(
                    initiator,
                    initiator_agent,
                    discussion.get_context(),
                    contract_data
                )
                
                discussion.add_message(initiator, follow_up)
                print(f"   {initiator}: {follow_up[:100]}...")
                
                if self._is_discussion_resolved(follow_up):
                    discussion.resolved = True
                    print(f"   ✅ Discussion resolved after {current_turn + 1} turns")
                    break
            
            current_turn += 1
        
        self.discussions.append(discussion)
        return discussion
    
    def _generate_question(self, agent_name: str, agent: any, topic: str,
                          context: str, contract_data: Dict) -> str:
        """Generate initial question from initiating agent"""
        prompt = f"""You are the {agent_name.upper()} agent and you found something unclear in your analysis.

TOPIC: {topic}

YOUR ANALYSIS EXCERPT:
{context[:500]}

CONTRACT EXCERPT:
{contract_data.get('contract_text', '')[:500]}

Ask a specific, focused question to clarify this issue. Be concise (2-3 sentences)."""

        messages = [
            SystemMessage(content=agent.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"Need clarification on: {topic}"
    
    def _generate_response(self, agent_name: str, agent: any, 
                          discussion_context: str, contract_data: Dict) -> str:
        """Generate response from responding agent"""
        prompt = f"""You are the {agent_name.upper()} agent responding to a colleague's question.

DISCUSSION SO FAR:
{discussion_context}

CONTRACT EXCERPT:
{contract_data.get('contract_text', '')[:500]}

Provide a helpful, specific answer from your domain expertise. Be concise (3-4 sentences)."""

        messages = [
            SystemMessage(content=agent.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return "Based on my analysis, the terms appear standard for this contract type."
    
    def _generate_followup(self, agent_name: str, agent: any,
                          discussion_context: str, contract_data: Dict) -> str:
        """Generate follow-up question or acknowledgment"""
        prompt = f"""You are the {agent_name.upper()} agent in a discussion.

DISCUSSION SO FAR:
{discussion_context}

Either:
1. Acknowledge if your question is answered (say "Thank you, that clarifies...")
2. Ask a focused follow-up question if still unclear

Be concise (1-2 sentences)."""

        messages = [
            SystemMessage(content=agent.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return "Thank you for the clarification."
    
    def _is_discussion_resolved(self, message: str) -> bool:
        """Check if discussion is resolved based on message content"""
        resolution_keywords = [
            'thank you', 'clarifies', 'understood', 'clear now',
            'makes sense', 'resolved', 'no further questions'
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in resolution_keywords)
    
    def get_discussion_summary(self) -> List[str]:
        """Generate summary of all discussions as a list"""
        if not self.discussions:
            return []
        
        summaries = []
        for discussion in self.discussions:
            # Format each discussion as a complete string
            summary = f"**Topic:** {discussion.topic}\n\n"
            summary += f"**Participants:** {', '.join(discussion.participants)}\n\n"
            summary += f"**Status:** {'✅ Resolved' if discussion.resolved else '⏳ Ongoing'}\n\n"
            summary += f"**Conversation ({len(discussion.messages)} messages):**\n\n"
            
            for msg in discussion.messages:
                agent_emoji = {
                    'compliance': '📋',
                    'finance': '💰',
                    'legal': '⚖️',
                    'operations': '🔧'
                }.get(msg['agent'], '💬')
                
                summary += f"{agent_emoji} **{msg['agent'].title()}:**\n"
                summary += f"{msg['message']}\n\n"
            
            summaries.append(summary)
        
        return summaries


if __name__ == "__main__":
    print("Multi-Turn Agent Interaction Module - Milestone 3")
    print("=" * 60)
    print("Enables agents to discuss and clarify findings")
    print("Features:")
    print("  - Automatic ambiguity detection")
    print("  - Agent-to-agent discussions")
    print("  - Multi-turn conversations (up to 3 turns)")
    print("  - Resolution tracking")
