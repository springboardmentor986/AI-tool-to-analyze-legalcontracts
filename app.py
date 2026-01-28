import streamlit as st
from config.settings import settings
import os
#  key 
os.environ["GROQ_API_KEY"] = settings.GROQ_KEY
os.environ["PINECONE_API_KEY"] = settings.PINECONE_KEY
import re     # to remove error
from dotenv import load_dotenv
from graph import get_workflow
from router_agent import classify_contract , assign_expert
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings 
from agents import get_document_text

# . Sabse pehle Configuration
st.set_page_config(layout="wide", page_title="ClauseAI Dashboard")
# 2.CUSTOM CSS 
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top center, #2e1065 0%, #020617 100%);
    }
    h1 {
        color: white; font-family: 'Inter', sans-serif; text-align: center;
        font-weight: 800; text-shadow: 0 0 20px rgba(168, 85, 247, 0.4);
    }
    .card-container {
        display: flex; justify-content: space-around; gap: 20px; margin-top: 50px;
    }
    .card {
        background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px; border-radius: 15px; text-align: center; transition: 0.3s; flex: 1;
    }
    .card:hover {
        background: rgba(255, 255, 255, 0.1); border-color: #a855f7; transform: translateY(-5px);
    }
    </style>
    """, unsafe_allow_html=True)
# 3.LANDING PAGE CONTENT
st.markdown("<h1>Know what you sign</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Automated legal analysis, powered by Multi-Agent AI</p>", unsafe_allow_html=True)
st.markdown("""
<div class="card-container">
    <div class="card"><h3>📊</h3><p style='color:white;'>Contract Analytics</p></div>
    <div class="card"><h3>⚖️</h3><p style='color:white;'>Legal Simplifier</p></div>
    <div class="card"><h3>🛡️</h3><p style='color:white;'>Compliance Tools</p></div>
    <div class="card"><h3>🕸️</h3><p style='color:white;'>Legal Graph Data</p></div>
