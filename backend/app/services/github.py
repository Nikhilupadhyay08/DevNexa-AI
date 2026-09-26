import httpx


GITHUB_API_URL = "https://api.github.com"


async def get_repository(owner: str, repository: str) -> dict:
    url = f"{GITHUB_API_URL}/repos/{owner}/{repository}"

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=headers,
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