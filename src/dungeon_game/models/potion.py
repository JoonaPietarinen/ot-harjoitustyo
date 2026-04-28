"""Potion model."""

from dataclasses import dataclass


@dataclass
class Potion:
    """Represents a healing potion that can be collected and used by the player.

    Attributes:
        x: X-coordinate on the game map.
        y: Y-coordinate on the game map.
        heal_amount: Amount of health points restored when used.
        symbol: Character symbol representing the potion on the map.
    """

    x: int
    y: int
    heal_amount: int = 4
    symbol: str = "!"
