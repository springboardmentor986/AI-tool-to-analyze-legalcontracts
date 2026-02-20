# ClauseAI – Multi-Agent Contract Analyzer ⚖️

ClauseAI is an AI-powered contract analysis platform that uses **multi-agent LLM pipelines** to review legal documents, extract clauses, identify risks, and generate structured reports.

It is built using **LangGraph, Groq LLM, Pinecone Vector DB, and Streamlit UI**, designed to simulate a real-world **AI SaaS legal assistant**.

---

## 🚀 Features

* Multi-Agent Contract Review (Compliance, Finance, Legal, Operations)
* Clause Extraction & Risk Identification
* Parallel Agent Processing using LangGraph
* Dynamic Agent Prompt Chat (ChatGPT-style interaction)
* Vector Storage using Pinecone
* Structured Markdown Report Generation
* Downloadable Report Bundle (.md, .json, .zip)
* Clean SaaS-style Streamlit UI
* Automatic AI Configuration (No manual settings required)
* Error-handled Session State Management

---

## 🧠 Architecture
User Upload 
    ↓ 
Text Extraction (PDF/DOCX)
    ↓ 
Chunking + Embeddings 
    ↓ 
Pinecone Vector Store 
    ↓ 
Multi-Agent LLM Analysis (Parallel) 
    ↓ 
Report Builder 
    ↓ 
Streamlit UI

### Agents:

* Compliance Agent
* Finance Agent
* Legal Agent
* Operations Agent

---

## 🛠 Tech Stack

| Layer         | Technology                          |
| ------------- | ----------------------------------- |
| UI            | Streamlit                           |
| LLM           | Groq (LLaMA Models)                 |
| Orchestration | LangGraph                           |
| Vector DB     | Pinecone                            |
| Embeddings    | Sentence-Transformers / HuggingFace |
| Parsing       | PyPDF, Python-DOCX                  |
| Backend       | Python                              |
| Environment   | Python 3.10+                        |

---

## 📂 Project Structure

```
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
```

---

## ⚙️ Installation

### 1. Clone Repository

```
git clone <your-repo-url>
cd ClauseAI
```

### 2. Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_key
PINECONE_API_KEY=your_pinecone_key
LLM_PROVIDER=groq
```

---

## ▶️ Run Application

```
streamlit run app.py
```

---

## 📊 Workflow

1. Upload PDF/DOCX contract
2. Extract and preview text
3. Chunk and store embeddings in Pinecone
4. Run multi-agent AI analysis
5. Review outputs from each agent
6. Interact with agents dynamically (chat mode)
7. Generate structured report
8. Download output bundle

---

## 📦 Output Files

* `report.md` → Final structured contract analysis
* `output.json` → Raw agent responses
* `contract.txt` → Extracted contract text
* `meta.json` → Execution metadata

---

## 🧪 Milestones Completed

### ✅ Milestone 1: Data Processing & Vector Store

* Contract text extraction (PDF/DOCX)
* Text chunking strategy
* Embedding generation
* Pinecone vector database integration

---

### ✅ Milestone 2: Multi-Agent Pipeline

* Designed agent architecture
* Built specialized agents (Compliance, Finance, Legal, Operations)
* Integrated LLM with LangGraph
* Structured response generation

---

### ✅ Milestone 3: UI & Parallel Processing

* Streamlit-based SaaS UI
* Parallel agent execution
* Dynamic prompt interaction system
* Real-time analysis visualization

---

### ✅ Milestone 4: Optimization & Production Readiness

* Removed manual settings → Fully automated AI pipeline
* Fixed session state errors (`st.session_state` initialization)
* Updated deprecated libraries (LangChain → langchain-huggingface)
* Improved UI/UX for cleaner workflow
* Optimized performance and response handling
* Replaced deprecated Streamlit parameters (`use_container_width`)
* Added better error handling and stability improvements

---

## ⚠️ Notes

* Large contracts may take longer to process
* Pinecone index must be active
* Groq API rate limits may apply
* Ensure `.env` file is correctly configured

---

## 📌 Future Enhancements

* Clause Comparison Mode
* AI-based Redline Suggestions
* User Authentication & Dashboard
* Cloud Deployment (AWS/GCP)
* Multi-language Contract Support
* Real-time Collaboration

---

## 👨‍💻 Author

**Sumuth T S**

---

## 📄 License

MIT License

