from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
import docx
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from google import genai
from pinecone import Pinecone
load_dotenv()

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# -------- Read DOCX ----------
def read_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])


def chunk_data(text):
    chunk_size=800
    chunk_overlap=50
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    return splitter.split_text(text)

file_path = 'SampleContract-Shuttle.pdf'
text = read_pdf(file_path)
chunks = chunk_data(text)

x = genai.Client()
response=x.models.generate_content(model="gemini-2.5-flash",contents=chunks)
print(len(response.text))


