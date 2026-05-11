import pygame
from constants import *


def get_tile_bounds(rect):
    """Return the row/col range of tiles overlapping a rect."""
    start_col = max(0, rect.left // TILE_SIZE)
    end_col = min(COLS, rect.right // TILE_SIZE + 1)
    start_row = max(0, rect.top // TILE_SIZE)
    end_row = min(ROWS, rect.bottom // TILE_SIZE + 1)
    return start_col, end_col, start_row, end_row


def resolve_collision_x(rect, vel_x, tiles):
    """Resolve horizontal tile collisions. Returns new vel_x (bounce or stop)."""
    sc, ec, sr, er = get_tile_bounds(rect)
    for row in range(sr, er):
        for col in range(sc, ec):
            tile = tiles[row][col]
            if tile == AIR:
                continue
            tile_rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if rect.colliderect(tile_rect):
                if vel_x > 0:
                    rect.right = tile_rect.left
                else:
                    rect.left = tile_rect.right
                return -vel_x
    return vel_x


def resolve_collision_y(rect, vel_y, tiles, on_land=None, on_bump=None):
    """Resolve vertical tile collisions. Returns (new_vel_y, on_ground).
       on_land is called when landing on a tile.
       on_bump(col, row) is called when hitting a tile from below."""
    sc, ec, sr, er = get_tile_bounds(rect)
    on_ground = False
    for row in range(sr, er):
        for col in range(sc, ec):
            tile = tiles[row][col]
            if tile == AIR:
                continue
            tile_rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if rect.colliderect(tile_rect):
                if vel_y > 0:
                    rect.bottom = tile_rect.top
                    vel_y = 0
                    on_ground = True
                    if on_land:
                        on_land(col, row, tile)
                elif vel_y < 0:
                    rect.top = tile_rect.bottom
                    vel_y = 0
                    if on_bump:
                        on_bump(col, row, tile)
    return vel_y, on_ground
