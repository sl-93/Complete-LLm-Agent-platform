from src.vectorstore.index_documents import indexing
from pathlib import Path


db_exists = Path("./chroma_db").exists()

if not db_exists:

    indexing("data",
             "nomic-embed-text",
             "chroma_db",
             "documents")