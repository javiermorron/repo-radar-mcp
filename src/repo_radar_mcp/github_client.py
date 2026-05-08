from __future__ import annotations

import base64
import os
from typing import Any

import requests
from dotenv import load_dotenv

from .models import RepositorySummary

load_dotenv()


class GitHubClientError(RuntimeError):
    """Raised when the GitHub API returns an error."""


class GitHubClient:
    def __init__(self) -> None:
        self.base_url = "https://api.github.com"
        self.token = os.getenv("GITHUB_TOKEN", "").strip()
        self.api_version = os.getenv("GITHUB_API_VERSION", "2022-11-28").strip()
        self.user_agent = os.getenv("GITHUB_USER_AGENT", "repo-radar-mcp/1.0.0").strip()

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": self.api_version,
                "User-Agent": self.user_agent,
            }
        )

        if self.token:
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        response = self.session.request(method=method, url=url, timeout=30, **kwargs)

        if response.status_code >= 400:
            try:
                payload = response.json()
                message = payload.get("message", response.text)
            except ValueError:
                message = response.text

            raise GitHubClientError(
                f"GitHub API error {response.status_code}: {message}"
            )

        try:
            return response.json()
        except ValueError as exc:
            raise GitHubClientError("GitHub API returned invalid JSON.") from exc

    @staticmethod
    def build_search_query(topic: str, language: str | None = None, min_stars: int = 0) -> str:
        parts = [topic.strip()]

        if language:
            parts.append(f"language:{language.strip()}")

        if min_stars and min_stars > 0:
            parts.append(f"stars:>={int(min_stars)}")

        return " ".join(part for part in parts if part)

    def search_repositories(
        self,
        topic: str,
        language: str | None = None,
        limit: int = 5,
        min_stars: int = 0,
        sort: str = "stars",
    ) -> dict[str, Any]:
        if not topic or not topic.strip():
            raise ValueError("topic is required.")

        safe_limit = max(1, min(int(limit), 10))
        allowed_sort = sort if sort in {"stars", "forks", "updated"} else "stars"

        query = self.build_search_query(topic, language, min_stars)

        payload = self._request(
            "GET",
            "/search/repositories",
            params={
                "q": query,
                "sort": allowed_sort,
                "order": "desc",
                "per_page": safe_limit,
            },
        )

        repositories = [
            RepositorySummary.from_github_item(item).to_dict()
            for item in payload.get("items", [])
        ]

        return {
            "query": query,
            "sort": allowed_sort,
            "total_count": payload.get("total_count", 0),
            "incomplete_results": payload.get("incomplete_results", False),
            "repositories": repositories,
        }

    def get_repository(self, full_name: str) -> dict[str, Any]:
        owner, repo = self._split_full_name(full_name)
        payload = self._request("GET", f"/repos/{owner}/{repo}")
        return RepositorySummary.from_github_item(payload).to_dict()

    def get_readme(self, full_name: str, max_chars: int = 8000) -> dict[str, Any]:
        owner, repo = self._split_full_name(full_name)
        payload = self._request("GET", f"/repos/{owner}/{repo}/readme")

        encoding = payload.get("encoding")
        content = payload.get("content", "")

        if encoding != "base64":
            raise GitHubClientError(f"Unsupported README encoding: {encoding}")

        decoded = base64.b64decode(content).decode("utf-8", errors="replace")

        return {
            "repository": full_name,
            "name": payload.get("name"),
            "path": payload.get("path"),
            "html_url": payload.get("html_url"),
            "content": decoded[:max_chars],
            "truncated": len(decoded) > max_chars,
        }

    @staticmethod
    def _split_full_name(full_name: str) -> tuple[str, str]:
        if "/" not in full_name:
            raise ValueError("Repository must use the format 'owner/name'.")

        owner, repo = [part.strip() for part in full_name.split("/", 1)]

        if not owner or not repo:
            raise ValueError("Repository must use the format 'owner/name'.")

        return owner, repo
