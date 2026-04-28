"""Pygame user interface."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from dungeon_game.game import Game, GameEvent
from dungeon_game.repositories.score_repository import ScoreRepository


@dataclass(frozen=True)
class Colors:
    background: tuple[int, int, int] = (18, 18, 24)
    wall: tuple[int, int, int] = (70, 70, 90)
    floor: tuple[int, int, int] = (40, 40, 50)
    exit: tuple[int, int, int] = (30, 140, 80)
    player: tuple[int, int, int] = (80, 180, 255)
    enemy: tuple[int, int, int] = (220, 80, 80)
    potion: tuple[int, int, int] = (220, 180, 60)
    text: tuple[int, int, int] = (240, 240, 240)
    message: tuple[int, int, int] = (220, 220, 160)
    button: tuple[int, int, int] = (60, 60, 80)
    button_hover: tuple[int, int, int] = (90, 90, 120)


class PygameUI:
    EVENT_MESSAGES = {
        GameEvent.HIT_WALL: "Törmäsit seinään.",
        GameEvent.EXIT_FOUND: "Löysit uloskäynnin!",
        GameEvent.QUIT: "Poistuit pelistä.",
        GameEvent.GAME_ALREADY_OVER: "Peli on jo päättynyt.",
        GameEvent.INVALID_COMMAND: "Tuntematon komento. Käytä: W, A, S, D, U tai Q.",
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
        pygame.init()
        self.colors = Colors()
        self.score_repository = ScoreRepository()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)
        self.small_font = pygame.font.SysFont("arial", 20)
        self.title_font = pygame.font.SysFont("arial", 36, bold=True)
        self.cell_size = 44
        self.margin = 20
        self.hud_height = 120
        self.menu_width = 720
        self.menu_height = 520
        self.game: Game | None = None
        self.state = "menu"
        self.message = ""
        self.best_scores = self.score_repository.get_scores()
        self.screen = pygame.display.set_mode((self.menu_width, self.menu_height))
        pygame.display.set_caption("Luolastopeli")

    def run(self):
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif self.state == "menu":
                    self._handle_menu_event(event)
                elif self.state == "game":
                    self._handle_game_event(event)
                elif self.state == "results":
                    self._handle_results_event(event)
                elif self.state == "game_over":
                    self._handle_game_over_event(event)

            self._render()
            self.clock.tick(60)

        pygame.quit()

    def _handle_menu_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_1:
            self.game = Game()
            self.message = ""
            self.state = "game"
        elif event.key == pygame.K_2:
            self.best_scores = self.score_repository.get_scores()
            self.state = "results"
        elif event.key == pygame.K_3 or event.key == pygame.K_ESCAPE:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def _handle_results_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE, pygame.K_RETURN):
            self.state = "menu"

    def _handle_game_over_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                self.state = "menu"
            elif event.key == pygame.K_1:
                self.game = Game()
                self.message = ""
                self.state = "game"

    def _handle_game_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN or self.game is None:
            return

        key_map = {
            pygame.K_w: "w",
            pygame.K_a: "a",
            pygame.K_s: "s",
            pygame.K_d: "d",
            pygame.K_u: "u",
            pygame.K_q: "q",
        }
        command = key_map.get(event.key)
        if command is None:
            return

        game_event = self.game.handle_command(command)
        self.message = self.EVENT_MESSAGES.get(game_event, "")

        if self.game.is_won:
            self._save_result(self.game.player.steps, self.game.player.kills)
            self.state = "game_over"
        elif not self.game.is_running:
            self.state = "game_over"

    def _render(self) -> None:
        if self.state == "menu":
            self._render_menu()
        elif self.state == "results":
            self._render_results()
        elif self.state == "game" and self.game is not None:
            self._render_game()
        elif self.state == "game_over" and self.game is not None:
            self._render_game_over()

        pygame.display.flip()

    def _ensure_menu_mode(self) -> None:
        if self.screen.get_size() != (self.menu_width, self.menu_height):
            self.screen = pygame.display.set_mode((self.menu_width, self.menu_height))

    def _render_menu(self) -> None:
        self._ensure_menu_mode()
        self.screen.fill(self.colors.background)
        self._draw_text("Luolastopeli", self.title_font, self.colors.text, (self.menu_width // 2, 70), center=True)
        self._draw_text("1  Uusi peli", self.font, self.colors.text, (self.menu_width // 2, 180), center=True)
        self._draw_text("2  Tulokset", self.font, self.colors.text, (self.menu_width // 2, 230), center=True)
        self._draw_text("3  Lopeta", self.font, self.colors.text, (self.menu_width // 2, 280), center=True)
        self._draw_text("Ohjaus pelissä: W A S D, U = käytä juoma, Q = lopeta", self.small_font, self.colors.message, (self.menu_width // 2, 360), center=True)

    def _render_results(self) -> None:
        self._ensure_menu_mode()
        self.screen.fill(self.colors.background)
        self._draw_text("Tallennetut tulokset", self.title_font, self.colors.text, (self.menu_width // 2, 50), center=True)
        if not self.best_scores:
            self._draw_text("Ei tallennettuja tuloksia.", self.font, self.colors.text, (self.menu_width // 2, 160), center=True)
        else:
            best = self.best_scores[0]
            self._draw_text(
                f"Paras tulos: {best['steps']} askelta, {best['kills']} tappoa",
                self.font,
                self.colors.text,
                (self.menu_width // 2, 130),
                center=True,
            )
            for index, score in enumerate(self.best_scores[:10], start=1):
                self._draw_text(
                    f"{index}. {score['steps']} askelta, {score['kills']} tappoa",
                    self.font,
                    self.colors.text,
                    (self.menu_width // 2, 170 + index * 32),
                    center=True,
                )
        self._draw_text("Palaa takaisin painamalla Enter, Esc tai Backspace", self.small_font, self.colors.message, (self.menu_width // 2, 470), center=True)

    def _render_game(self) -> None:
        assert self.game is not None
        map_width = self.game.width * self.cell_size + self.margin * 2
        map_height = self.game.height * self.cell_size + self.margin * 2 + self.hud_height
        if self.screen.get_width() != map_width or self.screen.get_height() != map_height:
            self.screen = pygame.display.set_mode((map_width, map_height))

        self.screen.fill(self.colors.background)
        for y, row in enumerate(self.game.map_rows):
            for x, tile in enumerate(row):
                rect = pygame.Rect(self.margin + x * self.cell_size, self.margin + y * self.cell_size, self.cell_size, self.cell_size)
                color = self._tile_color(tile)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (25, 25, 35), rect, 1)

                enemy = self.game.enemy_at(x, y)
                potion = self.game.potion_at(x, y)
                if x == self.game.player.x and y == self.game.player.y:
                    pygame.draw.circle(self.screen, self.colors.player, rect.center, self.cell_size // 3)
                elif enemy is not None:
                    pygame.draw.circle(self.screen, self.colors.enemy, rect.center, self.cell_size // 3)
                    self._draw_text(enemy.symbol, self.small_font, self.colors.text, rect.center, center=True)
                elif potion is not None:
                    pygame.draw.circle(self.screen, self.colors.potion, rect.center, self.cell_size // 4)
                    self._draw_text(potion.symbol, self.small_font, self.colors.background, rect.center, center=True)

        hud_y = self.margin + self.game.height * self.cell_size + 10
        self._draw_text(
            f"HP: {self.game.player.hp}/{self.game.player.max_hp}  Askeleet: {self.game.player.steps}  Tapot: {self.game.player.kills}  Juomat: {self.game.player.potions}",
            self.small_font,
            self.colors.text,
            (self.margin, hud_y),
        )
        self._draw_text(
            "W/A/S/D liikkuminen, U juoma, Q takaisin valikkoon",
            self.small_font,
            self.colors.message,
            (self.margin, hud_y + 32),
        )
        if self.message:
            self._draw_text(self.message, self.small_font, self.colors.message, (self.margin, hud_y + 62))

    def _render_game_over(self) -> None:
        assert self.game is not None
        self._render_game()
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))
        title = "Voitit pelin!" if self.game.is_won else "Peli päättyi"
        self._draw_text(title, self.title_font, self.colors.text, (self.screen.get_width() // 2, 120), center=True)
        self._draw_text(f"Askeleet: {self.game.player.steps}", self.font, self.colors.text, (self.screen.get_width() // 2, 190), center=True)
        self._draw_text(f"Tapot: {self.game.player.kills}", self.font, self.colors.text, (self.screen.get_width() // 2, 225), center=True)
        self._draw_text("Enter tai Esc valikkoon", self.small_font, self.colors.message, (self.screen.get_width() // 2, 300), center=True)

    def _draw_text(self, text: str, font: pygame.font.Font, color: tuple[int, int, int], position: tuple[int, int], *, center: bool = False) -> None:
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        if center:
            rect.center = position
        else:
            rect.topleft = position
        self.screen.blit(surface, rect)

    def _tile_color(self, tile: str) -> tuple[int, int, int]:
        if tile == "#":
            return self.colors.wall
        if tile == "X":
            return self.colors.exit
        return self.colors.floor

    def _save_result(self, steps: int, kills: int) -> None:
        previous_best = self.score_repository.get_best_score()
        self.score_repository.save_score(steps, kills)
        current_best = self.score_repository.get_best_score()
        if previous_best is None or (current_best is not None and current_best["steps"] < previous_best["steps"]):
            self.message = "Uusi paras tulos!"
