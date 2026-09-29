from src.embeddings.embedder import Embedder
from src.vectorstore.chroma_store import ChromaStore


class DenseRetriever:

    def __init__(self,
                 embedding_model,
                 db_path="./chroma_db",
                 collection_name="documents",
                 top_k=5):

        self.embedder = Embedder(embedding_model)
        self.vectorstore = ChromaStore(path=db_path,
                                       collection_name=collection_name)
        self.top_k = top_k

    def retrieve(self, query):

        query_embedding = self.embedder.encode([query])[0]

        results = self.vectorstore.search(query_embedding=query_embedding,
                                          top_k=self.top_k)

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        ids = results.get("ids", [[]])[0]

        retrieved = []

        for i, document in enumerate(documents):

            retrieved.append({"id": ids[i] if i < len(ids) else None,
                              "text": document,
                              "metadata": (metadatas[i]
                                           if i < len(metadatas)
                                           else {}),
                                "score": (distances[i]
                                          if i < len(distances)
                                          else None),
                                "retrieval_method": "dense",})

        return retrieved