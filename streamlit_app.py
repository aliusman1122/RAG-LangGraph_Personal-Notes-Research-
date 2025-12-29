import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="📘 Personal Notes Search",
    layout="wide"
)

st.title("📘 Personal Notes Search App (LangGraph RAG)")

# ---------------- Sidebar: Upload & Reset ----------------
with st.sidebar:
    st.header("📂 Upload Notes")
    files = st.file_uploader(
        "Upload PDF / TXT / MD",
        accept_multiple_files=True
    )

    if st.button("Upload"):
        if files:
            try:
                response = requests.post(
                    f"{API_URL}/upload",
                    files=[("files", (f.name, f, f.type)) for f in files]
                )
                response.raise_for_status()
                data = response.json()
                st.success(data.get("message", "Files uploaded successfully!"))
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")
            except ValueError:
                st.error(f"Invalid response from server: {response.text}")

    if st.button("🗑️ Delete All Notes"):
        try:
            response = requests.post(f"{API_URL}/reset")
            response.raise_for_status()
            data = response.json()
            st.warning(data.get("message", "All notes deleted"))
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
        except ValueError:
            st.error(f"Invalid response from server: {response.text}")

st.divider()

# ---------------- Chat ----------------
if "chat" not in st.session_state:
    st.session_state.chat = []

question = st.text_input("Ask a question from your notes:")

if st.button("Ask"):
    if question:
        try:
            res = requests.post(
                f"{API_URL}/query",
                params={"question": question}
            )
            res.raise_for_status()
            data = res.json()
            st.session_state.chat.append(data)
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
        except ValueError:
            st.error(f"Invalid response from server: {res.text}")

# Display chat history
for chat in st.session_state.chat[::-1]:
    st.subheader("🧠 Answer")
    st.write(chat.get("answer", "No answer"))

    st.subheader("📌 Sources")
    for s in chat.get("sources", []):
        st.code(s.get("content", ""))
        st.caption(f"Similarity Score: {s.get('score', 0)}")
