from src.agent.agent import Agent
from src.retrieval.advanced_retriever import AdvancedRetriever
from src.generation.generator import Generator


class AgentPipeline:

    def __init__(self,
                 embedding_model: str,
                 db_path: str,
                 collection_name: str,
                 llm_model: str = "gemma4:e2b",
                 query_mode = "original",
                 retrieval_mode = "dense",
                 top_k: int = 5,
                 num_queries: int = 3):

        self.retriever = AdvancedRetriever(db_path=db_path,
                                           collection_name=collection_name,
                                           embedding_model=embedding_model,
                                           llm_model=llm_model,
                                           query_mode=query_mode,
                                           retrieval_mode=retrieval_mode,
                                           top_k=top_k,
                                           num_queries=num_queries)

        self.generator = Generator(model=llm_model)

    def answer(self,
               question):

        agent = Agent(self.generator)
        documents = self.retriever.retrieve(question)

        return agent.run(question=question,
                         documents=documents)

