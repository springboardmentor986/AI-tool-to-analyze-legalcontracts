# Copilot Instructions for this repo

Purpose: Quickly orient AI assistants to be productive in this codebase (contract analysis pipeline using small "agents" + vector DB + LLMs).

Key architecture (big picture) 🔧

- Ingestion → Chunking → Embeddings → Vector DB → Planning → Agent execution
  - `ingestion/parser.py` — file parsing for PDF/DOCX/TXT
  - `ingestion/chunker.py` — chunking using `RecursiveCharacterTextSplitter`
  - `embeddings/embedder.py` + `embeddings/pinecone_client.py` — create embeddings and upsert/query Pinecone
  - `planner/domain_classifier.py` → `planner/planner.py` → returns allowed domains (e.g. `legal`, `finance`, `compliance`, `operations`)
  - `agents/` — domain agents perform analysis based on LLM prompts; `agents/registry.py` maps domain → callable
  - UI / entry points:
    - Streamlit: `app/streamlit_app.py` (primary dev UI)
    - FastAPI: `app/api.py` (programmatic analyze endpoint)
  - Supervisor / orchestration: `lang_graph/agent_graph.py` uses `langgraph` StateGraph for parallel / multi-turn orchestration

Critical runtime configuration ⚙️

- Environment is read from a top-level `.env` (loaded via `dotenv` in several modules).
- Required keys used in code:
  - `GOOGLE_API_KEY` (used by `app/llm.py`) for `ChatGoogleGenerativeAI`
  - `PINECONE_API_KEY` and `PINECONE_INDEX` (used by `embeddings/pinecone_client.py`) — missing values raise RuntimeError
- Install dependencies: `pip install -r requirements.txt`

Quick dev/run commands (explicit) ▶️

- Run Streamlit UI: `streamlit run app/streamlit_app.py` (README contains an older `app.py` reference; prefer this path)
- Run FastAPI (example): `uvicorn app.api:app --reload` (install `uvicorn` if needed)
- Quick checks:
  - `python test_pinecone_key.py` — validate Pinecone connectivity & API key usage
  - `python test.py` — local ad-hoc script demonstrating chunking + model calls

Project-specific conventions & patterns ✅

- LLM wrapper usage: always call `get_llm()` from `app/llm.py`, then `llm.invoke(prompt).content` for the text result. Several components depend on that exact shape (e.g., `planner/domain_classifier.py`, `agents/*`).
- Agent contract:
  - Function signature: `def analyze_<domain>(text: str, context: Optional[str] = None) -> dict` (existing files follow this pattern).
  - Return dict typically: `{"domain": "<name>", "analysis": <string>}`
  - To add a new domain: create `agents/<name>.py`, implement the `analyze_<name>` function, add the mapping to `agents/registry.py`, and include the domain in `planner/planner.py`'s allowed set.
- Planner restrictions: `planner.create_plan` filters recognized domains against a hardcoded allowed set; update that set when adding new agents.
- Two orchestration models coexist:
  - Simple registry-based executor: `planner/executor.py` calls `AGENT_REGISTRY` functions directly (single-turn, synchronous)
  - Graph-based orchestrator: `lang_graph/agent_graph.py` uses `StateGraph` for parallel/multi-turn flows. Node handlers accept and return the `state` dict (see `GraphState` in `lang_graph/state.py`).

Important implementation notes & known inconsistencies ⚠️

- `lang_graph/agent_graph.py` currently imports `legal_analysis`, `finance_analysis` but the actual functions in `agents` modules are named `analyze_legal`, `analyze_finance`. This looks like a bug; fix by importing `analyze_legal` / `analyze_finance` (or rename functions consistently). When changing, also update tests and call sites.
- `README.md` references `streamlit run app.py` (outdated). Prefer `streamlit run app/streamlit_app.py`.

Integration & external dependencies 🔗

- LLM providers used: Google Gemini via `langchain_google_genai` (see `app/llm.py`), and local embeddings via `langchain_ollama` in `embeddings/embedder.py`.
- Vector DB: Pinecone — `pinecone` client used directly in `embeddings/pinecone_client.py`. The code expects `index.upsert` and `index.query` to return `response['matches']` with `metadata.text`.
- Local dev notes: Ollama embeddings require a running Ollama instance and appropriate model availability (`nomic-embed-text` used here).

Testing & suggested validation checks (small, concrete) 🧪

- Add a test to assert parser handles `.pdf`, `.docx`, `.txt` using small fixture files.
- Add a unit test that stubs `get_llm()` (return a simple stub object with `.invoke(prompt).content`) and validates `planner/domain_classifier.classify_domains` parsing logic.
- Add a test to stub `embeddings.get_embedding_model()` (return deterministic embeddings) and validate `embeddings/pinecone_client.retrieve_context` returns expected text slices.

When proposing changes (PR guidance) ✍️

- Keep changes minimal and focused: update one flow (e.g., fix import names in `agent_graph.py`) and add a test that fails before the fix and passes after.
- Note environment requirements in the PR description (which env keys must be set locally to run the relevant tests/routines).

If you need to make edits, check these files first:

- `app/streamlit_app.py`, `app/api.py`, `app/llm.py`
- `agents/*`, `agents/registry.py`
- `planner/*`, `planner/executor.py`, `planner/domain_classifier.py`
- `embeddings/*`, especially `embeddings/pinecone_client.py` and `embeddings/embedder.py`
- `lang_graph/agent_graph.py`, `lang_graph/state.py`

Notes for AI assistants (short checklist) 🧭

- Respect the existing LLM invocation pattern (`get_llm()` + `invoke(...).content`).
- When adding domains, update `planner.create_plan`, `agents/registry.py` and, if needed, the graph in `lang_graph/agent_graph.py`.
- Avoid changing global environment-loading behavior unless necessary; prefer explicit `.env` keys.

If anything is unclear or you'd like additional examples (e.g., a sample unit test or a proposed PR patch for `agent_graph.py`), say which item and I will prepare it.
