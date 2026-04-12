
# Arkkitehtuuri

```mermaid
classDiagram
    class ConsoleUI {
        +run()
        -_start_new_game()
        -_draw_game(game)
        -_read_single_key(prompt)
    }

    class Game {
        +map_rows
        +player: Player
        +enemies: list~Enemy~
        +is_running
        +is_won
        +tile_at(x, y)
        +enemy_at(x, y)
        +move_player(dx, dy)
        +handle_command(command)
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

    class game_map {
        +WALL
        +FLOOR
        +EXIT
        +DEFAULT_MAP
    }

    ConsoleUI ..> Game : käyttää
    Game "1" *-- "1" Player : omistaa
    Game "1" *-- "0..*" Enemy : hallitsee
    Game  ..>  game_map : riippuvuus
