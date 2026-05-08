from repo_radar_mcp.scoring import calculate_repository_score


def test_active_repository_scores_higher_than_archived_repository():
    active_repo = {
        "stars": 1000,
        "forks": 200,
        "open_issues": 10,
        "license": "MIT",
        "archived": False,
        "updated_at": "2026-01-01T00:00:00Z",
    }

    archived_repo = {
        "stars": 1000,
        "forks": 200,
        "open_issues": 10,
        "license": "MIT",
        "archived": True,
        "updated_at": "2026-01-01T00:00:00Z",
    }

    active_score = calculate_repository_score(active_repo)["score"]
    archived_score = calculate_repository_score(archived_repo)["score"]

    assert active_score > archived_score


def test_score_is_between_zero_and_one_hundred():
    repo = {
        "stars": 999999,
        "forks": 999999,
        "open_issues": 0,
        "license": "MIT",
        "archived": False,
        "updated_at": "2026-01-01T00:00:00Z",
    }

    score = calculate_repository_score(repo)["score"]

    assert 0 <= score <= 100
