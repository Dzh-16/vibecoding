import pygame
from constants import *
from physics import resolve_collision_x, resolve_collision_y


class Enemy:
    def __init__(self, x, y, enemy_type=GOOMBA):
        w = TILE_SIZE - 8
        h = TILE_SIZE - 8
        self.rect = pygame.Rect(x, y, w, h)
        self.enemy_type = enemy_type
        self.alive = True
        self.vel_x = -ENEMY_SPEED
        self.vel_y = 0
        self.squish_timer = 0

    def update(self, tiles):
        if not self.alive:
            self.squish_timer -= 1
            return

        self.vel_y += GRAVITY
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED

        self.rect.x += self.vel_x
        result = resolve_collision_x(self.rect, self.vel_x, tiles)
        if result != self.vel_x:
            self.vel_x = result  # Bounce off wall

        self.rect.y += self.vel_y
        self.vel_y, _ = resolve_collision_y(self.rect, self.vel_y, tiles)

        if self.rect.top > SCREEN_HEIGHT + 100:
            self.alive = False

    def draw(self, screen, camera_x):
        if not self.alive and self.squish_timer <= 0:
            return

        x = self.rect.x - camera_x
        y = self.rect.y

        if not self.alive:
            pygame.draw.rect(screen, GOOMBA_BROWN, (x, y + TILE_SIZE // 2 - 4, TILE_SIZE - 8, 6))
            return

        if self.enemy_type == GOOMBA:
            self._draw_goomba(screen, x, y)
        elif self.enemy_type == KOOPA:
            self._draw_koopa(screen, x, y)

    def _draw_goomba(self, screen, x, y):
        pygame.draw.ellipse(screen, GOOMBA_BROWN, (x, y, TILE_SIZE - 8, TILE_SIZE - 8))
        pygame.draw.rect(screen, WHITE, (x + 6, y + 6, 6, 6))
        pygame.draw.rect(screen, WHITE, (x + 18, y + 6, 6, 6))
        pygame.draw.rect(screen, BLACK, (x + 8, y + 8, 3, 3))
        pygame.draw.rect(screen, BLACK, (x + 20, y + 8, 3, 3))
        pygame.draw.rect(screen, BLACK, (x + 2, y + 22, 10, 6))
        pygame.draw.rect(screen, BLACK, (x + 18, y + 22, 10, 6))

    def _draw_koopa(self, screen, x, y):
        pygame.draw.rect(screen, (0, 180, 0), (x + 2, y + 10, TILE_SIZE - 12, TILE_SIZE - 14))
        pygame.draw.rect(screen, (0, 220, 0), (x + 18, y, 12, 14))
        pygame.draw.rect(screen, WHITE, (x + 22, y + 2, 5, 5))
        pygame.draw.rect(screen, BLACK, (x + 24, y + 3, 2, 2))
        pygame.draw.rect(screen, (255, 200, 0), (x + 4, y + 24, 8, 5))
        pygame.draw.rect(screen, (255, 200, 0), (x + 18, y + 24, 8, 5))


class Item:
    def __init__(self, x, y, item_type=COIN):
        w = TILE_SIZE // 2
        h = TILE_SIZE // 2
        if item_type == MUSHROOM:
            w = TILE_SIZE - 4
            h = TILE_SIZE - 4
        self.rect = pygame.Rect(x, y, w, h)
        self.item_type = item_type
        self.alive = True
        self.anim_timer = 0

    def update(self):
        self.anim_timer += 1

    def draw(self, screen, camera_x):
        if not self.alive:
            return

        x = self.rect.x - camera_x
        y = self.rect.y

        if self.item_type == COIN:
            r = TILE_SIZE // 2 - 4
            bounce = abs((self.anim_timer % 20) - 10) // 2
            pygame.draw.circle(screen, COIN_YELLOW, (x + r + 4, y + r - bounce + 4), r)
            pygame.draw.circle(screen, (200, 170, 0), (x + r + 4, y + r - bounce + 4), r, 1)
        elif self.item_type == MUSHROOM:
            pygame.draw.rect(screen, WHITE, (x + 8, y + 8, 16, 16))
            pygame.draw.ellipse(screen, MUSHROOM_RED, (x, y, TILE_SIZE - 4, TILE_SIZE - 12))
            pygame.draw.circle(screen, WHITE, (x + 8, y + 4), 4)
            pygame.draw.circle(screen, WHITE, (x + 22, y + 4), 4)
