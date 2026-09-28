import chromadb


class ChromaStore:

    def __init__(self,
                 path="./chroma_db",
                 collection_name="documents"):

        self.client = chromadb.PersistentClient(path=path)

        self.collection = (self.client.get_or_create_collection(name=collection_name))

    def add_documents(self,
                      chunks,
                      embeddings):

        ids = []
        documents = []
        metadatas = []

        for i, chunk in enumerate(chunks):

            ids.append(f"chunk_{i}")

            documents.append(chunk["text"])

            metadatas.append(chunk["metadata"])

        self.collection.add(ids=ids,
                            documents=documents,
                            embeddings=embeddings,
                            metadatas=metadatas)


    def search(self,
               query_embedding,
               top_k=5):

        results = self.collection.query(query_embeddings=[query_embedding],
                                        n_results=top_k,
                                        include=["documents",
                                                 "metadatas",
                                                 "distances"])

        return results