import os
from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
def load_document(path):
    ext=os.path.splitext(path)[1].lower()
    if ext==".pdf":
        loader=PyPDFLoader(path)
    elif ext==".docx":
        loader=Docx2txtLoader(path)
    elif ext==".txt":   
        loader=TextLoader(path,encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file format: {ext}")
    return loader.load()

def chunk_contract(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)
    return chunks
