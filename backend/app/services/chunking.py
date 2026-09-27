from typing import TypedDict


class Document(TypedDict):
    path: str
    content: str
    size: int
    sha: str


class Chunk(TypedDict):
    path: str
    content: str
    chunk_index: int
    size: int
    sha: str


CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


def chunk_document(document: Document) -> list[Chunk]:
    content = document["content"]

    if not content.strip():
        return []

    chunks = []

    start = 0
    chunk_index = 0

    while start < len(content):
        end = start + CHUNK_SIZE
        chunk_content = content[start:end]

        chunks.append(
            {
                "path": document["path"],
                "content": chunk_content,
                "chunk_index": chunk_index,
                "size": len(chunk_content),
                "sha": document["sha"],
            }
        )

        if end >= len(content):
            break

        start = end - CHUNK_OVERLAP
        chunk_index += 1

    return chunks


def chunk_documents(
    documents: list[Document],
) -> list[Chunk]:
    chunks = []

    for document in documents:
        chunks.extend(
            chunk_document(document)
        )

    return chunks