"""Score persistence for dungeon game."""

from __future__ import annotations

import json
from pathlib import Path


class ScoreRepository:
    def __init__(self, file_path: str = "data/scores.json"):
        self._file_path = Path(file_path)

    def get_scores(self, limit: int = 10) -> list[int]:
        scores = self._read_scores()
        scores.sort()
        return scores[:limit]

    def get_best_score(self) -> int | None:
        scores = self.get_scores(limit=1)
        if not scores:
            return None
        return scores[0]

    def save_score(self, steps: int) -> None:
        scores = self._read_scores()
        scores.append(steps)
        scores.sort()
        self._write_scores(scores[:10])

    def _read_scores(self) -> list[int]:
        if not self._file_path.exists():
            return []

        try:
            with self._file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError):
            return []

        if not isinstance(data, list):
            return []

        numeric_scores = []
        for item in data:
            if isinstance(item, int):
                numeric_scores.append(item)

        return numeric_scores

    def _write_scores(self, scores: list[int]) -> None:
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        with self._file_path.open("w", encoding="utf-8") as file:
            json.dump(scores, file)
