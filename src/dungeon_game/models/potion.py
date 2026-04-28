"""Potion model."""

from dataclasses import dataclass


@dataclass
class Potion:
    x: int
    y: int
    heal_amount: int = 4
    symbol: str = "!"
