from dungeon_game.repositories.score_repository import ScoreRepository


def test_save_score_creates_file_and_returns_best_score(tmp_path):
    file_path = tmp_path / "scores.json"
    repository = ScoreRepository(str(file_path))

    repository.save_score(12, 3, "normal")
    repository.save_score(7, 1, "easy")

    assert repository.get_best_score() == {
        "steps": 7,
        "kills": 1,
        "difficulty": "easy",
    }
    assert repository.get_scores() == [
        {"steps": 7, "kills": 1, "difficulty": "easy"},
        {"steps": 12, "kills": 3, "difficulty": "normal"},
    ]


def test_get_scores_returns_only_top_twenty_sorted(tmp_path):
    file_path = tmp_path / "scores.json"
    repository = ScoreRepository(str(file_path))

    for score in range(20, 0, -1):
        repository.save_score(score, kills=score % 4, difficulty="normal")

    scores = repository.get_scores()
    assert len(scores) == 20
    assert scores[0]["steps"] == 1
    assert all(s["difficulty"] == "normal" for s in scores)


def test_get_scores_handles_invalid_json_shape(tmp_path):
    file_path = tmp_path / "scores.json"
    file_path.write_text('{"score": 5}', encoding="utf-8")
    repository = ScoreRepository(str(file_path))

    assert repository.get_scores() == []


def test_get_scores_handles_malformed_json(tmp_path):
    file_path = tmp_path / "scores.json"
    file_path.write_text('{"score": ', encoding="utf-8")
    repository = ScoreRepository(str(file_path))

    assert repository.get_scores() == []


def test_get_scores_supports_old_integer_score_format(tmp_path):
    file_path = tmp_path / "scores.json"
    file_path.write_text('[12, 7]', encoding="utf-8")
    repository = ScoreRepository(str(file_path))

    scores = repository.get_scores()
    assert len(scores) == 2
    assert all(s["difficulty"] == "normal" for s in scores)


def test_get_scores_supports_old_dict_format_without_difficulty(tmp_path):
    file_path = tmp_path / "scores.json"
    file_path.write_text(
        '[{"steps": 12, "kills": 3}, {"steps": 7, "kills": 1}]',
        encoding="utf-8",
    )
    repository = ScoreRepository(str(file_path))

    scores = repository.get_scores()
    assert len(scores) == 2
    assert all(s["difficulty"] == "normal" for s in scores)


def test_no_scores_returns_empty_list(tmp_path):
    file_path = tmp_path / "scores.json"
    repository = ScoreRepository(str(file_path))
    assert repository.get_scores() == []
    assert repository.get_best_score() is None


def test_get_scores_by_difficulty_easy(tmp_path):
    file_path = tmp_path / "scores.json"
    repository = ScoreRepository(str(file_path))

    repository.save_score(12, 3, "normal")
    repository.save_score(7, 1, "easy")
    repository.save_score(5, 2, "easy")

    easy_scores = repository.get_scores_by_difficulty("easy")
    assert len(easy_scores) == 2
    assert easy_scores[0]["steps"] == 5
    assert easy_scores[1]["steps"] == 7


def test_get_scores_by_difficulty_hard(tmp_path):
    file_path = tmp_path / "scores.json"
    repository = ScoreRepository(str(file_path))

    repository.save_score(12, 3, "normal")
    repository.save_score(20, 5, "hard")
    repository.save_score(25, 4, "hard")

    hard_scores = repository.get_scores_by_difficulty("hard")
    assert len(hard_scores) == 2
    assert all(s["difficulty"] == "hard" for s in hard_scores)


def test_get_scores_by_difficulty_returns_empty_for_no_matches(tmp_path):
    file_path = tmp_path / "scores.json"
    repository = ScoreRepository(str(file_path))

    repository.save_score(12, 3, "normal")

    hard_scores = repository.get_scores_by_difficulty("hard")
    assert len(hard_scores) == 0
