import json
import ollama

from src.generation.prompts import (SYSTEM_PROMPT,
                                    USER_PROMPT)


class Generator:

    def __init__(self,
                 model="gemma4:e2b"):
        
        self.model = model

    def build_context(self,
                      documents):

        if not documents:
            return "No relevant context was retrieved."

        context_parts = []

        for i, document in enumerate(documents,
                                     start=1):

            metadata = document.get("metadata",
                                    {})

            source = metadata.get("source",
                                  "unknown")

            page = metadata.get("page")

            if page is not None:

                source_info = (f"{source}, page {page}")

            else:

                source_info = source

            context_parts.append(f"""[DOCUMENT {i}] Source: {source_info} {document["text"]} """)

        return "\n".join(context_parts)

    def generate(self,
                 question,
                 documents,
                 tools=None):

        context = self.build_context(documents)

        if tools is None:
            tools = "No tools are currently available."

        prompt = USER_PROMPT.format(question=question,
                                    context=context,
                                    tools=tools)

        response = ollama.chat(model=self.model,
                               messages=[{"role": "system",
                                          "content": SYSTEM_PROMPT},
                                          {"role": "user",
                                           "content": prompt}],
                                options={"temperature": 0})

        content = response["message"]["content"]

        return self.parse_response(content)

    def parse_response(self,
                       content):

        try:

            result = json.loads(content)

            required_fields = ["strategy",
                               "use_context",
                               "context_sufficient",
                               "requires_tool",
                               "tool_name",
                               "answer"]

            for field in required_fields:

                if field not in result:

                    raise ValueError(f"Missing field: {field}")

            return result

        except (json.JSONDecodeError,
                ValueError):

            return {"strategy": "direct",
                    "use_context": False,
                    "context_sufficient": False,
                    "requires_tool": False,
                    "tool_name": None,
                    "answer": content}