import pygame
from constants import *
from physics import resolve_collision_x, resolve_collision_y

STOMP_BOUNCE = -8
STOMP_SCORE = 200
COIN_SCORE = 100
MUSHROOM_SCORE = 1000
INVINCIBILITY_FRAMES = 90
DEATH_MARGIN = 100


class Player:
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(self.start_x, self.start_y, TILE_SIZE - 4, TILE_SIZE - 2)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.state = SMALL
        self.facing_right = True
        self.invincible_timer = 0
        self.lives = 3
        self.score = 0
        self.coins = 0

    def update(self, tiles, enemies, items):
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        self.rect.x += self.vel_x
        result = resolve_collision_x(self.rect, self.vel_x, tiles)
        if result != self.vel_x:
            self.vel_x = 0

        self.vel_y += GRAVITY
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED
        self.rect.y += self.vel_y

        self.vel_y, self.on_ground = resolve_collision_y(
            self.rect, self.vel_y, tiles,
            on_bump=lambda col, row, tile: self._on_bump(col, row, tile, tiles))

        for enemy in enemies:
            if not enemy.alive:
                continue
            if self.rect.colliderect(enemy.rect):
                if self.vel_y > 0 and self.rect.bottom < enemy.rect.centery:
                    enemy.alive = False
                    self.vel_y = STOMP_BOUNCE
                    self.score += STOMP_SCORE
                elif self.invincible_timer == 0:
                    self.take_damage()

        for item in items:
            if not item.alive:
                continue
            if self.rect.colliderect(item.rect):
                item.alive = False
                if item.item_type == COIN:
                    self.coins += 1
                    self.score += COIN_SCORE
                elif item.item_type == MUSHROOM:
                    if self.state == SMALL:
                        self.state = BIG
                        self.rect.y -= TILE_SIZE
                        self.rect.height = TILE_SIZE * 2 - 4
                    self.score += MUSHROOM_SCORE

        if self.rect.top > SCREEN_HEIGHT + DEATH_MARGIN:
            self.die()

    def _on_bump(self, col, row, tile, tiles):
        if tile == QUESTION_BLOCK:
            tiles[row][col] = QUESTION_BLOCK_USED
            self.coins += 1
            self.score += COIN_SCORE

    def jump(self):
        if self.on_ground:
            self.vel_y = PLAYER_JUMP

    def move_left(self):
        self.vel_x = -PLAYER_SPEED
        self.facing_right = False

    def move_right(self):
        self.vel_x = PLAYER_SPEED
        self.facing_right = True

    def stop(self):
        self.vel_x = 0

    def take_damage(self):
        if self.state == BIG:
            self.state = SMALL
            self.rect.y += TILE_SIZE
            self.rect.height = TILE_SIZE - 2
            self.invincible_timer = INVINCIBILITY_FRAMES
        elif self.state == FIRE:
            self.state = BIG
            self.invincible_timer = INVINCIBILITY_FRAMES
        else:
            self.die()

    def die(self):
        self.lives -= 1
        if self.lives > 0:
            self.reset()

    def draw(self, screen, camera_x):
        x = self.rect.x - camera_x
        y = self.rect.y

        if self.invincible_timer > 0 and (self.invincible_timer // 5) % 2 == 0:
            return

        if self.state == SMALL:
            self._draw_small(screen, x, y)
        else:
            self._draw_big(screen, x, y)

    def _draw_small(self, screen, x, y):
        pygame.draw.rect(screen, MARIO_RED, (x + 8, y, 20, 8))
        pygame.draw.rect(screen, MARIO_SKIN, (x + 8, y + 8, 20, 10))
        pygame.draw.rect(screen, MARIO_RED, (x + 6, y + 18, 24, 10))
        pygame.draw.rect(screen, (0, 0, 180), (x + 6, y + 28, 24, 8))
        pygame.draw.rect(screen, MARIO_BROWN, (x + 8, y + 36, 8, 4))
        pygame.draw.rect(screen, MARIO_BROWN, (x + 20, y + 36, 8, 4))

    def _draw_big(self, screen, x, y):
        pygame.draw.rect(screen, MARIO_RED, (x + 6, y, 24, 10))
        pygame.draw.rect(screen, MARIO_SKIN, (x + 6, y + 10, 24, 14))
        pygame.draw.rect(screen, MARIO_RED, (x + 4, y + 24, 28, 14))
        pygame.draw.rect(screen, MARIO_SKIN, (x, y + 22, 8, 16))
        pygame.draw.rect(screen, MARIO_SKIN, (x + 28, y + 22, 8, 16))
        pygame.draw.rect(screen, (0, 0, 180), (x + 4, y + 38, 28, 12))
        pygame.draw.rect(screen, MARIO_BROWN, (x + 6, y + 50, 10, 12))
        pygame.draw.rect(screen, MARIO_BROWN, (x + 20, y + 50, 10, 12))
        pygame.draw.rect(screen, MARIO_BROWN, (x + 4, y + 62, 12, 6))
        pygame.draw.rect(screen, MARIO_BROWN, (x + 20, y + 62, 12, 6))
