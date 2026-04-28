"""Player model."""

from dataclasses import dataclass


@dataclass
class Player:
    x: int
    y: int
    hp: int = 3
    max_hp: int = 3
    steps: int = 0
    damage: int = 2
    kills: int = 0
    potions: int = 0
