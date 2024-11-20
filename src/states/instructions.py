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

class instructions(BaseState):       
    def enter(self):
        #self.bishio = Dron(settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2)
        
        self.texture = settings.TEXTURES['instruction']
        
       
    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.texture, (0, 0))
        
        
        
    def on_input(self, input_id: str, input_data: InputData) -> None:
        
        if input_id == "confirm" and input_data.pressed:
            self.state_machine.change(
                "start"
            )
            
            
        