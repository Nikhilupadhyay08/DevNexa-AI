from app.services.llm import LLMService, OllamaProvider


llm_service = LLMService(
    provider=OllamaProvider()
)


def select_tool(
    question: str,
) -> str:
    if not question.strip():
        raise ValueError(
            "Question cannot be empty"
        )

    prompt = f"""
You are the tool-selection component of DevNexa AI.

Choose exactly one tool for the user's request.

Available tools:

search_code
- Use when the user wants to find, understand,
  locate, or explore code across the repository.
- Use for questions about how a feature or system works.

read_file
- Use when the user explicitly asks to see,
  inspect, or explain a specific repository file.
- Use when the user names a specific file.

find_references
- Use when the user wants to know where a
  function, class, variable, method, API, or
  symbol is defined, imported, called, or used.
- Examples:
  "Where is create_access_token used?"
  "Where is User referenced?"
  "Find references to get_current_user."
  "Where is this function called?"

Rules:
- Return ONLY one of these exact values:
  search_code
  read_file
  find_references
- Do not add explanations.
- If a specific file is requested, choose read_file.
- If the user asks where a symbol/function/class is used
  or referenced, choose find_references.
- Otherwise, choose search_code.

User Question:
{question}

Tool:
"""

    result = llm_service.generate(
        prompt
    ).strip().lower()

    if "find_references" in result:
        return "find_references"

    if "read_file" in result:
        return "read_file"

    return "search_code"