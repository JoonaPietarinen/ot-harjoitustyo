"""Player model."""

from dataclasses import dataclass


@dataclass
class Player:
    """Represents the player character in the dungeon game.

    Attributes:
        x: X-coordinate on the game map.
        y: Y-coordinate on the game map.
        hp: Current health points.
        max_hp: Maximum health points.
        steps: Total number of steps taken by the player.
        damage: Damage dealt per attack.
        kills: Number of enemies defeated.
        potions: Number of healing potions in inventory.
    """

    x: int
    y: int
    hp: int = 3
    max_hp: int = 3
    steps: int = 0
    damage: int = 2
    kills: int = 0
    potions: int = 0
