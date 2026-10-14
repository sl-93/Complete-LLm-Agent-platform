import json
import ollama
from src.generation.prompts import (SYSTEM_PROMPT,
                                    build_user_prompt,
                                    PLAN_SYSTEM_PROMPT,
                                    build_plan_prompt)


class Generator:

    def __init__(self,
                 model: str = "gemma4:e2b"):
        
        self.model = model

    def generate(self,
                 question: str,
                 documents: list,
                 tool_schemas: list,
                 observations=None,
                 conversation_history=None,
                 long_term_memories=None):

        user_prompt = build_user_prompt(question=question,
                                        documents=documents,
                                        tool_schemas=tool_schemas,
                                        observations=observations,
                                        conversation_history=conversation_history,
                                        long_term_memories=long_term_memories)

        response = ollama.chat(model=self.model,
                               messages=[{"role": "system",
                                          "content": SYSTEM_PROMPT
                                          },
                                          {"role": "user",
                                           "content": user_prompt}],
                                options={"temperature": 0})

        content = response["message"]["content"]

        self.conversation_history = conversation_history
        self.long_term_memories = long_term_memories

        return self._parse_response(content)


    @staticmethod
    def _parse_response(content: str):

        try:
            return json.loads(content)

        except json.JSONDecodeError:

            return {"type": "final_answer",
                    "strategy": "direct",
                    "answer": content}

    def generate_plan(self,
                      question):

        user_prompt = build_plan_prompt(question)

        response = ollama.chat(model=self.model,
                               messages=[{"role": "system",
                                          "content":PLAN_SYSTEM_PROMPT},
                                          {"role": "user",
                                           "content": user_prompt}],
                                           format = "json",
                                           options={"temprature": 0})

        return response["message"]["content"]