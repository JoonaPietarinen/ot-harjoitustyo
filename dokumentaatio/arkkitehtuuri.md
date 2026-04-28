# Arkkitehtuuri

```mermaid
classDiagram
    class ConsoleUI {
        +run()
        -_start_new_game()
        -_draw_game(game)
        -_read_single_key(prompt)
    }

    class PygameUI {
        +run()
        -_handle_menu_event(event)
        -_handle_game_event(event)
        -_render()
        -_render_menu()
        -_render_game()
        -_render_results()
        -_render_game_over()
    }

    class GameEvent {
        <<enumeration>>
    }

    class ScoreRepository {
        +get_scores(limit)
        +get_best_score()
        +save_score(steps)
    }

    class Game {
        +map_rows
        +player: Player
        +enemies: list~Enemy~
        +potions: list~Potion~
        +is_running
        +is_won
        +tile_at(x, y)
        +enemy_at(x, y)
        +potion_at(x, y)
        +move_player(dx, dy)
        +handle_command(command)
        +use_potion()
        -_resolve_player_attack(enemy)
        -_enemy_turn()
    }

    class Player {
        +x
        +y
        +hp
        +max_hp
        +steps
        +damage
        +kills
        +potions
    }

    class Enemy {
        +x
        +y
        +hp
        +damage
        +symbol
        +is_alive
        +take_damage(amount)
    }

    class Potion {
        +x
        +y
        +heal_amount
        +symbol
    }

    class game_map {
        +WALL
        +FLOOR
        +EXIT
        +DEFAULT_MAP
    }

    ConsoleUI ..> Game : käyttää
    ConsoleUI ..> GameEvent : mapittaa viesteiksi
    ConsoleUI ..> ScoreRepository : tallentaa tulokset
    PygameUI ..> Game : käyttää
    PygameUI ..> GameEvent : mapittaa viesteiksi
    PygameUI ..> ScoreRepository : tallentaa tulokset
    Game "1" *-- "1" Player : omistaa
    Game "1" *-- "0..*" Enemy : hallitsee
    Game "1" *-- "0..*" Potion : hallitsee
    Game ..> game_map : riippuu kartoista
