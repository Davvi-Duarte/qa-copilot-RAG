import os
import pathlib

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

ingestion_path = os.getenv("INPUT_DOCS_DIR")

def load_documents(path):
    """read all text files from a directory and return their content as a list of strings."""
    documents = pathlib.Path(path).glob("*.txt")
    content = []
    for doc in documents:
        text = doc.read_text(encoding="utf-8").strip()
        if (not text):
            print(f"Warning: The document {doc} is empty and will be skipped.") 
        else:
            content.append(text)
    return content