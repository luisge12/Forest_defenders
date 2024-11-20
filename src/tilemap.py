"""
ISPPJ1 2024
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class GameLevel.
"""

from typing import Any, Dict

import pygame
import pytmx
from pytmx import load_pygame

import settings

def load_map(path):
    tmx_data = load_pygame(path)
    return tmx_data


class GameLevel:
    def __init__(self, num_level: int) -> None:
        
        self.map = load_map("assets/graphics/tile_maps/Level1_map.tmx")
    
        settings.LevelLoader().load(self, settings.TILEMAPS[num_level])


    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(0, 0, self.map.width, self.map.height)

    def set_render_boundaries(self, rect: pygame.Rect) -> None:
        self.map.set_render_boundaries(rect)

    def update(self, dt: float) -> None:
       pass

    def render(self, surface: pygame.Surface) -> None:
        self.tilemap.render(surface)
        for creature in self.creatures:
            creature.render(surface)
        for item in self.items:
            if item.active:
                item.render(surface)
