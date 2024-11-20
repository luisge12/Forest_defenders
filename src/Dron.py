"""
    Drones que quieren apoderarse del bosque junto con los robots    
"""
import random
from math import sqrt
from typing import Any, Tuple, Optional

import pygame
import settings

from src.Bullet import Bullet

from gale.factory import Factory
from gale.timer import Timer

class Dron:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.target_x = 0
        self.target_y = 0
        self.width = 37
        self.height = 30
        self.range_radius = 150
        self.texture = settings.TEXTURES['dron1']
        self.bullet_factory = Factory(Bullet)
        self.bullets = []
        self.is_shooting = False
        
        self.move_speed = 80
        
        
        self.vx = 0
        self.vy = 0
        
        
    def pop(self):
        if self.is_shooting:
            self.is_shooting = False
            self.bullets.pop()
            
    def get_collision_rect(self) -> pygame.Rect:        
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def shoot(self, target_x, target_y):
        if not self.is_shooting:
            self.is_shooting = True
            bullet = self.bullet_factory.create(self.x + settings.DRON_WIDTH // 2, self.y + settings.DRON_HEIGHT // 2)
            targetx = target_x
            targety = target_y
            dy = targety - self.y
            dx = targetx - self.x
            d = sqrt(dx*dx + dy*dy)
            bullet.vx = dx/d * bullet.move_speed
            bullet.vy = dy/d * bullet.move_speed
            self.bullets.append(bullet)
            
            Timer.after(
                3,
                lambda: self.pop()
            )
            
        
    
    def move(self, target_x, target_y):
        dy = target_y - self.y
        dx = target_x - self.x
        d = sqrt(dx*dx + dy*dy)
        self.vx = dx/d * self.move_speed
        self.vy = dy/d * self.move_speed


    def update(self, dt: float):
        self.x = self.x + self.vx * dt
        self.y = self.y + self.vy * dt
        
        
        for bullet in self.bullets:
            
            if bullet.x<0 or bullet.x>settings.MAP_WIDTH or bullet.y<0 or bullet.y>settings.MAP_HEIGHT:
                self.bullets.pop()
                self.is_shooting = False
    
    def render(self, surface) -> None:
        surface.blit(
            self.texture, (self.x, self.y)
        )
        