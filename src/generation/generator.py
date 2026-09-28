import json
import ollama
from src.generation.prompts import (SYSTEM_PROMPT,
                                build_user_prompt)


class Generator:

    def __init__(self,
                 model: str = "gemma4:e2b"):
        
        self.model = model

    def generate(self,
                 question: str,
                 documents: list,
                 tool_schemas: list):

        user_prompt = build_user_prompt(question=question,
                                        documents=documents,
                                        tool_schemas=tool_schemas)

        response = ollama.chat(model=self.model,
                               messages=[{"role": "system",
                                          "content": SYSTEM_PROMPT
                                          },
                                          {"role": "user",
                                           "content": user_prompt}],
                                options={"temperature": 0})

        content = response["message"]["content"]

        return self._parse_response(content)

    def generate_final_answer(self,
                              question: str,
                              documents: list,
                              tool_result=None):

        context_parts = []

        for document in documents:
            context_parts.append(document.get("text", ""))

        context = "\n\n".join(context_parts)

        prompt = f"""
                    Answer the user's question.

                    USER QUESTION:
                    {question}

                    RETRIEVED CONTEXT:
                    {context if context else "No relevant context."}

                    TOOL RESULT:
                    {tool_result if tool_result is not None else "No tool was used."}

                    Use the retrieved context and tool result when relevant.

                    Do not invent information.

                    Return only the final answer.
                """

        response = ollama.chat(model=self.model,
                               messages=[{"role": "system",
                                          "content": ("You are a helpful assistant. "
                                                      "Answer accurately and concisely.")},
                                        {"role": "user",
                                         "content": prompt}],
                                options={"temperature": 0})

        return response["message"]["content"]

    @staticmethod
    def _parse_response(content: str):

        try:
            return json.loads(content)

        except json.JSONDecodeError:

            return {"type": "final_answer",
                    "strategy": "direct",
                    "answer": content}