# 📄 ClauseAI — AI-Powered Contract Intelligence Platform

ClauseAI is an end-to-end AI system that analyzes legal contracts using multiple specialized agents, Retrieval-Augmented Generation (RAG), and vector databases to provide structured risk insights, visual dashboards, and actionable recommendations.

It is designed for non-technical users, startups, and enterprises to understand complex contracts without legal expertise.

---

## 🚀 Key Features

### 🧠 Multi-Agent Contract Analysis
- Independent AI agents for:
  - Legal Risk
  - Compliance Risk
  - Financial Risk
  - Operational Risk
- Each agent produces structured summaries and clause-level insights.

### 🔗 LangGraph-Based Orchestration
- Uses LangGraph to coordinate multi-agent workflows
- Controls execution order and dependencies
- Enables scalable and modular AI pipelines
- Ensures reliable agent collaboration

### 🗄️ Pinecone Vector Database Integration
- Stores semantic embeddings of contract clauses
- Enables fast similarity search
- Powers Retrieval-Augmented Generation (RAG)
- Supports long-term contract memory

### 📊 Interactive Visualization Dashboard
- Risk Distribution Charts
- Agent-wise Risk Comparison
- Compliance & Health Scores
- Important Clause Tables
- Priority Action Panels

### 🔍 RAG-Based Question Answering
- Semantic search using Pinecone
- Query grounded only in contract clauses
- Prevents hallucinated answers
- Context-aware responses

### 📥 Customizable Report Generation
- Downloadable structured reports
- Adjustable tone and focus (business/legal/technical)
- Consolidated multi-agent summary

### 🤝 Negotiation AI (Prototype)
- Converts detected risks into negotiation suggestions
- Helps users revise contract terms before signing

### 🗺️ Smart Action Plan
- Step-by-step guidance after analysis
- Non-technical recommendations

### 🎨 Modern UI
- Light/Dark themes
- Dashboard-style interface
- Responsive layout

---

## 🏗️ System Architecture

```text
User → Streamlit UI
        ↓
Text Extraction
        ↓
LangGraph Orchestration
        ↓
Parallel AI Agents (Groq LLM)
        ↓
Structured JSON Output
        ↓
Pinecone Vector Storage
        ↓
RAG Query Engine
        ↓
Visualization + Reports

⚙️ Technology Stack
Category	Technology
Frontend	Streamlit
LLM	Groq (LLaMA 3.1)
Orchestration	LangGraph
Vector DB	Pinecone
Embeddings	Custom Embedding Service
Visualization	Plotly, Pandas
Backend	Python
Version Control	Git + GitHub
📁 Project Structure
ClauseAI/
│
├── streamlit_app.py          # Main Application
├── pages/
│   └── 1_📊_Visualization.py # Dashboard Page
│
├── langgraph_flow.py         # Agent Orchestration
│
├── embeddings/
│   └── embedding_service.py
│
├── vectorstore/
│   ├── pinecone_store.py
│   └── pinecone_query.py
│
├── qa/
│   └── answer_generator.py
│
├── pipelines/
│   ├── compliance_pipeline.py
│   └── finance_pipeline.py
│
├── .env
└── README.md

🔄 Workflow

User uploads a contract (PDF/DOCX/TXT)

Text is extracted

LangGraph coordinates AI agents

Agents run in parallel

Each agent generates:

Risk Summary

Key Clauses

Clause embeddings stored in Pinecone

Final verdict is generated

Visual dashboard is created

User can ask RAG-based questions

Report is generated and downloadable

🧩 How RAG Works

User enters a question

Query is converted to embedding

Pinecone retrieves similar clauses

Retrieved clauses sent to LLM

LLM generates grounded answer

This ensures:

No hallucination

High factual accuracy

Contract-specific responses

🗄️ Pinecone Integration

Each extracted clause is stored as:

{
  "contract_id": "contract_123",
  "agent": "Legal",
  "clause_type": "Termination",
  "embedding": [0.021, 0.113, ...],
  "metadata": {
    "risk_level": "High",
    "summary": "...",
    "recommendation": "..."
  }
}


Used for:

Semantic search

RAG pipeline

Historical contract analysis

🖥️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/your-username/ClauseAI.git
cd ClauseAI

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Setup Environment

Create .env file:

GROQ_API_KEY=your_key
PINECONE_API_KEY=your_key
PINECONE_ENV=your_env

5️⃣ Run Application
streamlit run streamlit_app.py

📈 Performance Optimizations

Parallel agent execution using ThreadPoolExecutor

Cached embeddings

Chunked contract processing

Retry mechanism for LLM failures

Lightweight JSON validation

🌟 Future Enhancements

Multi-file contract comparison

Clause similarity analysis

Contract version tracking

OCR for scanned documents

User authentication

SaaS deployment

Team collaboration dashboard
👩‍💻 Developer

Pari
AI & Data Science Engineer
B.Tech (AI & DS)

📫 Email: paribhattacharya05@gmail.com

🔗 LinkedIn: (https://www.linkedin.com/in/pari-bhattacharya-4a2187291/)

📜 License

This project is licensed under the MIT License.

⭐ Acknowledgements

Groq LLM

Pinecone

Streamlit

LangGraph

Open Source Community

If you found this project useful, please consider giving it a ⭐ on GitHub!






