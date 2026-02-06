from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

def build_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return FAISS.from_texts(chunks, embeddings)
