import pygame
import sys
from constants import *
from level import build_level, ENEMY_SPAWNS, ITEM_SPAWNS, COLS, FLAG_COL
from player import Player
from entities import Enemy, Item
from camera import Camera

FLAG_SCORE = 2000


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Super Mario")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 60)
        self.question_font = pygame.font.Font(None, 24)
        self.question_text = self.question_font.render("?", True, BLACK)
        self.running = True
        self.state = PLAYING

        self.stars = [(i * 37 % (COLS * TILE_SIZE), i * 13 % SCREEN_HEIGHT) for i in range(40)]
        self.flag_rect = None
        self._load_level()

    def _load_level(self):
        self.tiles = build_level()
        self.level_width = COLS * TILE_SIZE
        self.player = Player(80, 420)
        self.camera = Camera(self.level_width)

        self.enemies = [Enemy(col * TILE_SIZE, row * TILE_SIZE, etype)
                        for col, row, etype in ENEMY_SPAWNS]
        self.items = [Item(col * TILE_SIZE + TILE_SIZE // 4, row * TILE_SIZE, itype)
                      for col, row, itype in ITEM_SPAWNS]

        self.flag_rect = pygame.Rect(FLAG_COL * TILE_SIZE, 4 * TILE_SIZE,
                                     TILE_SIZE, 8 * TILE_SIZE)

    def run(self):
        while self.running:
            self.clock.tick(FPS)

            self._handle_events()

            if self.state == PLAYING:
                self._update()
                if self.player.rect.colliderect(self.flag_rect):
                    self.player.score += FLAG_SCORE
                    self.state = WON
                elif self.player.lives <= 0:
                    self.state = GAMEOVER

            self._render()

        pygame.quit()
        sys.exit()

    def _handle_events(self):
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.player.jump()
                elif event.key == pygame.K_r and self.state in (WON, GAMEOVER):
                    self.state = PLAYING
                    self._load_level()

        if self.state == PLAYING:
            if keys[pygame.K_LEFT]:
                self.player.move_left()
            elif keys[pygame.K_RIGHT]:
                self.player.move_right()
            else:
                self.player.stop()

    def _update(self):
        self.player.update(self.tiles, self.enemies, self.items)
        for enemy in self.enemies:
            enemy.update(self.tiles)
        for item in self.items:
            item.update()
        self.camera.update(self.player)

    def _render(self):
        self.screen.fill(SKY_BLUE)

        for sx, sy in self.stars:
            draw_x = (sx - self.camera.x * STAR_PARALLAX) % SCREEN_WIDTH
            pygame.draw.circle(self.screen, WHITE, (int(draw_x), int(sy)), 2)

        self._draw_tiles()
        for item in self.items:
            item.draw(self.screen, self.camera.x)
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera.x)
        self.player.draw(self.screen, self.camera.x)
        self._draw_hud()

        if self.state == WON:
            self._draw_overlay("YOU WIN!", WHITE)
        elif self.state == GAMEOVER:
            self._draw_overlay("GAME OVER", RED)

        pygame.display.flip()

    def _draw_tiles(self):
        for row in range(ROWS):
            for col in range(COLS):
                tile = self.tiles[row][col]
                if tile == AIR:
                    continue
                x = col * TILE_SIZE - self.camera.x
                y = row * TILE_SIZE
                if x + TILE_SIZE < 0 or x > SCREEN_WIDTH:
                    continue
                self._draw_tile(tile, x, y)

    def _draw_tile(self, tile, x, y):
        s = TILE_SIZE
        if tile == GROUND:
            pygame.draw.rect(self.screen, GROUND_BROWN, (x, y, s, s))
            pygame.draw.rect(self.screen, (0, 180, 0), (x, y, s, 4))
            pygame.draw.line(self.screen, (120, 70, 30), (x, y + s // 2), (x + s, y + s // 2), 1)
        elif tile == BRICK:
            pygame.draw.rect(self.screen, BRICK_ORANGE, (x, y, s, s))
            mid = s // 2
            pygame.draw.line(self.screen, BLACK, (x, y + mid), (x + s, y + mid), 1)
            pygame.draw.line(self.screen, BLACK, (x + mid, y), (x + mid, y + mid), 1)
            pygame.draw.line(self.screen, BLACK, (x + s // 4, y + mid), (x + s // 4, y + s), 1)
            pygame.draw.line(self.screen, BLACK, (x + 3 * s // 4, y + mid), (x + 3 * s // 4, y + s), 1)
        elif tile == QUESTION_BLOCK:
            pygame.draw.rect(self.screen, QUESTION_YELLOW, (x, y, s, s))
            pygame.draw.rect(self.screen, (180, 150, 0), (x, y, s, s), 2)
            self.screen.blit(self.question_text,
                             (x + s // 2 - self.question_text.get_width() // 2,
                              y + s // 2 - self.question_text.get_height() // 2))
        elif tile == QUESTION_BLOCK_USED:
            pygame.draw.rect(self.screen, (120, 90, 30), (x, y, s, s))
            pygame.draw.rect(self.screen, (80, 60, 20), (x, y, s, s), 2)
        elif tile in (PIPE_TOP_LEFT, PIPE_TOP_RIGHT):
            pygame.draw.rect(self.screen, PIPE_GREEN, (x, y, s, s))
            pygame.draw.rect(self.screen, PIPE_DARK_GREEN, (x, y, s, s), 2)
            pygame.draw.rect(self.screen, (100, 220, 100), (x + 2, y, s - 4, 6))
        elif tile in (PIPE_BODY_LEFT, PIPE_BODY_RIGHT):
            pygame.draw.rect(self.screen, PIPE_GREEN, (x, y, s, s))
            pygame.draw.rect(self.screen, PIPE_DARK_GREEN, (x, y, s, s), 2)
            if tile == PIPE_BODY_LEFT:
                pygame.draw.rect(self.screen, (100, 220, 100), (x + 2, y, 4, s))
            else:
                pygame.draw.rect(self.screen, (100, 220, 100), (x + s - 6, y, 4, s))
        elif tile == FLAG_POLE:
            pygame.draw.rect(self.screen, (120, 120, 120), (x + s // 2 - 3, y, 6, s))
        elif tile == FLAG_TOP:
            pygame.draw.rect(self.screen, (120, 120, 120), (x + s // 2 - 3, y, 6, s))
            points = [(x + s // 2 + 3, y), (x + s // 2 + 3 + s, y + s // 2), (x + s // 2 + 3, y + s)]
            pygame.draw.polygon(self.screen, FLAG_GREEN, points)

    def _draw_hud(self):
        p = self.player
        for i, (label, value) in enumerate([
            ("SCORE", p.score), ("COINS", p.coins),
            ("LIVES", p.lives), ("STATE", p.state.upper()),
        ]):
            text = self.font.render(f"{label}: {value}", True, WHITE)
            self.screen.blit(text, (20 + i * 180, 10))

    def _draw_overlay(self, title, color):
        shadow = self.big_font.render(title, True, BLACK)
        text = self.big_font.render(title, True, color)
        cx = SCREEN_WIDTH // 2 - text.get_width() // 2
        cy = SCREEN_HEIGHT // 2 - 24
        self.screen.blit(shadow, (cx + 2, cy + 2))
        self.screen.blit(text, (cx, cy))
        hint = self.font.render("Press R to play again", True, WHITE)
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, cy + 50))
