"""Score persistence for dungeon game."""

from __future__ import annotations

import json
from pathlib import Path

ScoreEntry = dict[str, int]


class ScoreRepository:
    """Manages persistence of game scores to a JSON file.
    
    Stores game results (steps taken and enemies defeated) in a JSON file,
    allowing players to view their best scores and personal records.
    Maintains backward compatibility with old score files that only stored steps.
    """

    def __init__(self, file_path: str = "data/scores.json"):
        """Initialize the repository with a file path.
        
        Args:
            file_path: Path to the JSON file where scores are stored.
        """
        self._file_path = Path(file_path)

    def get_scores(self, limit: int = 10) -> list[ScoreEntry]:
        """Get the best scores sorted by steps and kills.
        
        Args:
            limit: Maximum number of scores to return (default 10).
            
        Returns:
            A list of score dictionaries sorted by steps (ascending) and kills (descending).
        """
        scores = self._read_scores()
        scores.sort(key=lambda item: (item["steps"], -item["kills"]))
        return scores[:limit]

    def get_best_score(self) -> ScoreEntry | None:
        """Get the single best score.
        
        Returns:
            The best score dictionary or None if no scores exist.
        """
        scores = self.get_scores(limit=1)
        if not scores:
            return None
        return scores[0]

    def save_score(self, steps: int, kills: int) -> None:
        """Save a new score to the file.
        
        Args:
            steps: Number of steps taken in the game.
            kills: Number of enemies defeated.
        """
        scores = self._read_scores()
        scores.append({"steps": steps, "kills": kills})
        scores.sort(key=lambda item: (item["steps"], -item["kills"]))
        self._write_scores(scores[:10])

    def _read_scores(self) -> list[ScoreEntry]:
        """Read and parse scores from the JSON file.
        
        Returns:
            A list of score dictionaries. Returns empty list if file doesn't exist or is invalid.
        """
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
        """Convert various score formats to a standard dictionary.
        
        Supports both old (integer only) and new (dict with steps and kills) formats.
        
        Args:
            item: The score item to normalize.
            
        Returns:
            A normalized score dictionary or None if the format is invalid.
        """
        if isinstance(item, int):
            return {"steps": item, "kills": 0}

        if isinstance(item, dict):
            steps = item.get("steps")
            kills = item.get("kills", 0)
            if isinstance(steps, int) and isinstance(kills, int):
                return {"steps": steps, "kills": kills}

        return None

    def _write_scores(self, scores: list[ScoreEntry]) -> None:
        """Write scores to the JSON file.
        
        Args:
            scores: List of score dictionaries to write.
        """
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        with self._file_path.open("w", encoding="utf-8") as file:
            json.dump(scores, file)
