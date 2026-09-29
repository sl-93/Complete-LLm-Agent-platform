from typing import Any
from src.embeddings.embedder import Embedder
from src.vectorstore.chroma_store import ChromaStore
from src.retrieval.retriever import DenseRetriever
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.hybrid_retriever import HybridRetriever
from src.retrieval.query_rewriter import QueryRewriter
from src.retrieval.multi_query import MultiQueryGenerator


class AdvancedRetriever:
    """
    Configurable Advanced RAG retrieval pipeline.

    Query modes:
        - original
        - rewrite
        - multi_query

    Retrieval modes:
        - dense
        - bm25
        - hybrid

    Optional reranking:
        - True
        - False
    """

    def __init__(self,
                 db_path="./chroma_db",
                 collection_name="documents",
                 embedding_model: str = "nomic-embed-text",
                 llm_model: str = "gemma4:e2b",
                 query_mode: str = "original",
                 retrieval_mode: str = "dense",
                 top_k: int = 5,
                 num_queries: int = 3):

        self.query_mode = query_mode
        self.retrieval_mode = retrieval_mode
        self.top_k = top_k

        # -----------------------------
        # Base retrievers
        # -----------------------------

        self.embedder = Embedder(embedding_model)
        self.vectorstore = ChromaStore(path=db_path,
                                       collection_name=collection_name)

        self.dense_retriever = DenseRetriever(embedding_model=embedding_model,
                                              db_path=db_path,
                                              collection_name=collection_name,
                                              top_k=top_k)

        self.bm25_retriever = BM25Retriever(db_path=db_path,
                                            collection_name=collection_name)

        self.hybrid_retriever = HybridRetriever(dense_retriever=self.dense_retriever,
                                                bm25_retriever=self.bm25_retriever)

        # -----------------------------
        # Query transformation
        # -----------------------------

        self.query_rewriter = QueryRewriter(model=llm_model)

        self.multi_query_generator = MultiQueryGenerator(model=llm_model,
                                                         num_queries=num_queries)

        # -----------------------------
        # Reranker
        # -----------------------------

        # self.reranker = None

        # if rerank:

        #     self.reranker = Reranker(model_name=reranker_model)

    def _transform_query(self,
                         query: str) -> list[str]:

        if self.query_mode == "original":

            return [query]

        if self.query_mode == "rewrite":

            rewritten = self.query_rewriter.rewrite(query)

            return [rewritten]

        if self.query_mode == "multi_query":

            return self.multi_query_generator.generate(query)

        raise ValueError(f"Unsupported query mode: "
                         f"{self.query_mode}")

    def _retrieve_single(self,
                         query: str) -> list[dict[str, Any]]:

        if self.retrieval_mode == "dense":

            return self.dense_retriever.retrieve(query=query)

        if self.retrieval_mode == "bm25":

            return self.bm25_retriever.retrieve(query=query,
                                                top_k=self.top_k)

        if self.retrieval_mode == "hybrid":

            return self.hybrid_retriever.retrieve(query=query,
                                                  top_k=self.top_k)

        raise ValueError(f"Unsupported retrieval mode: "
                         f"{self.retrieval_mode}")

    def _merge_results(self,
                       result_lists: list[list[dict[str, Any]]]) -> list[dict[str, Any]]:

        """
        Merge results from multiple queries.

        We use RRF here too, so multi-query retrieval
        can benefit from documents appearing across
        multiple query results.
        """

        return self.hybrid_retriever.reciprocal_rank_fusion(result_lists)

    def retrieve(self,
                 query: str) -> dict[str, Any]:

        # ----------------------------------
        # 1. Query transformation
        # ----------------------------------

        transformed_queries = self._transform_query(query)

        # ----------------------------------
        # 2. Retrieval
        # ----------------------------------

        result_lists = []

        for transformed_query in transformed_queries:

            results = self._retrieve_single(transformed_query)

            result_lists.append(results)

        # ----------------------------------
        # 3. Merge multi-query results
        # ----------------------------------

        if len(result_lists) == 1:

            documents = result_lists[0]

        else:

            documents = self._merge_results(result_lists)


        documents = documents[:self.top_k]

        return {"query": query,
                "transformed_queries": transformed_queries,
                "documents": documents,
                "query_mode": self.query_mode,
                "retrieval_mode": self.retrieval_mode}