from app.services.github import get_github_headers


def test_get_github_headers():
    headers = get_github_headers()

    assert headers["Accept"] == "application/vnd.github+json"
    assert headers["X-GitHub-Api-Version"] == "2022-11-28"
    assert headers["Authorization"].startswith("Bearer ")