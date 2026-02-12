from fastapi import FastAPI, UploadFile
from ingestion.parser import parse_file
from ingestion.chunker import chunk_text
from planner.domain_classifier import classify_domains
from planner.planner import create_plan
from lang_graph.agent_graph import build_graph

app = FastAPI()
graph = build_graph()

@app.post("/analyze")
async def analyze(file: UploadFile):
    text = await parse_file(file)
    chunks = chunk_text(text)
    domains = classify_domains(text)
    plan = create_plan(domains)

    result = graph.invoke({
        "text": chunks[0],
        "domains": plan,
        "results": {}
    })

    return result["results"]
