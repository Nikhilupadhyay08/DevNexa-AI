from app.services.llm import LLMService, OllamaProvider
from app.services.qdrant import build_code_context


llm_service = LLMService(
    provider=OllamaProvider()
)


def answer_code_question(
    question: str,
    limit: int = 5,
) -> str:
    if not question.strip():
        raise ValueError(
            "Question cannot be empty"
        )

    context = build_code_context(
        query=question,
        limit=limit,
    )

    prompt = f"""
You are DevNexa AI, an AI software engineering assistant.

Answer the user's question using the provided repository
context.

Rules:
- Use the repository context as your primary source.
- Do not invent files, functions, or implementation details.
- If the context is insufficient, clearly say that the
  available code context is insufficient.
- Explain technical concepts clearly.
- Mention relevant file paths when useful.

Repository Context:
{context}

User Question:
{question}

Answer:
"""

    return llm_service.generate(prompt)