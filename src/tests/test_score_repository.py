from dungeon_game.repositories.score_repository import ScoreRepository


def test_save_score_creates_file_and_returns_best_score(tmp_path):
    file_path = tmp_path / "scores.json"
    repository = ScoreRepository(str(file_path))

    repository.save_score(12)
    repository.save_score(7)

    assert repository.get_best_score() == 7
    assert repository.get_scores() == [7, 12]


def test_get_scores_returns_only_top_ten_sorted(tmp_path):
    file_path = tmp_path / "scores.json"
    repository = ScoreRepository(str(file_path))

    for score in range(20, 0, -1):
        repository.save_score(score)

    assert repository.get_scores() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


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
