from math import sqrt
from typing import Any, Tuple, Optional
import pygame
import settings

from src.Laser import Laser

from gale.timer import Timer

class Boss_eye:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.target_x = 0
        self.target_y = 0
        self.width = 20
        self.height = 50
        
        self.move_speed = 30
        self.vx = 0
        self.vy = 0
            
    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)
   

    def update(self, dt: float):
        self.x = self.x + self.vx * dt
        self.y = self.y + self.vy * dt

        