from backend.app.services.github import (
    get_file_content,
    get_repository,
    get_source_files,
)


MAX_FILE_SIZE = 1_000_000


async def ingest_repository(repository_url: str) -> list[dict]:
    """
    Retrieve source files from a GitHub repository
    and return their paths and contents.
    """

    repository = repository_url.rstrip("/")

    if repository.endswith(".git"):
        repository = repository[:-4]

    parts = repository.split("/")

    if len(parts) < 2:
        raise ValueError("Invalid GitHub repository URL")

    owner = parts[-2]
    repository_name = parts[-1]

    repository_data = await get_repository(
        owner,
        repository_name,
    )

    branch = repository_data["default_branch"]

    source_files = await get_source_files(
        owner,
        repository_name,
        branch,
    )

    documents = []

    for file in source_files:
        path = file["path"]
        size = file.get("size") or 0

        if size > MAX_FILE_SIZE:
            continue

        try:
            content = await get_file_content(
                owner,
                repository_name,
                path,
                branch,
            )

        except ValueError:
            continue

        documents.append(
            {
                "path": path,
                "content": content,
                "size": size,
                "sha": file["sha"],
            }
        )

    return documents