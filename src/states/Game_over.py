from typing import TypeVar
import pygame
from math import sqrt

from gale.state import BaseState
from gale.input_handler import InputData
from gale.factory import Factory
from gale.text import render_text
from gale.timer import Timer
from src.Dron import Dron
from src.Bullet import Bullet
from src.Wild_robot import Wild_robot

import settings

class Game_over(BaseState):       
    def enter(self, **params: dict):
        #self.bishio = Dron(settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2)
        self.level3_unlock = params["level3_unlock"]
        self.level2_unlock = params["level2_unlock"]
        
        self.texture = settings.TEXTURES["background"]
        
        
     
    
       
    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.texture, (0, 0))
        render_text(
            surface,
            f"Game Over",
            settings.FONTS["extra_large"],
            settings.VIRTUAL_WIDTH // 2 - 40,
            settings.VIRTUAL_HEIGHT // 2 - 20,
            (255, 255, 255),
        )
        render_text(
            surface,
            f"Pulse enter to continue",
            settings.FONTS["large"],
            settings.VIRTUAL_WIDTH // 2 - 60,
            settings.VIRTUAL_HEIGHT // 2 ,
            (255, 255, 255),
        )
        
        
        
    def on_input(self, input_id: str, input_data: InputData) -> None:
        
        if input_id == "confirm" and input_data.pressed:
            self.state_machine.change(
                "LevelSelectionState",
                level2_unlock = self.level2_unlock,
                level3_unlock = self.level3_unlock,
                arena_unlock = False
            )
            
            
        