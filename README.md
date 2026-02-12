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


