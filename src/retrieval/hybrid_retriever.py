from typing import Any


class HybridRetriever:
    """
    Combines dense and BM25 retrieval using
    Reciprocal Rank Fusion (RRF).
    """

    def __init__(self,
                 dense_retriever,
                 bm25_retriever,
                 rrf_k: int = 60):
        
        self.dense_retriever = dense_retriever
        self.bm25_retriever = bm25_retriever
        self.rrf_k = rrf_k

    def retrieve(self,
                 query: str,
                 top_k: int = 10) -> list[dict[str, Any]]:

        dense_results = self.dense_retriever.retrieve(query=query)

        bm25_results = self.bm25_retriever.retrieve(query=query,
                                                    top_k=top_k)

        fused = self.reciprocal_rank_fusion([dense_results,
                                             bm25_results])

        return fused[:top_k]

    def reciprocal_rank_fusion(self,
                               result_lists: list[list[dict[str, Any]]]) -> list[dict[str, Any]]:

        scores = {}
        documents = {}

        for results in result_lists:

            for rank, result in enumerate(results,
                                          start=1):

                document_id = result["id"]

                if document_id is None:
                    continue

                rrf_score = 1 / (self.rrf_k + rank)

                scores[document_id] = (scores.get(document_id, 0)
                                       + rrf_score)

                # Keep the first copy of the document.
                if document_id not in documents:
                    documents[document_id] = result.copy()

        ranked_ids = sorted(scores,
                            key=scores.get,
                            reverse=True)

        results = []

        for rank, document_id in enumerate(ranked_ids,
                                           start=1):

            result = documents[document_id].copy()

            result["rrf_score"] = scores[document_id]
            result["rank"] = rank
            result["retrieval_method"] = "hybrid"

            results.append(result)

        return results