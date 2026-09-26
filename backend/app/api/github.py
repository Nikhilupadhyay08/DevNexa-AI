from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.services.github import (
    get_file_content,
    get_repository,
)

router = APIRouter(
    prefix="/github",
    tags=["GitHub"],
)


class RepositoryRequest(BaseModel):
    url: str


class FileContentRequest(BaseModel):
    repository_url: str
    path: str
    branch: str


@router.post("/repository")
async def get_github_repository(request: RepositoryRequest):
    parsed_url = urlparse(request.url)

    if parsed_url.netloc.lower() not in {
        "github.com",
        "www.github.com",
    }:
        raise HTTPException(
            status_code=400,
            detail="Please provide a valid GitHub repository URL",
        )

    path_parts = [
        part
        for part in parsed_url.path.strip("/").split("/")
        if part
    ]

    if len(path_parts) != 2:
        raise HTTPException(
            status_code=400,
            detail=(
                "GitHub repository URL must look like "
                "https://github.com/owner/repository"
            ),
        )

    owner, repository = path_parts

    if repository.endswith(".git"):
        repository = repository[:-4]

    try:
        return await get_repository(owner, repository)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )


@router.post("/file")
async def get_github_file(request: FileContentRequest):
    parsed_url = urlparse(request.repository_url)

    if parsed_url.netloc.lower() not in {
        "github.com",
        "www.github.com",
    }:
        raise HTTPException(
            status_code=400,
            detail="Please provide a valid GitHub repository URL",
        )

    path_parts = [
        part
        for part in parsed_url.path.strip("/").split("/")
        if part
    ]

    if len(path_parts) != 2:
        raise HTTPException(
            status_code=400,
            detail=(
                "GitHub repository URL must look like "
                "https://github.com/owner/repository"
            ),
        )

    owner, repository = path_parts

    if repository.endswith(".git"):
        repository = repository[:-4]

    if not request.path.strip():
        raise HTTPException(
            status_code=400,
            detail="File path cannot be empty",
        )

    try:
        content = await get_file_content(
            owner,
            repository,
            request.path,
            request.branch,
        )

        return {
            "repository": f"{owner}/{repository}",
            "path": request.path,
            "branch": request.branch,
            "content": content,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )