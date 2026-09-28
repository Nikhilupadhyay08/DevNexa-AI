import re

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

    symbol = symbol.strip()

    results = search_code(
        query=symbol,
        limit=limit,
    )

    references = []

    symbol_pattern = re.compile(
        rf"\b{re.escape(symbol)}\b"
    )

    for result in results:
        content = result.get(
            "content",
            "",
        )

        if not content:
            continue

        matches = list(
            symbol_pattern.finditer(content)
        )

        if not matches:
            continue

        reference_types = set()

        for match in matches:
            start = max(
                0,
                match.start() - 100,
            )
            end = min(
                len(content),
                match.end() + 100,
            )

            surrounding_text = content[
                start:end
            ]

            if re.search(
                rf"\bdef\s+{re.escape(symbol)}\s*\(",
                surrounding_text,
            ):
                reference_types.add(
                    "definition"
                )

            elif re.search(
                rf"\bclass\s+{re.escape(symbol)}\b",
                surrounding_text,
            ):
                reference_types.add(
                    "definition"
                )

            elif re.search(
                rf"\b(?:from|import)\s+.*\b{re.escape(symbol)}\b",
                surrounding_text,
            ):
                reference_types.add(
                    "import"
                )

            elif re.search(
                rf"\b{re.escape(symbol)}\s*\(",
                surrounding_text,
            ):
                reference_types.add(
                    "call"
                )

            else:
                reference_types.add(
                    "reference"
                )

        references.append(
            {
                "path": result.get("path"),
                "chunk_index": result.get(
                    "chunk_index"
                ),
                "content": content,
                "score": result.get("score"),
                "reference_types": sorted(
                    reference_types
                ),
                "occurrence_count": len(matches),
            }
        )

    return references