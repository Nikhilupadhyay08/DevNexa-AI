import base64

import httpx


GITHUB_API_URL = "https://api.github.com"


def get_github_headers() -> dict:
    return {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


async def get_repository(owner: str, repository: str) -> dict:
    url = f"{GITHUB_API_URL}/repos/{owner}/{repository}"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=get_github_headers(),
            timeout=10.0,
        )

    if response.status_code == 404:
        raise ValueError("GitHub repository not found")

    if response.status_code != 200:
        raise ValueError(
            f"GitHub API request failed with status {response.status_code}"
        )

    data = response.json()

    return {
        "name": data["name"],
        "full_name": data["full_name"],
        "owner": data["owner"]["login"],
        "description": data["description"],
        "default_branch": data["default_branch"],
        "private": data["private"],
        "html_url": data["html_url"],
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
    }


async def get_repository_tree(
    owner: str,
    repository: str,
    branch: str,
) -> list[dict]:
    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repository}/git/trees/{branch}"
    )

    params = {
        "recursive": "1",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=get_github_headers(),
            params=params,
            timeout=20.0,
        )

    if response.status_code == 404:
        raise ValueError("GitHub repository or branch not found")

    if response.status_code != 200:
        raise ValueError(
            f"GitHub API request failed with status {response.status_code}"
        )

    data = response.json()

    return [
        {
            "path": item["path"],
            "type": item["type"],
            "size": item.get("size"),
            "sha": item["sha"],
        }
        for item in data.get("tree", [])
    ]


async def get_file_content(
    owner: str,
    repository: str,
    path: str,
    branch: str,
) -> str:
    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repository}/contents/{path}"
    )

    params = {
        "ref": branch,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=get_github_headers(),
            params=params,
            timeout=20.0,
        )

    if response.status_code == 404:
        raise ValueError("GitHub file not found")

    if response.status_code != 200:
        raise ValueError(
            f"GitHub API request failed with status {response.status_code}"
        )

    data = response.json()

    if data.get("type") != "file":
        raise ValueError("The requested path is not a file")

    if data.get("encoding") != "base64":
        raise ValueError("Unsupported GitHub file encoding")

    try:
        decoded_content = base64.b64decode(
            data["content"]
        ).decode("utf-8")
    except (KeyError, ValueError, UnicodeDecodeError) as error:
        raise ValueError("Unable to decode GitHub file content") from error

    return decoded_content