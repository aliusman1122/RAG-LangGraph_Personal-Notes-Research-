# app/embeddings.py

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from pathlib import Path
import shutil

CHROMA_DIR = "embeddings/chroma"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Global vector store
vectordb = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embedding_model
)

def get_vectorstore():
    """Return the Chroma vectorstore"""
    return vectordb

def add_documents(documents):
    vectordb.add_documents(documents)

def similarity_search(query, k=3):
    return vectordb.similarity_search_with_score(query, k=k)

def reset_vectorstore():
    """Delete all stored embeddings"""
    if Path(CHROMA_DIR).exists():
        shutil.rmtree(CHROMA_DIR)
    Path(CHROMA_DIR).mkdir(parents=True, exist_ok=True)
