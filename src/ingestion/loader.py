import os
import pathlib
import re
from typing import Any

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# Directory containing input .txt files (set in .env)
ingestion_path = os.getenv("INPUT_DOCS_DIR")


def normalize_text(text: str) -> str:
    """Normalize plain text for RAG without changing its structure."""
    if text is None:
        return ""

    # Normalize line endings and remove BOM
    s = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")

    # Replace tabs with spaces
    s = s.replace("\t", " ")

    # Remove trailing spaces on each line
    s = "\n".join(line.rstrip() for line in s.split("\n"))

    # Remove common indentation (4+ spaces) at the start of lines
    s = re.sub(r"(?m)^[ ]{4,}", "", s)

    # Collapse excessive blank lines (3+ -> 2)
    s = re.sub(r"\n{3,}", "\n\n", s)

    return s.strip()


def load_documents(path: str | None = None) -> list[dict[str, Any]]:
    """
    Read all .txt files from a directory and return structured docs with:
    - id: filename without extension
    - source: filename (with extension)
    - text: normalized content
    """
    path = path or ingestion_path
    if not path:
        raise ValueError("INPUT_DOCS_DIR is empty or not set. Check your .env")

    docs_dir = pathlib.Path(path)
    if not docs_dir.exists() or not docs_dir.is_dir():
        raise ValueError(f"INPUT_DOCS_DIR does not exist or is not a directory: {docs_dir}")

    content: list[dict[str, Any]] = []
    for doc_path in docs_dir.glob("*.txt"):
        raw = doc_path.read_text(encoding="utf-8").strip()
        if not raw:
            print(f"Warning: The document {doc_path} is empty and will be skipped.")
            continue

        normalized = normalize_text(raw)
        content.append(
            {
                "id": doc_path.stem,
                "source": doc_path.name,  # use name for cleaner citations
                "text": normalized,
            }
        )

    return content


def chunk_text(
    text: str,
    *,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[str]:
    """Split a text string into chunks using LangChain's RecursiveCharacterTextSplitter."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    # For strings, use split_text (split_documents is for Document inputs)
    return splitter.split_text(text)


def to_langchain_documents(
    chunks: list[str],
    *,
    doc_id: str,
    source: str,
) -> list[Document]:
    """Convert chunks into LangChain Documents with metadata."""
    docs: list[Document] = []
    for i, chunk in enumerate(chunks):
        docs.append(
            Document(
                page_content=chunk,
                metadata={"id": doc_id, "source": source, "chunk_index": i},
            )
        )
    return docs


def build_langchain_documents(
    path: str | None = None,
    *,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[Document]:
    """
    Full ingestion pipeline for the RAG base:
    - load .txt files
    - normalize
    - chunk
    - return LangChain Documents with metadata
    """
    raw_docs = load_documents(path)
    all_docs: list[Document] = []

    for item in raw_docs:
        chunks = chunk_text(
            item["text"],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        all_docs.extend(
            to_langchain_documents(
                chunks,
                doc_id=item["id"],
                source=item["source"],
            )
        )

    return all_docs
