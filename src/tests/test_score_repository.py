from dungeon_game.repositories.score_repository import ScoreRepository


def test_save_score_creates_file_and_returns_best_score(tmp_path):
    file_path = tmp_path / "scores.json"
    repository = ScoreRepository(str(file_path))

    repository.save_score(12, 3)
    repository.save_score(7, 1)

    assert repository.get_best_score() == {"steps": 7, "kills": 1}
    assert repository.get_scores() == [
        {"steps": 7, "kills": 1},
        {"steps": 12, "kills": 3},
    ]


def test_get_scores_returns_only_top_ten_sorted(tmp_path):
    file_path = tmp_path / "scores.json"
    repository = ScoreRepository(str(file_path))

    for score in range(20, 0, -1):
        repository.save_score(score, kills=score % 4)

    assert repository.get_scores() == [
        {"steps": 1, "kills": 1},
        {"steps": 2, "kills": 2},
        {"steps": 3, "kills": 3},
        {"steps": 4, "kills": 0},
        {"steps": 5, "kills": 1},
        {"steps": 6, "kills": 2},
        {"steps": 7, "kills": 3},
        {"steps": 8, "kills": 0},
        {"steps": 9, "kills": 1},
        {"steps": 10, "kills": 2},
    ]


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

    assert repository.get_scores() == [
        {"steps": 7, "kills": 0},
        {"steps": 12, "kills": 0},
    ]
