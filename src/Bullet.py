"""
    Bullets fired by drons
"""
import random
from typing import Any, Tuple, Optional

import pygame
import settings
from math import sqrt

class Bullet:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8
        self.texture = settings.TEXTURES['dron1_bullet']
        
        self.move_speed = 120
        
        self.vx = 0
        self.vy = 0
        
        
        
    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def collides_with(self, another: Any) -> bool:
        return self.get_collision_rect().colliderect(another.get_collision_rect())

    def update(self, dt: float):
        self.x = self.x + self.vx * dt
        self.y = self.y + self.vy * dt
    
    def render(self, surface) -> None:
        surface.blit(
            self.texture, (self.x, self.y)
        )