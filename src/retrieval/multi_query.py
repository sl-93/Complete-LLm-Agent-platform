import ollama


class MultiQueryGenerator:
    """
    Generates multiple alternative search queries
    from a single user question.
    """

    def __init__(self,
                 model: str = "gemma4:e2b",
                 num_queries: int = 3):
        
        self.model = model
        self.num_queries = num_queries

    def generate(self, 
                 query: str) -> list[str]:

        system_prompt = f"""
                            You are a search query generation system.

                            Generate {self.num_queries} different search queries
                            that can be used to retrieve documents relevant to
                            the user's question.

                            Rules:

                            - Preserve the original meaning.
                            - Each query should approach the question from a
                            slightly different perspective.
                            - Preserve important names, numbers and identifiers.
                            - Do not answer the question.
                            - Return ONLY a numbered list.
                        """

        user_prompt = f"""
                        User question:

                        {query}

                        Generate {self.num_queries} retrieval queries.
                    """

        response = ollama.chat(model=self.model,
                               messages=[{"role": "system",
                                          "content": system_prompt},
                                          {"role": "user",
                                           "content": user_prompt}])

        content = response["message"]["content"].strip()

        queries = []

        for line in content.splitlines():

            line = line.strip()

            if not line:
                continue

            # Remove common numbering formats.
            if "." in line[:4]:
                prefix, remainder = line.split(".", 1)

                if prefix.strip().isdigit():
                    line = remainder.strip()

            elif ")" in line[:4]:
                prefix, remainder = line.split(")", 1)

                if prefix.strip().isdigit():
                    line = remainder.strip()

            if line:
                queries.append(line)

        # Remove duplicates while preserving order.
        unique_queries = []

        for q in queries:
            if q not in unique_queries:
                unique_queries.append(q)

        # Guarantee the original query exists.
        if query not in unique_queries:
            unique_queries.insert(0, query)

        return unique_queries[: self.num_queries + 1]