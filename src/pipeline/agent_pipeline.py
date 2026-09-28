from src.retrieval.retriever import Retriever
from src.generation.generator import Generator
from src.tools.registry import execute_tool
from src.tools.schemas import TOOL_SCHEMAS


class AgentPipeline:

    def __init__(self,
                 embedding_model: str,
                 db_path: str,
                 collection_name: str,
                 llm_model: str = "gemma4:e2b",
                 top_k: int = 5):

        self.retriever = Retriever(embedding_model=embedding_model,
                                   db_path=db_path,
                                   collection_name=collection_name,
                                   top_k=top_k)

        self.generator = Generator(model=llm_model)

    def answer(self, question: str):

        # --------------------------------
        # 1. Retrieve candidate context
        # --------------------------------

        documents = self.retriever.retrieve(question)

        # --------------------------------
        # 2. Ask LLM what to do
        # --------------------------------

        decision = self.generator.generate(question=question,
                                           documents=documents,
                                           tool_schemas=TOOL_SCHEMAS)

        # --------------------------------
        # 3. Direct / RAG answer
        # --------------------------------

        if decision["type"] == "final_answer":

            return {"answer": decision["answer"],
                    "strategy": decision.get("strategy",
                                             "direct"),
                    "tool_used": False}

        # --------------------------------
        # 4. Tool call
        # --------------------------------

        if decision["type"] == "tool_call":

            tool_name = decision["tool_name"]
            arguments = decision["arguments"]

            tool_result = execute_tool(tool_name,
                                       arguments)

            # --------------------------------
            # 5. Give tool result back to LLM
            # --------------------------------

            final_answer = (self.generator.generate_final_answer(question=question,
                                                                 documents=documents,
                                                                 tool_result=tool_result))

            return {"answer": final_answer,
                    "strategy": decision.get("strategy",
                                             "tool"),
                    "tool_used": True,
                    "tool_name": tool_name,
                    "tool_result": tool_result}

        raise ValueError(f"Unknown decision type: "
                         f"{decision.get('type')}")