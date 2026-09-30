from src.retrieval.advanced_retriever import AdvancedRetriever
from src.generation.generator import Generator
from src.tools.registry import execute_tool
from src.tools.schemas import TOOL_SCHEMAS


class AgentPipeline:
    MAX_ITERATIONS = 5

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

    def answer(self, question: str):

        # --------------------------------
        # 1. Retrieve candidate context
        # --------------------------------

        documents = self.retriever.retrieve(question)

        # --------------------------------
        # 2. Ask LLM what to do
        # --------------------------------

        observations = []
        for step in range(self.MAX_ITERATIONS):

            decision = self.generator.generate(question=question,
                                               documents=documents,
                                               tool_schemas=TOOL_SCHEMAS,
                                               observations=self._format_observations(observations))

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


                try:

                    tool_result = execute_tool(tool_name,
                                               arguments)

                    observation = {"step": step + 1,
                                   "tool": tool_name,
                                   "arguments": arguments,
                                   "result": tool_result}

                except Exception as e:

                    observation = {"step": step + 1,
                                   "tool": tool_name,
                                   "arguments": arguments,
                                   "error": str(e)}

                observations.append(observation)

                continue
                    
        # --------------------------------
        # MAX ITERATIONS
        # --------------------------------

        return ("The agent could not complete "
                "the task within the maximum "
                "number of tool calls.")

    @staticmethod
    def _format_observations(observations):

        if not observations:
            return "No previous tool calls."

        formatted = []

        for observation in observations:

            formatted.append(str(observation))

        return "\n".join(formatted)        