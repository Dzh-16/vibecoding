from constants import *

GROUND_ROWS = range(12, 15)
GAPS = [(35, 38), (68, 71), (115, 118)]
FLAG_COL = 190


def make_empty_level():
    return [[AIR for _ in range(COLS)] for _ in range(ROWS)]


def _place_pipe(grid, col, top_row):
    grid[top_row][col] = PIPE_TOP_LEFT
    grid[top_row][col + 1] = PIPE_TOP_RIGHT
    grid[top_row + 1][col] = PIPE_BODY_LEFT
    grid[top_row + 1][col + 1] = PIPE_BODY_RIGHT
    grid[top_row + 2][col] = PIPE_BODY_LEFT
    grid[top_row + 2][col + 1] = PIPE_BODY_RIGHT


def _place_staircase(grid, start_col, steps):
    for i in range(steps):
        for row in range(11 - i, 12):
            grid[row][start_col + i] = BRICK


def build_level():
    grid = make_empty_level()

    for row in GROUND_ROWS:
        for col in range(COLS):
            if any(g[0] <= col <= g[1] for g in GAPS):
                continue
            grid[row][col] = GROUND

    # Floating brick platform
    for col in range(20, 25):
        grid[10][col] = BRICK

    # Question blocks with bricks
    for col in range(30, 34):
        grid[10][col] = BRICK
        grid[9][col] = QUESTION_BLOCK

    # Brick staircases
    _place_staircase(grid, 45, 4)
    _place_staircase(grid, 130, 4)

    # Pipes
    _place_pipe(grid, 55, 10)
    _place_pipe(grid, 95, 10)
    _place_pipe(grid, 150, 10)

    # Floating bricks
    for col in range(60, 63):
        grid[9][col] = BRICK
    grid[10][61] = QUESTION_BLOCK

    # Elevated platform
    for col in range(80, 86):
        grid[10][col] = BRICK
    grid[9][82] = QUESTION_BLOCK

    # Floating question blocks
    for col in range(100, 103):
        grid[9][col] = QUESTION_BLOCK

    # Flagpole
    for row in range(5, 12):
        grid[row][FLAG_COL] = FLAG_POLE
    grid[4][FLAG_COL] = FLAG_TOP

    return grid


ENEMY_SPAWNS = [
    (15, 11, GOOMBA),
    (28, 11, GOOMBA),
    (42, 11, GOOMBA),
    (58, 11, GOOMBA),
    (75, 11, GOOMBA),
    (88, 11, GOOMBA),
    (106, 11, GOOMBA),
    (125, 11, KOOPA),
    (140, 11, GOOMBA),
    (160, 11, GOOMBA),
]

ITEM_SPAWNS = [
    (21, 9, COIN),
    (22, 9, COIN),
    (23, 9, COIN),
    (31, 8, COIN),
    (32, 8, COIN),
    (33, 8, COIN),
    (61, 8, COIN),
    (101, 8, COIN),
    (102, 8, COIN),
    (9, 11, MUSHROOM),
]
