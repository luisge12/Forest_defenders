from typing import Any, Tuple, Optional

import pygame
import settings
from math import sqrt
from gale.timer import Timer

class Laser:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = settings.LASER_WIDTH
        self.height = settings.LASER_HEIGHT
        self.charging = settings.TEXTURES['blue_laser']
        self.shooting = settings.TEXTURES['red_laser']
        self.charged = False

        
        self.move_speed = 120
        
        self.vx = 0
        self.vy = 30
        
    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def collides_with(self, another: Any) -> bool:
        return self.get_collision_rect().colliderect(another.get_collision_rect())

    def update(self, dt: float):
        self.x = self.x + self.vx * dt
        self.y = self.y + self.vy * dt
    
    def render(self, surface) -> None:
        if not self.charged:
            surface.blit(
                self.charging, (self.x, self.y)
            )

        if self.charged:
            surface.blit(
                self.shooting, (self.x, self.y)
            )