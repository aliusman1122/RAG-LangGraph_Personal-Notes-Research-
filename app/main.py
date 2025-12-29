from fastapi import FastAPI, UploadFile, File
from pathlib import Path
import shutil

from app.loaders import load_document
from app.embeddings import add_documents, reset_vectorstore
from app.graph import build_graph
from app.state import GraphState

app = FastAPI(title="Personal Notes Search App")

# ---------------- Upload directory ----------------
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ---------------- Graph ----------------
graph = build_graph()

# ---------------- Upload Endpoint ----------------
@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    try:
        all_docs = []

        for file in files:
            file_path = UPLOAD_DIR / file.filename
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            docs = load_document(file_path)
            all_docs.extend(docs)

        add_documents(all_docs)
        return {"message": "Files uploaded and indexed successfully"}

    except Exception as e:
        return {"error": str(e)}

# ---------------- Query Endpoint (✅ FIXED) ----------------
@app.post("/query")
async def query(question: str):
    try:
        state = GraphState(question=question)

        # 🔑 LangGraph returns DICT, not object
        result = graph.invoke(state)

        return {
            "answer": result.get("answer", "No relevant information found."),
            "sources": result.get("retrieved_docs", []),
            "chat_history": result.get("chat_history", [])
        }

    except Exception as e:
        return {"error": str(e)}

# ---------------- Reset Endpoint ----------------
@app.post("/reset")
async def reset():
    try:
        reset_vectorstore()
        shutil.rmtree(UPLOAD_DIR, ignore_errors=True)
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        return {"message": "All notes deleted"}

    except Exception as e:
        return {"error": str(e)}
