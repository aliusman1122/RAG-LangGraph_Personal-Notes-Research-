from pathlib import Path
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    UnstructuredMarkdownLoader,
)

def load_document(file_path: Path):
    if file_path.suffix == ".pdf":
        loader = PyPDFLoader(str(file_path))
    elif file_path.suffix in [".txt"]:
        loader = TextLoader(str(file_path), encoding="utf-8")
    elif file_path.suffix in [".md"]:
        loader = UnstructuredMarkdownLoader(str(file_path))
    else:
        raise ValueError("Unsupported file type")

    return loader.load()
