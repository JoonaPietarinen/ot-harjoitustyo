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
        enemy_type: Type of enemy ('goblin' or 'orc').
    """
    x: int
    y: int
    hp: int = 5
    damage: int = 1
    symbol: str = "E"
    enemy_type: str = "orc"

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


def create_enemy(enemy_type: str, x: int, y: int) -> Enemy:
    """Factory function to create enemies of different types.
    
    Args:
        enemy_type: Type of enemy ('goblin' or 'orc').
        x: X-coordinate.
        y: Y-coordinate.
        
    Returns:
        An Enemy instance with appropriate stats.
    """
    if enemy_type == "goblin":
        return Enemy(x=x, y=y, hp=2, damage=1, symbol="e", enemy_type="goblin")
    return Enemy(x=x, y=y, hp=5, damage=1, symbol="E", enemy_type="orc")
