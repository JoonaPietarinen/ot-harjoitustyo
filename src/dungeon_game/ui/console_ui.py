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

from dungeon_game.game import Game, GameEvent, Difficulty
from dungeon_game.repositories.score_repository import ScoreRepository


class ConsoleUI:
    """Text-based user interface for the dungeon game."""

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
        """Initialize the console UI."""
        self.score_repository = ScoreRepository()
        self.difficulty = Difficulty.NORMAL

    def run(self):
        """Main menu loop."""
        while True:
            self._print_menu()
            choice = self._read_single_key("Valinta (1/2/3): ")

            if choice == "1":
                self._select_difficulty()
            elif choice == "2":
                self._show_results()
            elif choice == "3":
                print("Näkemiin!")
                return
            else:
                print("Virheellinen valinta.")

    def _print_menu(self):
        """Print the main menu."""
        print("\n=== Luolastopeli ===")
        print("1) Uusi peli")
        print("2) Tulokset")
        print("3) Lopeta")

    def _select_difficulty(self):
        """Let player select difficulty level."""
        print("\n=== Valitse vaikeustaso ===")
        print("1) Helppo (Easy)")
        print("2) Normaali (Normal)")
        print("3) Vaikea (Hard)")
        choice = self._read_single_key("Valinta (1/2/3): ")

        if choice == "1":
            self.difficulty = Difficulty.EASY
        elif choice == "2":
            self.difficulty = Difficulty.NORMAL
        elif choice == "3":
            self.difficulty = Difficulty.HARD
        else:
            self.difficulty = Difficulty.NORMAL

        self._start_new_game()

    def _start_new_game(self):
        """Start a new game with the selected difficulty."""
        game = Game(self.difficulty)
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
            print(f"Vaikeustaso: {game.difficulty.value}")
            self._save_result(
                game.player.steps,
                game.player.kills,
                game.difficulty.value,
            )
        else:
            print("Peli päättyi.")

    def _draw_game(self, game: Game):
        """Draw the game map and statistics."""
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

        stats = (
            f"HP: {game.player.hp}/{game.player.max_hp} | "
            f"Askeleet: {game.player.steps} | "
            f"Tapot: {game.player.kills} | "
            f"Juomat: {game.player.potions}"
        )
        print(stats)

    def _save_result(
        self, steps: int, kills: int, difficulty: str
    ):
        """Save the game result."""
        previous_best = self.score_repository.get_best_score()
        self.score_repository.save_score(steps, kills, difficulty)
        current_best = self.score_repository.get_best_score()

        if previous_best is None or (
            current_best is not None and current_best["steps"] < previous_best["steps"]
        ):
            print("Uusi paras tulos!")

    def _show_results(self):
        """Display saved game results with difficulty selection."""
        print("\n=== Tulokset ===")
        print("1) Kaikki tulokset")
        print("2) Helppo (Easy)")
        print("3) Normaali (Normal)")
        print("4) Vaikea (Hard)")
        choice = self._read_single_key("Valinta (1/2/3/4): ")

        if choice == "1":
            self._show_all_results()
        elif choice == "2":
            self._show_results_for_difficulty("easy")
        elif choice == "3":
            self._show_results_for_difficulty("normal")
        elif choice == "4":
            self._show_results_for_difficulty("hard")

    def _show_all_results(self):
        """Display all top 10 scores."""
        print("\n=== Kaikki tulokset (Top 10) ===")
        scores = self.score_repository.get_scores()
        if not scores:
            print("Ei tallennettuja tuloksia.")
            return

        best = scores[0]
        print(
            f"Paras tulos: {best['steps']} askelta, {best['kills']} tappoa "
            f"({best['difficulty']})"
        )
        print("Top 10:")
        for index, score in enumerate(scores, start=1):
            print(
                f"{index}. {score['steps']} askelta, {score['kills']} tappoa "
                f"({score['difficulty']})"
            )

    def _show_results_for_difficulty(self, difficulty: str):
        """Display top 10 scores for a specific difficulty."""
        print(f"\n=== {difficulty.capitalize()} - Top 10 ===")
        scores = self.score_repository.get_scores_by_difficulty(difficulty)
        if not scores:
            print(f"Ei tallennettuja tuloksia tasolla {difficulty}.")
            return

        for index, score in enumerate(scores, start=1):
            print(
                f"{index}. {score['steps']} askelta, {score['kills']} tappoa"
            )

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
