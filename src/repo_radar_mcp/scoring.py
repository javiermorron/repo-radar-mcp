from __future__ import annotations

from datetime import datetime, timezone
from math import log10
from typing import Any


def _parse_github_datetime(value: str | None) -> datetime | None:
    if not value:
        return None

    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def calculate_repository_score(repository: dict[str, Any]) -> dict[str, Any]:
    """Calculate a simple usefulness score from 0 to 100.

    This score is intentionally simple and explainable. It is not a definitive
    measure of quality.
    """

    stars = int(repository.get("stars") or 0)
    forks = int(repository.get("forks") or 0)
    open_issues = int(repository.get("open_issues") or 0)
    archived = bool(repository.get("archived", False))
    license_id = repository.get("license")
    updated_at = repository.get("updated_at")

    score = 0
    reasons: list[str] = []

    stars_score = min(30, int(log10(max(stars, 1)) * 10))
    score += stars_score
    if stars >= 1000:
        reasons.append("Strong community adoption.")
    elif stars >= 100:
        reasons.append("Moderate community adoption.")
    else:
        reasons.append("Low community adoption.")

    forks_score = min(15, int(log10(max(forks, 1)) * 6))
    score += forks_score
    if forks >= 100:
        reasons.append("Good fork activity.")

    updated = _parse_github_datetime(updated_at)
    if updated:
        days_since_update = (datetime.now(timezone.utc) - updated).days
        if days_since_update <= 90:
            score += 25
            reasons.append("Recently updated.")
        elif days_since_update <= 365:
            score += 15
            reasons.append("Updated within the last year.")
        else:
            score += 5
            reasons.append("Not updated recently.")
    else:
        reasons.append("Update date unavailable.")

    if license_id and license_id != "NOASSERTION":
        score += 15
        reasons.append(f"Clear license: {license_id}.")
    else:
        reasons.append("License is missing or unclear.")

    if open_issues == 0:
        score += 10
        reasons.append("No open issues detected.")
    elif stars > 0 and open_issues / max(stars, 1) < 0.05:
        score += 10
        reasons.append("Open issues look reasonable relative to popularity.")
    else:
        score += 3
        reasons.append("Open issues may require inspection.")

    if archived:
        score -= 30
        reasons.append("Repository is archived.")

    final_score = max(0, min(100, score))

    if final_score >= 80:
        recommendation = "study_or_use"
    elif final_score >= 60:
        recommendation = "study"
    elif final_score >= 40:
        recommendation = "inspect_manually"
    else:
        recommendation = "low_priority"

    return {
        "score": final_score,
        "recommendation": recommendation,
        "reasons": reasons,
    }


def add_scores(repositories: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched = []

    for repo in repositories:
        scored = dict(repo)
        scored["radar_score"] = calculate_repository_score(repo)
        enriched.append(scored)

    return sorted(
        enriched,
        key=lambda item: item["radar_score"]["score"],
        reverse=True,
    )
