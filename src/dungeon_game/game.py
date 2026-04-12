"""Game logic for movement and map interactions."""

from dungeon_game.game_map import DEFAULT_MAP, EXIT, WALL
from dungeon_game.models.enemy import Enemy
from dungeon_game.models.player import Player


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

    def _resolve_player_attack(self, enemy: Enemy) -> str:
        enemy.take_damage(self.player.damage)
        if not enemy.is_alive:
            self.enemies.remove(enemy)
            self.player.kills += 1
            return "Vihollinen kaatui."

        self.player.hp -= enemy.damage
        if self.player.hp <= 0:
            self.player.hp = 0
            self.is_running = False
            self.is_won = False
            return "Kuolit taistelussa."

        return "Hyökkäsit viholliseen."

    def _enemy_turn(self) -> str | None:
        for enemy in self.enemies:
            distance = abs(enemy.x - self.player.x) + \
                abs(enemy.y - self.player.y)
            if distance == 1:
                self.player.hp -= enemy.damage
                if self.player.hp <= 0:
                    self.player.hp = 0
                    self.is_running = False
                    self.is_won = False
                    return "Vihollinen osui sinuun. Kuolit."
                return "Vihollinen osui sinuun."
        return None

    def move_player(self, dx: int, dy: int) -> str | None:
        next_x = self.player.x + dx
        next_y = self.player.y + dy

        next_tile = self.tile_at(next_x, next_y)
        if next_tile == WALL:
            return "Törmäsit seinään."

        enemy = self.enemy_at(next_x, next_y)
        if enemy is not None:
            return self._resolve_player_attack(enemy)

        self.player.x = next_x
        self.player.y = next_y
        self.player.steps += 1

        if next_tile == EXIT:
            self.is_running = False
            self.is_won = True
            return "Löysit uloskäynnin!"

        return None

    def handle_command(self, command: str) -> str | None:
        movement = {
            "w": (0, -1),
            "s": (0, 1),
            "a": (-1, 0),
            "d": (1, 0),
        }

        if not self.is_running:
            return "Peli on jo päättynyt."

        if command == "q":
            self.is_running = False
            return "Poistuit pelistä."

        if command in movement:
            dx, dy = movement[command]
            result = self.move_player(dx, dy)

            if not self.is_running:
                return result

            if result is not None:
                return result

            enemy_result = self._enemy_turn()
            if enemy_result is not None:
                return enemy_result

            return None

        return "Tuntematon komento. Käytä: w, a, s, d tai q."
