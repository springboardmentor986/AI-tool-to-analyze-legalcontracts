# ClauseAI – Multi-Agent Contract Analyzer ⚖️

ClauseAI is an AI-powered contract analysis platform that uses **multi-agent LLM pipelines** to review legal documents, extract clauses, identify risks, and generate structured reports.

It is built using **LangGraph, Groq LLM, Pinecone Vector DB, and Streamlit UI**.

---

## 🚀 Features

- Multi-Agent Contract Review (Compliance, Finance, Legal, Operations)
- Clause Extraction & Risk Identification
- Parallel Agent Processing
- Dynamic Agent Prompt Chat (ChatGPT-style interaction)
- Vector Storage using Pinecone
- Structured Markdown Report Generation
- Downloadable Report Bundle (.md, .json, .zip)
- Clean SaaS-style Streamlit UI

---

## 🧠 Architecture

User Upload → Chunking → Vector Store (Pinecone)
→ Multi-Agent LLM Analysis (Parallel)
→ Report Builder → Streamlit UI

Agents:
- Compliance Agent
- Finance Agent
- Legal Agent
- Operations Agent

---

## 🛠 Tech Stack

| Layer | Technology |
|------|-----------|
| UI | Streamlit |
| LLM | Groq (LLaMA Models) |
| Orchestration | LangGraph |
| Vector DB | Pinecone |
| Embeddings | Sentence-Transformers |
| Parsing | PyPDF, Python-DOCX |
| Environment | Python 3.10+ |

---

## 📂 Project Structure

ClauseAI/
│
├── app.py
├── requirements.txt
├── README.md
│
└── src/clauseai/
├── config.py
├── graph.py
├── agents.py
├── vectorstore.py
├── embeddings.py
├── report.py
└── llm.py


---

## ⚙️ Installation

### 1. Clone Repo
git clone <your-repo-url>
cd ClauseAI

### 2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate

### 3. Install Dependencies
pip install -r requirements.txt

---

## 🔑 Environment Variables

Create `.env` file:

GROQ_API_KEY=your_groq_key
PINECONE_API_KEY=your_pinecone_key
LLM_PROVIDER=groq

---

## ▶️ Run Application
streamlit run app.py

---

## 📊 Workflow

1. Upload PDF/DOCX contract
2. Preview extracted text
3. Analyze contract
4. Review each agent output
5. Ask dynamic prompts to agents
6. Generate final report
7. Download bundle

---

## 📦 Output Files

- `report.md` – Structured contract review
- `output.json` – Raw agent outputs
- `contract.txt` – Extracted text
- `meta.json` – Run metadata

---

## 🧪 Milestones Completed

- **Milestone 1:** Clause Extraction & Vector Store
- **Milestone 2:** Multi-Agent Analysis Pipeline
- **Milestone 3:** Parallel Processing + UI + Dynamic Prompting

---

## ⚠️ Notes

- Large contracts may take longer.
- Pinecone index must be active.
- Groq API limits apply.

---

## 📌 Future Enhancements

- Clause Comparison Mode
- Redline Suggestions
- User Authentication
- Cloud Deployment

---

## 👨‍💻 Author

**Sumuth T S**

---

## 📄 License

MIT License
