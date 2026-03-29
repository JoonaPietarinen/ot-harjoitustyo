"""Game logic for movement and map interactions."""

from dungeon_game.game_map import DEFAULT_MAP, EXIT, WALL
from dungeon_game.model import Player


class Game:
    def __init__(self):
        self.map_rows = [list(row) for row in DEFAULT_MAP]
        self.height = len(self.map_rows)
        self.width = len(self.map_rows[0])
        self.player = Player(x=1, y=1)
        self.is_running = True
        self.is_won = False

    def tile_at(self, x: int, y: int) -> str:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return WALL
        return self.map_rows[y][x]

    def move_player(self, dx: int, dy: int) -> str:
        next_x = self.player.x + dx
        next_y = self.player.y + dy

        next_tile = self.tile_at(next_x, next_y)
        if next_tile == WALL:
            return "Törmäsit seinään."

        self.player.x = next_x
        self.player.y = next_y
        self.player.steps += 1

        if next_tile == EXIT:
            self.is_running = False
            self.is_won = True
            return "Löysit uloskäynnin!"

        return

    def handle_command(self, command: str) -> str:
        movement = {
            "w": (0, -1),
            "s": (0, 1),
            "a": (-1, 0),
            "d": (1, 0),
        }

        if command == "q":
            self.is_running = False
            return "Poistuit pelistä."

        if command in movement:
            dx, dy = movement[command]
            return self.move_player(dx, dy)

        return "Tuntematon komento. Käytä: w, a, s, d tai q."
