import ollama


class QueryRewriter:
    """
    Rewrites a user question into a retrieval-oriented query.
    """

    def __init__(self,
                 model: str = "gemma4:e2b"):
        self.model = model

    def rewrite(self, 
                query: str) -> str:

        system_prompt = """
                            You are a search query optimization system.

                            Your task is to rewrite the user's question into a concise
                            query optimized for document retrieval.

                            Rules:

                            - Preserve the original meaning.
                            - Keep important entities, numbers, identifiers and technical terms.
                            - Remove conversational filler.
                            - Do not answer the question.
                            - Return ONLY the rewritten search query.
                        """

        user_prompt = f"""
                            Original user question:

                            {query}

                            Return the optimized retrieval query.
                        """

        response = ollama.chat(model=self.model,
                               messages=[{"role": "system",
                                          "content": system_prompt,},
                                          {"role": "user",
                                           "content": user_prompt,},],)

        rewritten = response["message"]["content"].strip()

        return rewritten