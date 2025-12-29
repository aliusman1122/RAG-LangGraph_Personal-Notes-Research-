# 📘 LangGraph RAG – Personal Notes Search

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-purple)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-orange)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black)
![RAG](https://img.shields.io/badge/RAG-Hallucination--Free-success)
### LangGraph-powered RAG + Summary System

A **Retrieval-Augmented Generation (RAG)** application built using **LangGraph**, **FastAPI**, **Streamlit**, **ChromaDB**, and **Ollama** that allows users to:

* Upload personal documents (PDF, TXT, MD)
* Ask factual questions strictly from uploaded notes
* Generate **controlled summaries** from documents
* Prevent hallucinations by enforcing **context-only answers**

---

## 🚀 Key Features

✅ Document-based Question Answering (RAG)
✅ Context-only Summarization
✅ Hallucination-free responses
✅ Local LLM support via **Ollama**
✅ Modular LangGraph workflow
✅ Simple Streamlit UI
✅ FastAPI backend

---

## 🧠 System Architecture

```
User (Streamlit UI)
        |
        v
FastAPI Backend
        |
        v
LangGraph Workflow
   ├── Retrieve Node (ChromaDB)
   └── Generate Node (Ollama LLM)
```

---

## 🧩 Tech Stack

| Component     | Technology        |
| ------------- | ----------------- |
| UI            | Streamlit         |
| Backend       | FastAPI           |
| Orchestration | LangGraph         |
| Vector Store  | ChromaDB          |
| Embeddings    | HuggingFace       |
| LLM           | Ollama (llama3.x) |
| Language      | Python            |

---

## 📂 Project Structure

```
LangGraph_personal_report_search/
│
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── graph.py             # LangGraph workflow
│   ├── embeddings.py        # ChromaDB logic
│   ├── loaders.py           # PDF/TXT/MD loaders
│   └── state.py             # GraphState definition
│
├── streamlit_app.py         # Frontend UI
├── data/uploads/            # Uploaded documents
├── embeddings/chroma/       # Vector database
├── requirements.txt
└── README.md
```

---

## 🔁 LangGraph Workflow

### 🔹 Retrieve Node

* Searches ChromaDB using semantic similarity
* Retrieves top-k relevant document chunks

### 🔹 Generate Node

* Uses retrieved context only
* Handles both:

  * **Questions**
  * **Summaries**
* Enforces strict rules:

  * ❌ No outside knowledge
  * ❌ No assumptions
  * ❌ No hallucinations

---

## 📜 Prompt Rules (Safety-First)

* Answer **only using retrieved context**
* If partial info exists → summarize only that
* If info is missing → respond exactly:

```
No relevant information found in the uploaded notes.
```

---

## 🧪 Example Queries

### Question

```
Who is Prophet Muhammad SAW?
```

### Summary

```
Give a summary of this PDF
```

### Invalid / Out-of-context

```
What is Bitcoin?
```

➡️ Response:

```
No relevant information found in the uploaded notes.
```

---

## ⚙️ Setup Instructions

### 1️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Install Ollama & Pull Model

```bash
ollama pull llama3.2:3b
```

### 4️⃣ Run Backend

```bash
uvicorn app.main:app --reload
```

### 5️⃣ Run Frontend

```bash
streamlit run streamlit_app.py
```

---

## 🎯 Use Cases

* Personal knowledge base
* Research document search
* Academic notes analysis
* Internal company documentation
* Hallucination-safe AI assistants

---

## 🏆 Why This Project Matters

Most AI apps **hallucinate**.
This project enforces **document-grounded intelligence** using LangGraph — making it **safe, reliable, and production-ready**.

---

## 📌 Future Improvements

* Multi-document summarization
* Query intent classification
* Chunk relevance filtering
* Chat history memory
* Deployment (Docker / Cloud)

---

## 👨‍💻 Author

**Mohammad Usman**

