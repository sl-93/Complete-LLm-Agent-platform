SYSTEM_PROMPT = """
You are an intelligent AI assistant operating inside
a tool-using application.

You have access to:

1. RETRIEVED_CONTEXT
   Information retrieved from a vector database.

2. MODEL_KNOWLEDGE
   Your general language-model knowledge.

3. TOOLS
   External capabilities available to the system.

4. PREVIOUS_TOOL_RESULTS
   Results from tools already executed in the current task.

Your task is to decide what action should happen next.

SOURCE SELECTION RULES:

1. Use retrieved context when it is relevant and useful.
2. Ignore retrieved context when it is irrelevant.
3. Use model knowledge for general questions.
4. Use a tool when the question requires:
   - calculation
   - database access
   - real-time information
   - external APIs
   - executing an operation
5. If both context and a tool are useful, use both.
6. Never invent retrieved information or tool results.

MULTI-STEP TOOL CALLING:

- Multiple tool calls are allowed.
- After receiving a tool result, decide whether:
  1. another tool call is required, or
  2. the final answer can be generated.
- Use previous tool results when deciding the next tool call.
- Do not repeat a tool call unless necessary.
- Never fabricate tool results.

TOOL CALLING:

When a tool is required:

- Return a tool_call.
- Specify the exact tool name.
- Provide only the required arguments.
- Do not generate the final answer yet.
- The application will execute the tool and provide its result.

If no more tools are required, return final_answer.

RESPONSE TYPES:

FINAL ANSWER:

{
    "type": "final_answer",
    "strategy": "rag | direct",
    "use_context": true,
    "context_sufficient": true,
    "answer": "Final answer to the user."
}

TOOL CALL:

{
    "type": "tool_call",
    "strategy": "tool | rag_and_tool",
    "use_context": true,
    "context_sufficient": true,
    "requires_tool": true,
    "tool_name": "name_of_tool",
    "arguments": {}
}

IMPORTANT:

- Use only available tools.
- Never invent tool results.
- Do not expose chain-of-thought.
- Return ONLY valid JSON.
"""


def build_user_prompt(question,
                      documents,
                      tool_schemas,
                      observations=None):

    context_parts = []

    # Your AdvancedRetriever returns a wrapper dictionary.
    documents = documents.get("documents", [])

    for i, document in enumerate(documents,
                                 start=1):

        metadata = document.get("metadata",
                                {})

        text = document.get("text",
                            "")

        source = metadata.get("source",
                              "unknown")

        page = metadata.get("page")

        if page is not None:
            source_info = (f"{source}, page {page}")
        else:
            source_info = source

        context_parts.append(f"[Context {i} | {source_info}]\n"
                             f"{text}")

    context = "\n\n".join(context_parts)

    observations_text = (observations
                         if observations
                         else "No previous tool calls.")

    return f"""
                USER QUESTION:
                {question}

                RETRIEVED CONTEXT:
                {context if context else "No context retrieved."}

                PREVIOUS TOOL OBSERVATIONS:
                {observations_text}

                AVAILABLE TOOLS:
                {tool_schemas}

                Choose the next action and return ONLY valid JSON.

                If no tool is required:

                {{
                    "type": "final_answer",
                    "strategy": "rag | direct",
                    "use_context": true,
                    "context_sufficient": true,
                    "answer": "Final answer to the user."
                }}

                If a tool is required:

                {{
                    "type": "tool_call",
                    "strategy": "tool | rag_and_tool",
                    "use_context": true,
                    "context_sufficient": true,
                    "requires_tool": true,
                    "tool_name": "name_of_tool",
                    "arguments": {{}}
                }}

                Rules:

                - Use only available tools.
                - For tool_call, do not generate the final answer.
                - For final_answer, include the final answer.
                - Do not fabricate tool results.
                - Do not include reasoning or chain-of-thought.
                - Return ONLY valid JSON.
            """