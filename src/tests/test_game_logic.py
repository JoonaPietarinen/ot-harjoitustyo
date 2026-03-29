from dungeon_game.game import Game

def test_player_spawn():
    game = Game()
    assert game.player.x == 1
    assert game.player.y == 1

def test_player_movement_right():
    game = Game()

    result = game.handle_command("d")
    assert result is None
    assert game.player.x == 2
    assert game.player.y == 1

def test_player_movement_down():
    game = Game()

    result = game.handle_command("s")
    assert result is None
    assert game.player.x == 1
    assert game.player.y == 2

def test_player_movement_into_wall():
    game = Game()

    result = game.handle_command("w")
    assert result == "Törmäsit seinään."
    assert game.player.x == 1
    assert game.player.y == 1

def test_player_movement_out_of_bounds():
    game = Game()

    result = game.handle_command("a")
    result = game.handle_command("a")  # Try moving left again to go out of bounds
    assert result == "Törmäsit seinään."
    assert game.player.x == 0
    assert game.player.y == 1

def test_player_wins_game():
    game = Game()

    # Move down 4 times, right 8 times and up once to reach the exit
    for _ in range(4):
        game.handle_command("s")
    for _ in range(8):
        game.handle_command("d")
    game.handle_command("w")

    assert not game.is_running
    assert game.is_won

def test_invalid_command():
    game = Game()

    result = game.handle_command("x")
    assert result == "Tuntematon komento. Käytä: w, a, s, d tai q."
    assert game.player.x == 1
    assert game.player.y == 1

def test_quit_command():
    game = Game()

    result = game.handle_command("q")
    assert result == "Poistuit pelistä."
    assert not game.is_running