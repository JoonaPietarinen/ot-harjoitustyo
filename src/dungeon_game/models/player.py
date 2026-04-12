"""Player model."""

from dataclasses import dataclass


@dataclass
class Player:
    x: int
    y: int
    hp: int = 10
    max_hp: int = 10
    steps: int = 0
    damage: int = 2
    kills: int = 0
