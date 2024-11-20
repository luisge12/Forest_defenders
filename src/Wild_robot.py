import random
from math import sqrt
from typing import Any, Tuple, Optional

import pygame
import settings

from src.Bullet import Bullet

from gale.factory import Factory
from gale.timer import Timer

class Wild_robot:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = 38
        self.height = 40
        self.target_x = None
        self.target_y = None
        self.range_radius = 1
        self.texture = settings.TEXTURES['wild_robot']
        self.shield_texture = settings.TEXTURES['shield']
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
        self.hand1 = Bullet(self.x + 2,self.y + 30)
        self.hand2 = Bullet(self.x + 35,self.y + 30)
        self.has_hand1 = True
        self.has_hand2 = True
        self.hand_range = 200
        self.hands = [self.hand1, self.hand2]
        self.health = 10 
        self.move_speed = 50
        self.has_shield = False
        self.is_taking_damage = False
        
        self.vx = 0
        self.vy = 0
        
            
    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)
       
    def not_taking_damage(self):
        self.health -= 1
        self.is_taking_damage = False

    def taking_damage(self):
        if not self.is_taking_damage:
            self.is_taking_damage = True
            Timer.after(0.25,
                        lambda: self.not_taking_damage()
                        )
             
    def recharging1(self):
        if not self.has_hand1:
            self.has_hand1 = True
            
    def recharging2(self):
        if not self.has_hand2:
            self.has_hand2 = True

    def hand_back(self):
        Timer.tween( 
                0.4,
                [
                    (self.hand1, {"x": self.x + 2, "y": self.y + 20})
                ],
                on_finish = lambda: self.recharging1()
        )

    def hand2_back(self):
        Timer.tween( 
            0.4,
            [
                (self.hand2, {"x": self.x + 32 , "y": self.y + 20})
            ],
            on_finish = lambda: self.recharging2()
        )     
    def propellants_hands(self, target_x, target_y):
        if self.has_hand2 and not self.has_hand1:
            target_x2 = target_x / 2
            target_y2 = target_y / 2
            dy2 = target_y2 - self.y
            dx2 = target_x2 - self.x
            d2 = sqrt(dx2*dx2 + dy2*dy2)  
            final_x2 = dx2/d2 * self.hand_range + self.x
            final_y2 = dy2/d2 * self.hand_range + self.y
            self.has_hand2 = False
            
            Timer.tween( 
                    0.4,
                    [
                        (self.hand2, {"x": final_x2, "y": final_y2})
                    ],
                    on_finish = lambda: self.hand2_back(),
            )
            
        if self.has_hand1:
            target_x1 = target_x / 2
            target_y1 = target_y / 2
            dy = target_y1 - self.y
            dx = target_x1 - self.x
            d = sqrt(dx*dx + dy*dy) 
            final_x1 = dx/d * self.hand_range + self.x
            final_y1 = dy/d * self.hand_range + self.y
            self.has_hand1 = False
            Timer.tween( 
                    0.4,
                    [
                        (self.hand1, {"x": final_x1, "y": final_y1})
                    ],
                    on_finish = lambda: self.hand_back(),
            )
    
    def return_ms(self):
        self.move_speed = 50
    
    def speed_boost(self):
        self.move_speed = 100
        Timer.after(
            5,
            lambda: self.return_ms(),
        )
    
    def move(self, target_x, target_y):
        self.target_x = target_x / 2 - self.width / 2
        self.target_y = target_y / 2 - self.height / 2
        dy = self.target_y - self.y
        dx = self.target_x - self.x
        d = sqrt(dx*dx + dy*dy)
        self.vx = dx/d * self.move_speed
        self.vy = dy/d * self.move_speed
        
        

    def update(self, dt: float):
        self.x = self.x + self.vx * dt
        self.y = self.y + self.vy * dt
        if self.target_x != None and self.target_y != None:
            if (abs(self.target_x-self.x) < 1) and abs(self.target_y - self.y) < 1:
                self.vx = 0
                self.vy = 0
        if self.has_hand1:
            self.hand1.x = self.x + 2
            self.hand1.y = self.y + 20
        if self.has_hand2:
            self.hand2.x = self.x + 32
            self.hand2.y = self.y + 20
        
    
    def render(self, surface) -> None:
        surface.blit(
            self.texture, (self.x, self.y-14)
        )
        if not self.has_hand1:
            self.hand1.render(surface)
        if not self.has_hand2:
            self.hand2.render(surface)
        if self.has_shield:
            surface.blit(
                self.shield_texture, (self.x-2, self.y-18)
            )

        if self.is_taking_damage:
            surface.blit(
                self.health_barhit, (self.x-2, self.y-16)
            )
        else:
            if self.health == 0:
                surface.blit(
                    self.health_bar0, (self.x-2, self.y-18)
                )

            if self.health == 1:
                surface.blit(
                    self.health_bar1, (self.x-2, self.y-18)
                )

            if self.health == 2:
                surface.blit(
                    self.health_bar2, (self.x-2, self.y-18)
                )

            if self.health == 3:
                surface.blit(
                    self.health_bar3, (self.x-2, self.y-18)
                )

            if self.health == 4:
                surface.blit(
                    self.health_bar4, (self.x-2, self.y-18)
                )

            if self.health == 5:
                surface.blit(
                    self.health_bar5, (self.x-2, self.y-18)
                )

            if self.health == 6:
                surface.blit(
                    self.health_bar6, (self.x-2, self.y-18)
                )

            if self.health == 7:
                surface.blit(
                    self.health_bar7, (self.x-2, self.y-18)
                )

            if self.health == 8:
                surface.blit(
                    self.health_bar8, (self.x-2, self.y-18)
                )

            if self.health == 9:
                surface.blit(
                    self.health_bar9, (self.x-2, self.y-18)
                )

            if self.health == 10:
                surface.blit(
                    self.health_bar10, (self.x-2, self.y-18)
                )