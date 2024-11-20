import random
from math import sqrt
from typing import Any, Tuple, Optional
import pygame
import settings

from src.Laser import Laser
from src.Boss_eye import Boss_eye

from gale.factory import Factory
from gale.timer import Timer

class Final_Boss:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.target_x = 0
        self.target_y = 0
        self.width = 64
        self.height = 64
        self.eye_x = self.x + 10
        self.eye_y = self.y + 26
        self.eye_width = 20
        self.eye_height = 50
        self.texture = settings.TEXTURES['finalboss']
        self.eye = Boss_eye(self.eye_x, self.eye_y)
        self.laser_factory = Factory(Laser)
        self.lasers = []
        self.is_shooting = False
        self.health = 50
        self.is_taking_damage = False
        self.health_barhit = settings.TEXTURES['HHIT']
        self.health_bar0 = settings.TEXTURES['H0']
        self.health_bar1 = settings.TEXTURES['H1']
        self.health_bar2 = settings.TEXTURES['H2']
        self.health_bar3 = settings.TEXTURES['H3']
        self.health_bar4 = settings.TEXTURES['H4']
        self.health_bar5 = settings.TEXTURES['H5']
        self.health_bar6 = settings.TEXTURES['H6']
        self.health_bar7 = settings.TEXTURES['H7']
        self.health_bar8 = settings.TEXTURES['H8']
        self.health_bar9 = settings.TEXTURES['H9']
        self.health_bar10 = settings.TEXTURES['H10']
        
        self.move_speed = 30
        
        
        self.vx = 0
        self.vy = 0
        Timer.every(6,
            lambda: self.shoot()
        )
        
        
    def pop(self):
        self.bullets.pop()
            
    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def get_eye_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.eye_x, self.eye_y, self.eye_width, self.eye_height)

    def pop(self):
        self.is_shooting = False
        self.lasers.pop()

    def not_taking_damage(self):
        self.health -= 1
        self.is_taking_damage = False

    def taking_damage(self):
        if not self.is_taking_damage:
            self.is_taking_damage = True
            Timer.after(0.25,
                        lambda: self.not_taking_damage()
                        )

    def charge(self):
        for laser in self.lasers:
            laser.charged = True
            pygame.mixer.Sound.play(settings.SOUNDS['laser_shoot'])
        Timer.after(2,
            lambda: self.pop() 
        )
    def shoot(self):
        if not self.is_shooting:
            self.is_shooting = True
            laser = self.laser_factory.create(self.x - settings.LASER_WIDTH + 30, self.y + settings.FINALBOSS_HEIGHT // 2 - settings.LASER_HEIGHT // 2+6)
            laser.charged = False
            self.lasers.append(laser)
            pygame.mixer.Sound.play(settings.SOUNDS['laser_charge'])
            Timer.after(2,
                        lambda: self.charge()
                        )
           
            
        
    
    def move(self, target_y):
        #calculo la posicion centrada del final boss respecto al centro de dron
        self.target_y = target_y + settings.ROBOT_HEIGHT/2 - settings.FINALBOSS_HEIGHT/2
        dy = self.target_y - self.y
        if dy > 1:
            self.vy = self.move_speed
        elif dy < -1:
            self.vy = -self.move_speed
        elif -2 < dy < 2:
            self.vy = 0 
            self.shoot()


    def update(self, dt: float):
        self.x = self.x + self.vx * dt
        self.y = self.y + self.vy * dt
        self.eye.vy = self.vy
        self.eye.update(dt)
        for laser in self.lasers:
            laser.vx = 0
            laser.vy = self.vy
            laser.update(dt)
        
    
    def render(self, surface) -> None:
        if self.is_shooting:
            for laser in self.lasers:
                laser.render(surface)
        surface.blit(
            self.texture, (self.x, self.y)
        )
        if self.is_taking_damage:
            surface.blit(
                self.health_barhit, (self.x, self.y-10)
            )
        

        else:
            if  0 <= self.health < 5:
                surface.blit(
                    self.health_bar0, (self.x, self.y-10)
                )

            if 5 <= self.health < 10:
                surface.blit(
                    self.health_bar1, (self.x, self.y-10)
                )

            if 10 <= self.health < 15:
                surface.blit(
                    self.health_bar2, (self.x, self.y-10)
                )

            if 15 <= self.health < 20:
                surface.blit(
                    self.health_bar3, (self.x, self.y-10)
                )

            if 20 <= self.health < 25:
                surface.blit(
                    self.health_bar4, (self.x, self.y-10)
                )

            if 25 <= self.health < 30:
                surface.blit(
                    self.health_bar5, (self.x, self.y-10)
                )

            if 30 <= self.health < 35:
                surface.blit(
                    self.health_bar6, (self.x, self.y-10)
                )

            if 35 <= self.health < 40:
                surface.blit(
                    self.health_bar7, (self.x, self.y-10)
                )

            if 40 <= self.health < 45:
                surface.blit(
                    self.health_bar8, (self.x, self.y-10)
                )

            if 45 <= self.health < 50:
                surface.blit(
                    self.health_bar9, (self.x, self.y-10)
                )

            if self.health == 50:
                surface.blit(
                    self.health_bar10, (self.x+2, self.y-10)
                )
        