from utils.docsloader import load_document as load_pdf, chunk_contract
from multi_agents.finance import finance
from utils.pinecone_client import get_pinecone_client
from google import genai
import dotenv
dotenv.load_dotenv()

docs = load_pdf("demo contracts/sample.pdf")
chunks = chunk_contract(docs)
print(f"Total Chunks:{len(chunks)}")
print(chunks[0].page_content[:300])

agent=finance()
print(agent.role)

index=get_pinecone_client()
print("connected to pinecone index:",index)

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)