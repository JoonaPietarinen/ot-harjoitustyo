"""Score persistence for dungeon game."""

from __future__ import annotations

import json
from pathlib import Path

ScoreEntry = dict[str, int]


class ScoreRepository:
    def __init__(self, file_path: str = "data/scores.json"):
        self._file_path = Path(file_path)

    def get_scores(self, limit: int = 10) -> list[ScoreEntry]:
        scores = self._read_scores()
        scores.sort(key=lambda item: (item["steps"], -item["kills"]))
        return scores[:limit]

    def get_best_score(self) -> ScoreEntry | None:
        scores = self.get_scores(limit=1)
        if not scores:
            return None
        return scores[0]

    def save_score(self, steps: int, kills: int) -> None:
        scores = self._read_scores()
        scores.append({"steps": steps, "kills": kills})
        scores.sort(key=lambda item: (item["steps"], -item["kills"]))
        self._write_scores(scores[:10])

    def _read_scores(self) -> list[ScoreEntry]:
        if not self._file_path.exists():
            return []

        try:
            with self._file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError):
            return []

        if not isinstance(data, list):
            return []

        scores: list[ScoreEntry] = []
        for item in data:
            normalized = self._normalize_score(item)
            if normalized is not None:
                scores.append(normalized)

        return scores

    def _normalize_score(self, item: object) -> ScoreEntry | None:
        if isinstance(item, int):
            return {"steps": item, "kills": 0}

        if isinstance(item, dict):
            steps = item.get("steps")
            kills = item.get("kills", 0)
            if isinstance(steps, int) and isinstance(kills, int):
                return {"steps": steps, "kills": kills}

        return None

    def _write_scores(self, scores: list[ScoreEntry]) -> None:
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        with self._file_path.open("w", encoding="utf-8") as file:
            json.dump(scores, file)
