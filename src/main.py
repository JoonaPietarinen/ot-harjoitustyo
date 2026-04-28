from dungeon_game.ui import ConsoleUI

try:
    from dungeon_game.pygame_ui import PygameUI
except ImportError:  # pragma: no cover - fallback when pygame is unavailable.
    PygameUI = None


def main():
    ui = PygameUI() if PygameUI is not None else ConsoleUI()
    ui.run()


if __name__ == "__main__":
    main()
