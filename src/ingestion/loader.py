import os
import pathlib
import re

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()
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



def load_documents(path):
    """read all text files from a directory and return their content as a list of strings."""
    documents = pathlib.Path(path).glob("*.txt")
    content = []
    for doc in documents:
        text = doc.read_text(encoding="utf-8").strip()
        if (not text):
            print(f"Warning: The document {doc} is empty and will be skipped.") 
        else:
            normalized_text = normalize_text(text)
            metadata_document = {"id": str(doc.stem),
                                 "source" : str(doc),
                                 "text" : normalized_text}
            content.append(metadata_document)
    return content


print(load_documents(ingestion_path))