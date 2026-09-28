TOOL_SCHEMAS = [
    {
        "name": "calculator",
        "description": (
            "Perform basic arithmetic calculations "
            "such as addition, subtraction, multiplication "
            "and division."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                },
                "operation": {
                    "type": "string",
                    "enum": [
                        "add",
                        "subtract",
                        "multiply",
                        "divide"
                    ],
                    "description": "Arithmetic operation"
                }
            },
            "required": [
                "a",
                "b",
                "operation"
            ]
        }
    }
]