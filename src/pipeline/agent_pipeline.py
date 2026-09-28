from src.retrieval.retriever import Retriever
from src.generation.generator import Generator


class AgentPipeline:

    def __init__(self,
                 embedding_model="nomic-embed-text",
                 llm_model="gemma4:e2b",
                 db_path="./chroma_db",
                 collection_name="documents",
                 top_k=5):

        self.retriever = Retriever(embedding_model=embedding_model,
                                   db_path=db_path,
                                   collection_name=collection_name,
                                   top_k=top_k)

        self.generator = Generator(model=llm_model)

    def answer(self,
               question):

        documents = self.retriever.retrieve(question)

        result = self.generator.generate(question=question,
                                         documents=documents)

        return result