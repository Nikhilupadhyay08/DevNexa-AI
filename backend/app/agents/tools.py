from app.services.github import get_file_content
from app.services.qdrant import search_code


def search_code_tool(
    query: str,
    limit: int = 5,
) -> list[dict]:
    if not query.strip():
        raise ValueError(
            "Search query cannot be empty"
        )

    return search_code(
        query=query,
        limit=limit,
    )


async def read_file_tool(
    owner: str,
    repository: str,
    path: str,
    branch: str,
) -> str:
    if not owner.strip():
        raise ValueError(
            "GitHub owner cannot be empty"
        )

    if not repository.strip():
        raise ValueError(
            "GitHub repository cannot be empty"
        )

    if not path.strip():
        raise ValueError(
            "File path cannot be empty"
        )

    if not branch.strip():
        raise ValueError(
            "GitHub branch cannot be empty"
        )

    return await get_file_content(
        owner=owner,
        repository=repository,
        path=path,
        branch=branch,
    )


def find_references_tool(
    symbol: str,
    limit: int = 20,
) -> list[dict]:
    if not symbol.strip():
        raise ValueError(
            "Symbol cannot be empty"
        )

    results = search_code(
        query=symbol,
        limit=limit,
    )

    references = []

    for result in results:
        content = result.get(
            "content",
            "",
        )

        if symbol in content:
            references.append(
                {
                    "path": result.get("path"),
                    "chunk_index": result.get(
                        "chunk_index"
                    ),
                    "content": content,
                    "score": result.get("score"),
                }
            )

    return references