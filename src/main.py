import sys
from dungeon_game.ui import ConsoleUI

force_console = "--no-pygame" in sys.argv

if not force_console:
    try:
        from dungeon_game.pygame_ui import PygameUI
    except ImportError:
        PygameUI = None
else:
    PygameUI = None

def main():
    ui = PygameUI() if PygameUI is not None else ConsoleUI()
    ui.run()


if __name__ == "__main__":
    main()
