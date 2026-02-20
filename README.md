<div align="center">
  <img src="assets/logo.png" alt="ClauseAI Logo" width="200" height="200" />
  <h1>ClauseAI Ultimate ⚖️</h1>
  <p><b>An AI-Powered System to Read, Analyze, and Risk-Score Legal Contracts Automatically.</b></p>
  <i>Built with LangGraph, Gemini 1.5 Pro, and Pinecone Vector Stores</i>
</div>

<br/>

## 📖 Overview
**ClauseAI** is an intelligent, multi-agent AI system designed to democratize legal access and streamline contract analysis. By leveraging Large Language Models (LLMs) and LangGraph-powered Multi-Agent orchestration, the platform automates the extraction, risk assessment, and summarization of complex legal documents across multiple domains (Finance, Legal, Compliance, Operations).

The platform transforms raw legal text into highly accessible, professionally formatted Executive Summaries, significantly reducing manual review times.

---

## ⚡ Core Innovations & Features
- **Parallel Asynchronous Execution**: Custom AsyncRunner implementation allowing multiple AI agents to process document clauses simultaneously, cutting Wait/Response times by 75% while securely handling Gemini API rate limits.
- **Dynamic Machine Vision (OCR)**: Integrated hybrid extraction pipelines that automatically detect scanned, non-selectable PDF images and trigger internal Optical Character Recognition (Tesseract) seamlessly.
- **Priority LLM Queues**: Automated failover architecture routing from DeepSeek R1 reasoning models to Gemini 1.5 Flash to ensure 100% uptime and cost resilience.
- **Multi-Language Robustness**: Natively exports Executive Summaries into perfectly formatted Gujarati, Hindi, Spanish, and French Localized Web Reports.
- **Interactive Risk Dashboards**: Embedded Plotly-powered Radar and Bar charts to visually interpret document risk profiles instantly.

---

## 🏗️ System Architecture
ClauseAI utilizes a modular, fast-responding architecture to ensure infinite scalability:

1. **Ingestion Layer:** User uploads documents (PDF/DOCX). If scanned, Tesseract OCR maps text back to page coordinates.
2. **Vector Storage:** Text is semantically chunked and embedded into **Pinecone** via LangChain.
3. **Processing Layer (LangGraph):** The App initializes the state, the Coordinator assigns tasks in parallel, and Domain Agents (Legal, Finance, Compliance, Operations) process their specific constraints targeting Liabilities and Delivery.
4. **Output Synthesis Layer:** Findings are synthesized into an Executive Summary and displayed via the striking `Cyber-Emerald` user interface.
5. **Export Engine:** One-click exports to beautifully formatted PDF, HTML Web Reports, and Word (.docx) formats natively featuring `Segoe UI` fonts and Emerald aesthetics.

---

## 💻 Installation & Setup

### 1. Prerequisites
- **Python 3.9+**
- **Tesseract OCR & Poppler**: (Required for scanned PDF image extraction)
  - Windows: [Tesseract Installer](https://github.com/UB-Mannheim/tesseract/wiki) | [Poppler Binary](https://github.com/oschwartz10612/poppler-windows/releases/)
  - Linux: `sudo apt-get install tesseract-ocr poppler-utils`
  - macOS: `brew install tesseract poppler`

### 2. Environment Variables
Create a `.env` file in the root directory:
```env
# API Keys (Required)
GEMINI_API_KEY=your_gemini_key_here
PINECONE_API_KEY=your_pinecone_key_here

# Pinecone Configuration
PINECONE_INDEX_NAME=clauseai-contracts
PINECONE_ENV=us-east-1

# Optional Fallback
OPENROUTER_API_KEY=your_openrouter_key
```

### 3. Quick Start
```bash
git clone https://github.com/yourusername/clauseAI.git
cd clauseAI
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

## 🛠️ Tech Stack & Attribution
This project is built using the following open-source technologies. We gratefully acknowledge their authors and contributors.

| Library | License | URL |
| :--- | :--- | :--- |
| **Streamlit** | Apache 2.0 | [streamlit.io](https://streamlit.io) |
| **Streamlit Extras** | MIT | [github.com/arnaudmiribel/streamlit-extras](https://github.com/arnaudmiribel/streamlit-extras) |
| **LangChain & LangGraph** | MIT | [github.com/langchain-ai](https://github.com/langchain-ai) |
| **Google Generative AI** | Apache 2.0 | [github.com/google/generative-ai-python](https://github.com/google/generative-ai-python) |
| **Pinecone Client** | Apache 2.0 | [github.com/pinecone-io/pinecone-python-client](https://github.com/pinecone-io/pinecone-python-client) |
| **Deep-Translator** | MIT | [github.com/nidhaloff/deep-translator](https://github.com/nidhaloff/deep-translator) |
| **Python-docx** | MIT | [github.com/python-openxml/python-docx](https://github.com/python-openxml/python-docx) |
| **Plotly Express** | MIT | [plotly.com](https://plotly.com/) |

---

## 👨‍💻 Developer
**Author:** Krish Pandya
**Program:** Infosys Springboard Internship 
**Version:** Build v1.0

## ⚖️ License
This project is licensed under the terms of the MIT License. See `LICENSE` for details.

## ⚠️ Disclaimer
This tool is for educational and assistive purposes only. It does not constitute professional legal advice. Always verify findings with a qualified attorney.
