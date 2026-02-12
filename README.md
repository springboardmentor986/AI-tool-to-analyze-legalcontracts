# Contract Upload & Basic Parser

Run a simple Streamlit app to upload contracts and extract text and basic clauses.

Requirements
- Install from the existing `requirements.txt` (contains `streamlit`, `PyPDF2`, `python-docx`).

Quick start
```bash
pip install -r requirements.txt
streamlit run app.py
```

Files added
- [parser.py](parser.py) — extraction and clause heuristics
- [app.py](app.py) — Streamlit upload UI

LangChain features
- The app can summarize the uploaded contract and answer simple questions using LangChain + OpenAI.
- Set your OpenAI API key in the environment before using these features:

```bash
set OPENAI_API_KEY="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"   # Windows (cmd)
# or
$env:OPENAI_API_KEY = "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"  # PowerShell
```

Then click "Summarize contract" or enter a question in the app UI.

Notes
- This provides basic, heuristic clause detection only. For production/legal workflows use a dedicated NLP or contract analysis tool.

