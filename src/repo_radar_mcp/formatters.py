from __future__ import annotations

from typing import Any


def repositories_to_markdown(result: dict[str, Any], include_scores: bool = False) -> str:
    repositories = result.get("repositories", [])

    lines = [
        "# Repo Radar MCP Report",
        "",
        f"**Query:** `{result.get('query', '')}`",
        f"**Sort:** `{result.get('sort', 'stars')}`",
        f"**Total approximate results:** {result.get('total_count', 0)}",
        "",
    ]

    if not repositories:
        lines.append("No repositories found.")
        return "\n".join(lines)

    for index, repo in enumerate(repositories, start=1):
        lines.extend(
            [
                f"## {index}. {repo.get('full_name')}",
                "",
                f"- ⭐ Stars: {repo.get('stars')}",
                f"- 🍴 Forks: {repo.get('forks')}",
                f"- 🧠 Language: {repo.get('language') or 'Unknown'}",
                f"- 📄 License: {repo.get('license') or 'Unknown'}",
                f"- 🐛 Open issues: {repo.get('open_issues')}",
                f"- 📦 Archived: {repo.get('archived')}",
                f"- 🕒 Updated at: {repo.get('updated_at') or 'Unknown'}",
                f"- 🔗 URL: {repo.get('url')}",
                f"- 📝 Description: {repo.get('description') or 'No description'}",
            ]
        )

        topics = repo.get("topics") or []
        lines.append(f"- 🏷️ Topics: {', '.join(topics) if topics else 'No topics'}")

        if include_scores and repo.get("radar_score"):
            score = repo["radar_score"]
            lines.extend(
                [
                    f"- 📊 Repo Radar Score: {score.get('score')}/100",
                    f"- ✅ Recommendation: `{score.get('recommendation')}`",
                    "- 💡 Reasons:",
                ]
            )
            for reason in score.get("reasons", []):
                lines.append(f"  - {reason}")

        lines.append("")

    return "\n".join(lines)


def comparison_to_markdown(repositories: list[dict[str, Any]]) -> str:
    lines = [
        "# Repository Comparison",
        "",
        "| Repository | Stars | Forks | Language | License | Issues | Score | Recommendation |",
        "|---|---:|---:|---|---|---:|---:|---|",
    ]

    for repo in repositories:
        score_data = repo.get("radar_score", {})
        lines.append(
            "| {name} | {stars} | {forks} | {language} | {license} | {issues} | {score} | {recommendation} |".format(
                name=repo.get("full_name", ""),
                stars=repo.get("stars", 0),
                forks=repo.get("forks", 0),
                language=repo.get("language") or "Unknown",
                license=repo.get("license") or "Unknown",
                issues=repo.get("open_issues", 0),
                score=score_data.get("score", "-"),
                recommendation=score_data.get("recommendation", "-"),
            )
        )

    return "\n".join(lines)
