from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class RepositorySummary:
    full_name: str
    name: str
    owner: str
    html_url: str
    description: str | None
    language: str | None
    stars: int
    forks: int
    open_issues: int
    license: str | None
    topics: list[str]
    archived: bool
    updated_at: str | None

    @classmethod
    def from_github_item(cls, item: dict[str, Any]) -> "RepositorySummary":
        license_data = item.get("license") or {}
        owner_data = item.get("owner") or {}

        return cls(
            full_name=item.get("full_name", ""),
            name=item.get("name", ""),
            owner=owner_data.get("login", ""),
            html_url=item.get("html_url", ""),
            description=item.get("description"),
            language=item.get("language"),
            stars=int(item.get("stargazers_count") or 0),
            forks=int(item.get("forks_count") or 0),
            open_issues=int(item.get("open_issues_count") or 0),
            license=license_data.get("spdx_id") if license_data else None,
            topics=item.get("topics") or [],
            archived=bool(item.get("archived", False)),
            updated_at=item.get("updated_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "full_name": self.full_name,
            "name": self.name,
            "owner": self.owner,
            "url": self.html_url,
            "description": self.description,
            "language": self.language,
            "stars": self.stars,
            "forks": self.forks,
            "open_issues": self.open_issues,
            "license": self.license,
            "topics": self.topics,
            "archived": self.archived,
            "updated_at": self.updated_at,
        }