</div>
""", unsafe_allow_html=True)
st.markdown("<br><hr style='border: 0.5px solid rgba(255,255,255,0.1);'><br>", unsafe_allow_html=True)
# 4. FILE UPLOAD LOGIC
uploaded_file = st.file_uploader("📤 Upload Legal Document (PDF or DOCX)", type=["pdf", "docx"])
if uploaded_file:

    #Define Variable
    metadata_res = "" 
    contract_type = "Analyzing..."
    score, exposure, flags = "N/A", "N/A", "0"

    # --- MILESTONE 1: EXTRACTION (Purana Logic) ---
    file_extension = os.path.splitext(uploaded_file.name)[1]
    temp_filename = f"temp_document{file_extension}" 
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())
    # Text nikalna [cite: 33]
    text = get_document_text(temp_filename)
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    st.toast("File Uploaded Successfully!", icon="📄")
    
    # --- AUTOMATIC ENGINE STARTS HER
    brain_app = get_workflow()
    with st.status("🧠 ClauseAI Brain (LangGraph) is thinking...", expanded=True) as status:
        st.write("⚙️ Running Agentic Workflow.....") 
        # AI se puchenge ye kya hai 
        inputs = {"contract_text": text}
        result = brain_app.invoke(inputs) # Yahan poora graph chalega!
        #  Result dikhao
        contract_type = result['domain']
        analysis_plan = result['plan'] 
        st.info(f"**Domain Identified:** {contract_type}")
        st.success(f"**AI Strategy:** {analysis_plan}")

        #  PARALLEL ANALYSIS 
        #  Pehle Dictionary define karo (Loop se pehle)
        agents_roles = {
        "Compliance": "Aap ek legal expert hain jo contract mein kanooni galtiyan dhoondte hain.",
        "Finance": "Aap ek finance expert hain jo payment terms aur money risks check karte hain.",
        "Legal": "Aap contract ke clauses ko interpret karte hain.",
        "operational": "Aap dekhte hain ki contract ki shartein business operations ke liye sahi hain ya nahi."
        }
        st.write("🧠 **Node 2: Running Parallel Multi-Agent Analysis...**")
        # Ye agents Compliance, Finance aur Legal domains check karenge [cite: 34]
        domains = ["Compliance", "Finance", "Legal", "operational"]  
        cols = st.columns(4)
        for i, domain in enumerate(domains):
            with cols[i]:
                st.markdown(f"**{domain} Agent**")
                # Sahi role uthana (Key match karke)
                system_role = agents_roles.get(domain, "Legal Expert")
                # Har domain ka alag analysis [cite: 9, 12]
                agent_query = f"Analyze {domain} risks in this {contract_type}: {text[:100]}"
                res = llm.invoke(agent_query).content
                st.caption(res)

        #st.write("🔑 **Node 2.5: Extracting Metadata...**")
        meta_prompt = f"Extract Jurisdiction, Expiry Date, and Liability Cap. Separate by new lines: {text[:200]}"
        metadata_res = llm.invoke(meta_prompt).content
        
        # 3. VECTOR STORAGE 
        st.write("💾 **Node 3: Indexing in Pinecone...**")
        # Chunks banana (Document ko chhote tukdo mein todna)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_text(text)
        # Embeddings Model (Jo text ko numbers mein badlega)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        # Pinecone mein save karna
        index_name = "clause-ai"  # Jo aapne Pinecone dashboard pe banaya hai
        vectorstore = PineconeVectorStore.from_texts(
            chunks, 
            embeddings, 
            index_name=index_name
        )
        st.write(f"✅ {len(chunks)} Chunks stored successfully!")

    st.markdown("---") # Ek line separation ke liye
    # 1. Advanced Risk Heatmap (Milestone 4: Polished UI)
    # --- STEP: AI se Dashboard Metrics nikalwana ---
    dashboard_prompt = f"""
            Analyze the following contract and provide exactly three values separated by commas:
            1. A Compliance Score (0-100%)
            2. Financial Exposure level (Low, Medium, or High)
            3. Number of Legal Red Flags found.
            Contract Text: {text[:200]}   
            """
    # AI se response lena
    db_res = llm.invoke(dashboard_prompt).content
    # Response ko tod kar variables mein dalna (e.g., "90%, Low, 1")
    try:
        metrics = [m.strip() for m in db_res.split(',')]
        score = metrics[0]
        exposure = metrics[1]
        flags = metrics[2]
    except:
        # Agar AI thoda alag format de de toh backup values
        score, exposure, flags = "N/A", "Analyzing...", "0"
    # --- AB DASHBOARD MEIN VARIABLES DALO ---
    st.subheader("📊 Executive Decision Dashboard")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric(label="Compliance Score", value=score, delta="Based on Clauses")
    with col_b:
        st.metric(label="Financial Exposure", value=exposure, delta="Market Risk")
    with col_c:
        st.metric(label="Legal Red Flags", value=flags, delta="Requires Review", delta_color="inverse")
        
        
    # 2. Key Metadata Table (For quick reading)
    st.markdown("#### 🔑 Critical Contract Metadata")
    m_list = metadata_res.split('\n') if metadata_res else ["N/A", "N/A", "N/A"]
    st.table({
    "Attribute": ["Contract Type", "Jurisdiction", "Expiry Date", "Liability Cap"],
    "Value": [
        contract_type,
        m_list[0] if len(m_list) > 0 else "N/A",
        m_list[1] if len(m_list) > 1 else "N/A",
        m_list[2] if len(m_list) > 2 else "N/A"
        ]
    })
    # 3. RAG CHATBOT (Real AI Integration)
    st.markdown("---")
    st.subheader("💬 Chat with your Contract")
    user_query = st.text_input("Ask anything (e.g., 'What is the notice period?')")
    if user_query:
        with st.spinner("🤖 AI is thinking..."):
            # Hum AI ko bhej rahe hain: 1. Pura contract, 2. User ka sawal
            chat_prompt = f"""
            You are a legal assistant. Answer the user's question based ONLY on the contract text provided.
            If the answer is not in the text, say 'Information not found'.
            Contract Text: {text[:100]} 
            User Question: {user_query}
            """
            # AI se asli answer mangwana
            response = llm.invoke(chat_prompt).content
            # Asli answer screen pe dikhana
            st.chat_message("assistant").write(response)
       
         # SUCCESS ANIMATION
    st.balloons() # Isse poore screen par balloons udenge🎈🎈
    status.update(label="✅ All Milestones Completed!", state="complete")
        # Final Celebration Message with Emoji
    st.success("🎉 Congratulations! Contract Analysis is Ready! 😘")

else:
        st.info("Please upload a legal document to begin automation.")
    
#    python -m streamlit run app.py  for run app😘