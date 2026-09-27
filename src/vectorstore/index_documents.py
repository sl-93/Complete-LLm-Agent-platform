from src.ingestion.loader import LoadFiles
from src.chunking.chunker import ChunkDocuments
from src.embeddings.embedder import Embedder
from src.vectorstore.chroma_store import ChromaStore

def indexing(data_path,
             embedding_model,
             db_path,
             collection_name):
    
    loader = LoadFiles(data_path)
    documents = loader.load_directory()
    chunker = ChunkDocuments(documents)
    chunks = chunker.chunk_documents()
    embedder = Embedder(embedding_model)
    texts = [chunk["text"]
            for chunk in chunks]

    embeddings = embedder.encode(texts)

    chroma_store = ChromaStore(path=db_path,
                               collection_name=collection_name)
    
    chroma_store.add_documents(chunks,
                               embeddings)