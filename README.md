# 📑 ClauseAI: Advanced Legal Contract Analyzer

**ClauseAI** ek AI-powered tool hai jo complex legal documents (PDF/Docx) ko analyze karta hai. Ye **Multi-Agent Architecture** aur **RAG (Retrieval-Augmented Generation)** ka use karke contract ke critical clauses, financial implications, aur compliance issues ko turant detect karta hai.

---

## 🚀 Key Features
* **Intelligent Routing:** Router agent document ko identify karta hai (Finance, Legal, ya Compliance).
* **Multi-Agent Workflow:** Har domain ke liye dedicated AI experts.
* **Vector Search:** Pinecone ka use karke fast aur accurate context retrieval.
* **Hybrid Parsing:** PDF aur Word files se structured data extraction.

---

## 🛠️ Tech Stack
* **Framework:** Streamlit (Frontend), LangGraph (Agent Orchestration)
* **LLM:** Groq (Llama-3.3-70b-versatile)
* **Database:** Pinecone (Vector Database)
* **Embeddings:** HuggingFace (sentence-transformers)
* **Parsing:** pdfplumber, python-docx

---

## 📂 Project Structure
- `app.py`: Main entry point (Streamlit UI).
- `graph.py`: LangGraph workflow logic.
- `router_agent.py`: Intelligent classification logic.
- `config/`: Centralized environment & settings management.
- `agents.py`: Expert agents definition.
- `utils/`: Helper functions for document loading and DB connections.

---

## ⚙️ Setup Instructions

1. **Clone the repo:**
   ```bash
   git clone <your-repo-link>
   cd clauseAI