from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from .formatters import comparison_to_markdown, repositories_to_markdown
from .github_client import GitHubClient
from .scoring import add_scores, calculate_repository_score

mcp = FastMCP("Repo Radar MCP")


@mcp.tool()
def search_repositories(
    topic: str,
    language: str | None = None,
    limit: int = 5,
    min_stars: int = 0,
    sort: str = "stars",
) -> dict[str, Any]:
    """Search GitHub repositories by topic, language and minimum stars.

    Args:
        topic: Search topic. Examples: "mcp server", "rag chatbot", "trading bot".
        language: Optional programming language. Examples: "Python", "JavaScript".
        limit: Number of repositories to return. Default 5. Maximum 10.
        min_stars: Optional minimum stars filter.
        sort: Sort mode. Use "stars", "forks" or "updated".
    """

    client = GitHubClient()
    return client.search_repositories(
        topic=topic,
        language=language,
        limit=limit,
        min_stars=min_stars,
        sort=sort,
    )


@mcp.tool()
def search_repositories_markdown(
    topic: str,
    language: str | None = None,
    limit: int = 5,
    min_stars: int = 0,
    sort: str = "stars",
) -> str:
    """Search GitHub repositories and return a Markdown report."""

    result = search_repositories(
        topic=topic,
        language=language,
        limit=limit,
        min_stars=min_stars,
        sort=sort,
    )

    return repositories_to_markdown(result)


@mcp.tool()
def rank_repositories(
    topic: str,
    language: str | None = None,
    limit: int = 5,
    min_stars: int = 0,
    sort: str = "stars",
) -> dict[str, Any]:
    """Search and rank repositories with a simple Repo Radar score."""

    result = search_repositories(
        topic=topic,
        language=language,
        limit=limit,
        min_stars=min_stars,
        sort=sort,
    )
    result["repositories"] = add_scores(result["repositories"])
    return result


@mcp.tool()
def rank_repositories_markdown(
    topic: str,
    language: str | None = None,
    limit: int = 5,
    min_stars: int = 0,
    sort: str = "stars",
) -> str:
    """Search, rank and return repositories as a Markdown report."""

    result = rank_repositories(
        topic=topic,
        language=language,
        limit=limit,
        min_stars=min_stars,
        sort=sort,
    )

    return repositories_to_markdown(result, include_scores=True)


@mcp.tool()
def analyze_repository(full_name: str) -> dict[str, Any]:
    """Analyze one GitHub repository using the format owner/name."""

    client = GitHubClient()
    repository = client.get_repository(full_name)
    repository["radar_score"] = calculate_repository_score(repository)
    return repository


@mcp.tool()
def analyze_repository_markdown(full_name: str) -> str:
    """Analyze one GitHub repository and return a Markdown report."""

    repository = analyze_repository(full_name)
    result = {
        "query": full_name,
        "sort": "single_repository",
        "total_count": 1,
        "repositories": [repository],
    }
    return repositories_to_markdown(result, include_scores=True)


@mcp.tool()
def compare_repositories(repositories: str) -> dict[str, Any]:
    """Compare multiple repositories.

    Args:
        repositories: Comma-separated repository names using owner/name format.
            Example: "freqtrade/freqtrade, ccxt/ccxt, hummingbot/hummingbot"
    """

    client = GitHubClient()
    names = [item.strip() for item in repositories.split(",") if item.strip()]

    if not names:
        raise ValueError("At least one repository is required.")

    analyzed = []

    for name in names[:10]:
        repo = client.get_repository(name)
        repo["radar_score"] = calculate_repository_score(repo)
        analyzed.append(repo)

    analyzed = sorted(
        analyzed,
        key=lambda item: item["radar_score"]["score"],
        reverse=True,
    )

    return {
        "repositories": analyzed,
        "count": len(analyzed),
    }


@mcp.tool()
def compare_repositories_markdown(repositories: str) -> str:
    """Compare multiple repositories and return a Markdown table."""

    result = compare_repositories(repositories)
    return comparison_to_markdown(result["repositories"])


@mcp.tool()
def get_repository_readme(full_name: str, max_chars: int = 8000) -> dict[str, Any]:
    """Fetch the README of a GitHub repository using owner/name format."""

    client = GitHubClient()
    safe_max_chars = max(500, min(int(max_chars), 20000))
    return client.get_readme(full_name, max_chars=safe_max_chars)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
