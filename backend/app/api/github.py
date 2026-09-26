from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.services.github import get_repository


router = APIRouter(
    prefix="/github",
    tags=["GitHub"],
)


class RepositoryRequest(BaseModel):
    url: str


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
            detail="GitHub repository URL must look like https://github.com/owner/repository",
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