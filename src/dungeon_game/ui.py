"""Console user interface."""

import sys

try:
    import msvcrt
except ImportError:  # pragma: no cover - Not available on Linux.
    msvcrt = None

try:
    import termios
    import tty
except ImportError:  # pragma: no cover - Not available on Windows.
    termios = None
    tty = None

from dungeon_game.game import Game, GameEvent
from dungeon_game.repositories.score_repository import ScoreRepository


class ConsoleUI:
    EVENT_MESSAGES = {
        GameEvent.HIT_WALL: "Törmäsit seinään.",
        GameEvent.EXIT_FOUND: "Löysit uloskäynnin!",
        GameEvent.QUIT: "Poistuit pelistä.",
        GameEvent.GAME_ALREADY_OVER: "Peli on jo päättynyt.",
        GameEvent.INVALID_COMMAND: "Tuntematon komento. Käytä: w, a, s, d, u tai q.",
        GameEvent.PLAYER_ATTACKED: "Hyökkäsit viholliseen.",
        GameEvent.ENEMY_DEFEATED: "Vihollinen kaatui.",
        GameEvent.PLAYER_DIED_IN_COMBAT: "Kuolit taistelussa.",
        GameEvent.ENEMY_HIT_PLAYER: "Vihollinen osui sinuun.",
        GameEvent.ENEMY_HIT_PLAYER_FATAL: "Vihollinen osui sinuun. Kuolit.",
        GameEvent.POTION_PICKED_UP: "Poimit juoman.",
        GameEvent.POTION_USED: "Joit juoman ja sait elämää takaisin.",
        GameEvent.NO_POTION_AVAILABLE: "Sinulla ei ole juomaa käytettävissä.",
    }

    def __init__(self):
        self.score_repository = ScoreRepository()

    def run(self):
        while True:
            self._print_menu()
            choice = self._read_single_key("Valinta (1/2/3): ")

            if choice == "1":
                self._start_new_game()
            elif choice == "2":
                self._show_results()
            elif choice == "3":
                print("Näkemiin!")
                return
            else:
                print("Virheellinen valinta.")

    def _print_menu(self):
        print("\n=== Luolastopeli ===")
        print("1) Uusi peli")
        print("2) Tulokset")
        print("3) Lopeta")

    def _start_new_game(self):
        game = Game()
        message = ""

        while game.is_running:
            self._draw_game(game)
            if message:
                print(message)
            command = self._read_single_key("Komento (w/a/s/d/u, q=lopeta): ")
            event = game.handle_command(command)
            message = self.EVENT_MESSAGES.get(event, "")

        self._draw_game(game)
        if message:
            print(message)
        if game.is_won:
            print("Voitit pelin!")
            print(f"Askeleet: {game.player.steps}")
            print(f"Tapot: {game.player.kills}")
            self._save_result(game.player.steps, game.player.kills)
        else:
            print("Peli päättyi.")

    def _draw_game(self, game: Game):
        print("\n" + "-" * 25)
        for y, row in enumerate(game.map_rows):
            rendered = ""
            for x, tile in enumerate(row):
                enemy = game.enemy_at(x, y)
                potion = game.potion_at(x, y)
                if x == game.player.x and y == game.player.y:
                    rendered += "@"
                elif enemy is not None:
                    rendered += enemy.symbol
                elif potion is not None:
                    rendered += potion.symbol
                else:
                    rendered += tile
            print(rendered)

        print(
            f"HP: {game.player.hp}/{game.player.max_hp} | Askeleet: {game.player.steps} | Tapot: {game.player.kills} | Juomat: {game.player.potions}"
        )

    def _save_result(self, steps: int, kills: int):
        previous_best = self.score_repository.get_best_score()
        self.score_repository.save_score(steps, kills)
        current_best = self.score_repository.get_best_score()

        if previous_best is None or (
            current_best is not None and current_best["steps"] < previous_best["steps"]
        ):
            print("Uusi paras tulos!")

    def _show_results(self):
        print("\n=== Tulokset ===")
        scores = self.score_repository.get_scores()
        if not scores:
            print("Ei tallennettuja tuloksia.")
            return

        best = scores[0]
        print(f"Paras tulos: {best['steps']} askelta, {best['kills']} tappoa")
        print("Top 10:")
        for index, score in enumerate(scores, start=1):
            print(f"{index}. {score['steps']} askelta, {score['kills']} tappoa")

    def _read_single_key(self, prompt: str) -> str:
        """
        Read a single key press from the user without requiring Enter. Falls back to normal input if necessary.
        Checks for Windows (msvcrt) and Unix (termios + tty) methods, and defaults to input() if neither is available.
        """
        print(prompt, end="", flush=True)

        if msvcrt is not None:
            while True:
                key = msvcrt.getwch()

                if key in ("\x00", "\xe0"):
                    msvcrt.getwch()
                    continue

                if key in ("\n", "\r"):
                    continue

                print(key)
                return key.lower()

        if termios is not None and tty is not None and sys.stdin.isatty():
            file_descriptor = sys.stdin.fileno()
            old_settings = termios.tcgetattr(file_descriptor)

            try:
                while True:
                    tty.setcbreak(file_descriptor)
                    key = sys.stdin.read(1)

                    if key in ("\n", "\r"):
                        continue

                    print(key)
                    return key.lower()
            finally:
                termios.tcsetattr(
                    file_descriptor, termios.TCSADRAIN, old_settings)

        value = input().strip().lower()
        return value[:1]
