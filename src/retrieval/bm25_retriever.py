from typing import Any
from rank_bm25 import BM25Okapi
from src.vectorstore.chroma_store import ChromaStore


class BM25Retriever:
    """
    BM25 lexical retriever.

    The corpus is loaded from the existing Chroma collection.
    """

    def __init__(self, 
                 db_path="./chroma_db",
                 collection_name="documents",):

        self.vectorstore = ChromaStore(path=db_path,
                                       collection_name=collection_name)

        self.documents: list[dict[str, Any]] = []
        self.bm25 = None

        self._build_index()

    def _build_index(self):

        results = self.vectorstore.collection.get(include=["documents",
                                                           "metadatas"])

        documents = results.get("documents", [])
        metadatas = results.get("metadatas", [])
        ids = results.get("ids", [])

        self.documents = []
        tokenized_corpus = []

        for i, document in enumerate(documents):

            document_id = (ids[i]
                           if i < len(ids)
                           else str(i))

            metadata = (metadatas[i]
                        if i < len(metadatas)
                        else {})

            item = {"id": document_id,
                    "text": document,
                    "metadata": metadata,
                    "retrieval_method": "bm25"}

            self.documents.append(item)

            tokenized_corpus.append(self._tokenize(document))

        if tokenized_corpus:
            self.bm25 = BM25Okapi(tokenized_corpus)

    @staticmethod
    def _tokenize(text: str) -> list[str]:

        return text.lower().split()

    def retrieve(self,
                 query: str,
                 top_k: int = 10) -> list[dict[str, Any]]:

        if self.bm25 is None:
            return []

        query_tokens = self._tokenize(query)

        scores = self.bm25.get_scores(query_tokens)

        ranked_indices = sorted(range(len(scores)),
                                key=lambda i: scores[i],
                                reverse=True)

        results = []

        for index in ranked_indices[:top_k]:

            document = self.documents[index].copy()

            document["score"] = float(scores[index])

            results.append(document)

        return results