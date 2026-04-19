"""Game logic for movement and map interactions."""

from enum import Enum, auto

from dungeon_game.game_map import DEFAULT_MAP, EXIT, WALL
from dungeon_game.models.enemy import Enemy
from dungeon_game.models.player import Player


class GameEvent(Enum):
    NONE = auto()
    HIT_WALL = auto()
    EXIT_FOUND = auto()
    QUIT = auto()
    GAME_ALREADY_OVER = auto()
    INVALID_COMMAND = auto()
    PLAYER_ATTACKED = auto()
    ENEMY_DEFEATED = auto()
    PLAYER_DIED_IN_COMBAT = auto()
    ENEMY_HIT_PLAYER = auto()
    ENEMY_HIT_PLAYER_FATAL = auto()


class Game:
    def __init__(self):
        self.map_rows = [list(row) for row in DEFAULT_MAP]
        self.height = len(self.map_rows)
        self.width = len(self.map_rows[0])
        self.player = Player(x=1, y=1)
        self.enemies = [Enemy(x=8, y=1)]
        self.is_running = True
        self.is_won = False

    def tile_at(self, x: int, y: int) -> str:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return WALL
        return self.map_rows[y][x]

    def enemy_at(self, x: int, y: int) -> Enemy | None:
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y and enemy.is_alive:
                return enemy
        return None

    def _resolve_player_attack(self, enemy: Enemy) -> GameEvent:
        enemy.take_damage(self.player.damage)
        if not enemy.is_alive:
            self.enemies.remove(enemy)
            self.player.kills += 1
            return GameEvent.ENEMY_DEFEATED

        self.player.hp -= enemy.damage
        if self.player.hp <= 0:
            self.player.hp = 0
            self.is_running = False
            self.is_won = False
            return GameEvent.PLAYER_DIED_IN_COMBAT

        return GameEvent.PLAYER_ATTACKED

    def _enemy_turn(self) -> GameEvent:
        for enemy in self.enemies:
            distance = abs(enemy.x - self.player.x) + abs(enemy.y - self.player.y)
            if distance == 1:
                self.player.hp -= enemy.damage
                if self.player.hp <= 0:
                    self.player.hp = 0
                    self.is_running = False
                    self.is_won = False
                    return GameEvent.ENEMY_HIT_PLAYER_FATAL
                return GameEvent.ENEMY_HIT_PLAYER
        return GameEvent.NONE

    def move_player(self, dx: int, dy: int) -> GameEvent:
        next_x = self.player.x + dx
        next_y = self.player.y + dy

        next_tile = self.tile_at(next_x, next_y)
        if next_tile == WALL:
            return GameEvent.HIT_WALL

        enemy = self.enemy_at(next_x, next_y)
        if enemy is not None:
            return self._resolve_player_attack(enemy)

        self.player.x = next_x
        self.player.y = next_y
        self.player.steps += 1

        if next_tile == EXIT:
            self.is_running = False
            self.is_won = True
            return GameEvent.EXIT_FOUND

        return GameEvent.NONE

    def handle_command(self, command: str) -> GameEvent:
        movement = {
            "w": (0, -1),
            "s": (0, 1),
            "a": (-1, 0),
            "d": (1, 0),
        }

        if not self.is_running:
            return GameEvent.GAME_ALREADY_OVER

        if command == "q":
            self.is_running = False
            return GameEvent.QUIT

        if command in movement:
            dx, dy = movement[command]
            result = self.move_player(dx, dy)

            if not self.is_running:
                return result

            if result != GameEvent.NONE:
                return result

            enemy_result = self._enemy_turn()
            if enemy_result != GameEvent.NONE:
                return enemy_result

            return GameEvent.NONE

        return GameEvent.INVALID_COMMAND
