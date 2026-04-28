"""Game logic for movement and map interactions."""

from enum import Enum, auto

from dungeon_game.game_map import DEFAULT_MAP, EXIT, WALL
from dungeon_game.models.enemy import Enemy
from dungeon_game.models.player import Player
from dungeon_game.models.potion import Potion


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
    POTION_PICKED_UP = auto()
    POTION_USED = auto()
    NO_POTION_AVAILABLE = auto()


class Game:
    def __init__(self):
        self.map_rows = [list(row) for row in DEFAULT_MAP]
        self.height = len(self.map_rows)
        self.width = len(self.map_rows[0])
        self.player = Player(x=1, y=1)
        self.enemies = [Enemy(x=8, y=1), Enemy(x=6, y=5), Enemy(x=7, y=4)]
        self.potions = [Potion(x=4, y=1)]
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

    def potion_at(self, x: int, y: int) -> Potion | None:
        for potion in self.potions:
            if potion.x == x and potion.y == y:
                return potion
        return None

    def _collect_potion(self, x: int, y: int) -> GameEvent:
        potion = self.potion_at(x, y)
        if potion is None:
            return GameEvent.NONE

        self.potions.remove(potion)
        self.player.potions += 1
        return GameEvent.POTION_PICKED_UP

    def use_potion(self) -> GameEvent:
        if self.player.potions <= 0:
            return GameEvent.NO_POTION_AVAILABLE

        self.player.potions -= 1
        self.player.hp = min(self.player.max_hp, self.player.hp + 4)
        return GameEvent.POTION_USED

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

        potion_event = self._collect_potion(next_x, next_y)
        if next_tile == EXIT:
            self.is_running = False
            self.is_won = True
            return GameEvent.EXIT_FOUND

        if potion_event != GameEvent.NONE:
            return potion_event

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

        if command == "u":
            result = self.use_potion()
            if result == GameEvent.POTION_USED:
                enemy_result = self._enemy_turn()
                if enemy_result != GameEvent.NONE:
                    return enemy_result
            return result

        if command in movement:
            dx, dy = movement[command]
            result = self.move_player(dx, dy)

            if not self.is_running:
                return result

            if result == GameEvent.NONE:
                enemy_result = self._enemy_turn()
                if enemy_result != GameEvent.NONE:
                    return enemy_result
                return GameEvent.NONE

            if result in (GameEvent.POTION_PICKED_UP,):
                enemy_result = self._enemy_turn()
                if enemy_result != GameEvent.NONE:
                    return enemy_result

            return result

        return GameEvent.INVALID_COMMAND
