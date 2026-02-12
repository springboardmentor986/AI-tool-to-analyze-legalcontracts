import streamlit as st
from utils.universal_llm import universal_llm
from utils.helpers import clean_raw_output

def show():
    st.title("🔮 The Oracle")
    st.markdown("<p style='color: #94a3b8;'>Chat with your specific AI Agents about the contract.</p>", unsafe_allow_html=True)

    # 1. Safety Check
    if not st.session_state['results']:
        st.info("⚠️ Please analyze a contract in the 'Main Console' first to populate the agents.")
        return

    # 2. Agent Tabs
    # We create a tab for each specialist
    tabs = st.tabs(["⚖️ Legal Agent", "💰 Finance Agent", "🛡️ Compliance Agent", "⚙️ Ops Agent"])

    # 3. Chat Logic Helper
    def render_agent_chat(agent_key, tab_obj, agent_icon):
        with tab_obj:
            # A. Display History
            chat_container = st.container(height=500)
            with chat_container:
                for msg in st.session_state['chat_history'][agent_key]:
                    role = msg['role']
                    content = msg['content']
                    
                    if role == "user":
                        # FIX: Explicit avatar prevents the "fac" glitch
                        with st.chat_message("user", avatar="👤"): 
                            st.write(content)
                    else:
                        with st.chat_message("assistant", avatar=agent_icon):
                            st.write(content)

            # B. Chat Input
            if prompt := st.chat_input(f"Ask the {agent_key.title()} Agent...", key=f"chat_{agent_key}"):
                
                # 1. Add User Message to History & UI
                st.session_state['chat_history'][agent_key].append({"role": "user", "content": prompt})
                with chat_container:
                    with st.chat_message("user", avatar="👤"):
                        st.write(prompt)

                # 2. Prepare Context (RAG)
                agent_data = st.session_state['results'].get(agent_key, {})
                raw_summary = agent_data.get('summary', '')
                context = clean_raw_output(raw_summary)
                
                # --- PROMPT ENGINEERED TO FIX THE "DUMP" ISSUE ---
                full_prompt = f"""
                You are the {agent_key.upper()} Expert Agent.
                
                CONTEXT (Your Analysis of the Contract):
                {context}
                
                USER QUESTION:
                {prompt}
                
                INSTRUCTIONS:
                1. If the user is greeting you (e.g., "hi", "hello"), introduce yourself briefly and mention one key risk from your analysis. DO NOT output the full summary.
                2. If the user asks a question, answer strictly based on the context above.
                3. Keep it professional and concise.
                """

                # 3. Generate Answer
                with chat_container:
                    with st.chat_message("assistant", avatar=agent_icon):
                        response_placeholder = st.empty()
                        response_placeholder.markdown("Thinking...")
                        
                        try:
                            # Call AI
                            ai_response_raw = universal_llm.invoke(full_prompt).content
                            ai_response_clean = clean_raw_output(ai_response_raw)
                            
                            # Update UI
                            response_placeholder.markdown(ai_response_clean)
                            
                            # Save to History
                            st.session_state['chat_history'][agent_key].append({"role": "ai", "content": ai_response_clean})
                            
                        except Exception as e:
                            response_placeholder.error(f"Connection Error: {e}")

    # 4. Render the 4 Interfaces with specific icons
    render_agent_chat("legal", tabs[0], "⚖️")
    render_agent_chat("finance", tabs[1], "💰")
    render_agent_chat("compliance", tabs[2], "🛡️")
    render_agent_chat("operations", tabs[3], "⚙️")