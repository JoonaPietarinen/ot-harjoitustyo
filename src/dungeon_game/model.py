"""Core game state models."""

from dataclasses import dataclass


@dataclass
class Player:
    x: int
    y: int
    hp: int = 10
    max_hp: int = 10
    steps: int = 0
