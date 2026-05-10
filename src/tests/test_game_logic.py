from dungeon_game.game import Game, GameEvent, Difficulty
from dungeon_game.models.enemy import Enemy, create_enemy
from dungeon_game.models.potion import Potion


def test_player_spawn():
    game = Game()
    assert game.player.x == 1
    assert game.player.y == 1


def test_player_movement_right():
    game = Game()

    result = game.handle_command("d")
    assert result == GameEvent.NONE
    assert game.player.x == 2
    assert game.player.y == 1


def test_player_movement_down():
    game = Game()

    result = game.handle_command("s")
    assert result == GameEvent.NONE
    assert game.player.x == 1
    assert game.player.y == 2


def test_player_movement_into_wall():
    game = Game()

    result = game.handle_command("w")
    assert result == GameEvent.HIT_WALL
    assert game.player.x == 1
    assert game.player.y == 1


def test_player_movement_out_of_bounds():
    game = Game()

    game.handle_command("a")
    # Try moving left again to go out of bounds
    result = game.handle_command("a")
    assert result == GameEvent.HIT_WALL
    assert game.player.x == 0
    assert game.player.y == 1


def test_player_wins_game():
    game = Game()

    # Move down 4 times, right 8 (plus one to kill enemy) times and up once to reach the exit
    for _ in range(4):
        game.handle_command("s")
    for _ in range(10):
        game.handle_command("d")
    result = game.handle_command("w")

    assert result == GameEvent.EXIT_FOUND
    assert not game.is_running
    assert game.is_won


def test_invalid_command():
    game = Game()

    result = game.handle_command("x")
    assert result == GameEvent.INVALID_COMMAND
    assert game.player.x == 1
    assert game.player.y == 1


def test_quit_command():
    game = Game()

    result = game.handle_command("q")
    assert result == GameEvent.QUIT
    assert not game.is_running


def test_player_attacks_enemy_on_target_tile():
    game = Game()
    game.enemies = [Enemy(x=2, y=1, hp=2, damage=1)]

    result = game.handle_command("d")

    assert result == GameEvent.ENEMY_DEFEATED
    assert game.player.x == 1
    assert game.player.y == 1
    assert game.player.kills == 1
    assert len(game.enemies) == 0


def test_enemy_turn_attacks_when_adjacent_after_player_move():
    game = Game()
    game.enemies = [Enemy(x=3, y=1, hp=5, damage=1)]

    result = game.handle_command("d")

    assert result == GameEvent.ENEMY_HIT_PLAYER
    assert game.player.x == 2
    assert game.player.hp == 2


def test_player_picks_up_potion_when_moving_to_tile():
    game = Game()
    game.enemies = []
    game.potions = [Potion(x=2, y=1, heal_amount=4)]

    result = game.handle_command("d")

    assert result == GameEvent.POTION_PICKED_UP
    assert game.player.x == 2
    assert game.player.y == 1
    assert game.player.potions == 1
    assert len(game.potions) == 0


def test_player_uses_potion_and_heals():
    game = Game()
    game.player.hp = 1
    game.player.potions = 1

    result = game.handle_command("u")

    assert result == GameEvent.POTION_USED
    assert game.player.hp == 3
    assert game.player.potions == 0


def test_using_potion_without_inventory_fails():
    game = Game()

    result = game.handle_command("u")

    assert result == GameEvent.NO_POTION_AVAILABLE
    assert game.player.potions == 0


def test_easy_difficulty_has_fewer_enemies():
    game = Game(Difficulty.EASY)
    assert len(game.enemies) == 1


def test_normal_difficulty_has_standard_enemies():
    game = Game(Difficulty.NORMAL)
    assert len(game.enemies) == 3


def test_hard_difficulty_has_more_enemies():
    game = Game(Difficulty.HARD)
    assert len(game.enemies) == 16


def test_goblin_has_lower_hp_than_orc():
    goblin = create_enemy("goblin", 0, 0)
    orc = create_enemy("orc", 0, 0)

    assert goblin.hp < orc.hp
    assert goblin.damage == orc.damage
    assert goblin.symbol == "e"
    assert orc.symbol == "E"


def test_easy_difficulty_contains_goblins():
    game = Game(Difficulty.EASY)
    goblin_count = sum(1 for e in game.enemies if e.enemy_type == "goblin")
    assert goblin_count == 1


def test_hard_difficulty_contains_mix_of_enemies():
    game = Game(Difficulty.HARD)
    orc_count = sum(1 for e in game.enemies if e.enemy_type == "orc")
    goblin_count = sum(1 for e in game.enemies if e.enemy_type == "goblin")
    assert orc_count == 10
    assert goblin_count == 6


def test_player_heals_from_defeating_goblin():
    game = Game()
    game.enemies = [create_enemy("goblin", 2, 1)]
    game.player.hp = 2

    result = game.handle_command("d")

    assert result == GameEvent.ENEMY_DEFEATED
    assert game.player.hp == 3  # 2 + 1 from goblin defeat
    assert len(game.enemies) == 0


def test_player_heals_from_defeating_orc():
    game = Game()
    game.enemies = [create_enemy("orc", 2, 1)]
    game.player.hp = 3

    game.handle_command("d") # Player hp drops to 2
    game.handle_command("d") # Player hp drops to 1
    game.player.hp += 1 # Simulate using a potion so player won't die
    result = game.handle_command("d") # Player hp drops to 1

    assert result == GameEvent.ENEMY_DEFEATED
    assert game.player.hp == 3  # 1 + 2 from orc defeat
    assert len(game.enemies) == 0


def test_player_heal_doesnt_exceed_max_hp():
    game = Game()
    game.enemies = [create_enemy("orc", 2, 1)]
    game.player.hp = 3

    game.handle_command("d") # Player hp drops to 2
    game.player.hp += 1 # Simulate using a potion
    game.handle_command("d") # Player hp drops to 2
    game.player.hp += 1 # Simulate using a potion
    result = game.handle_command("d") # Player hp drops to 2

    assert result == GameEvent.ENEMY_DEFEATED
    assert game.player.hp == 3  # Max hp is 3, so + 2 won't result in 4

def test_player_dies():
    game = Game()
    game.enemies = [Enemy(x=2, y=1, hp=5, damage=3)]
    game.player.hp = 1
    result = game.handle_command("d")
    assert result == GameEvent.PLAYER_DIED_IN_COMBAT
    assert not game.is_running
    assert not game.is_won

def test_player_dies_from_enemy_turn():
    game = Game()
    game.enemies = [Enemy(x=2, y=2, hp=5, damage=3)]
    game.player.hp = 1
    result = game.handle_command("d")
    assert result == GameEvent.PLAYER_DIED_IN_COMBAT
    assert not game.is_running
    assert not game.is_won