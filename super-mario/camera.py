from constants import *


class Camera:
    def __init__(self, level_width):
        self.x = 0
        self.level_width = level_width

    def update(self, player):
        target_x = player.rect.centerx - SCREEN_WIDTH // 3
        target_x = max(0, min(target_x, self.level_width - SCREEN_WIDTH))
        self.x += (target_x - self.x) * CAMERA_SMOOTHING
        self.x = int(self.x)
