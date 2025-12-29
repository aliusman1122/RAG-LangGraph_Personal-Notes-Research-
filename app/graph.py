from langgraph.graph import StateGraph
from app.state import GraphState
from app.embeddings import get_vectorstore
import ollama
import os

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

# ---------------------------
# Retriever Node
# ---------------------------
def retrieve(state: GraphState):
    vectordb = get_vectorstore()

    results = vectordb.similarity_search_with_score(
        state.question, k=3
    )

    # ✅ similarity threshold (IMPORTANT)
    filtered_docs = []
    for doc, score in results:
        if score < 1.4:   # lower = more relevant
            filtered_docs.append({
                "content": doc.page_content,
                "score": float(score)
            })

    state.retrieved_docs = filtered_docs
    return state


# ---------------------------
# Generator Node
# ---------------------------
def generate(state: GraphState):

    # ✅ STRICT RAG SAFETY
    if not state.retrieved_docs:
        state.answer = "No relevant information found in the uploaded notes."
        return state

    context = "\n\n".join(
        d["content"] for d in state.retrieved_docs
    )

    prompt = f"""
You must answer ONLY using the provided context in a precise and friendly tone.

Task rules:
- If the user asks a QUESTION, answer it strictly from the context.
- If the user asks for a SUMMARY or OVERVIEW, summarize ONLY what is explicitly written in the context.
- Do NOT add missing details.
- Do NOT use outside knowledge.
- Do NOT explain anything extra.

Hard rule:
- If the answer OR summary is NOT clearly present in the context, reply EXACTLY:
"No relevant information found in the uploaded notes."


Context:
{context}

Question:
{state.question}
"""

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    state.answer = response["message"]["content"]
    return state


# ---------------------------
# Build LangGraph
# ---------------------------
def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.set_finish_point("generate")

    return graph.compile()
