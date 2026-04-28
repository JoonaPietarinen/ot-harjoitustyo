"""Enemy model"""

from dataclasses import dataclass


@dataclass
class Enemy:
    """Represents an enemy character that attacks the player.
    
    Attributes:
        x: X-coordinate on the game map.
        y: Y-coordinate on the game map.
        hp: Current health points.
        damage: Damage dealt per attack.
        symbol: Character symbol representing the enemy on the map.
    """
    x: int
    y: int
    hp: int = 2
    damage: int = 1
    symbol: str = "E"

    @property
    def is_alive(self) -> bool:
        """Check if the enemy is still alive.
        
        Returns:
            True if hp is greater than 0, False otherwise.
        """
        return self.hp > 0

    def take_damage(self, amount: int) -> None:
        """Apply damage to the enemy.
        
        Args:
            amount: The amount of damage to apply.
        """
        self.hp = max(0, self.hp - amount)
