import pygame

from gale.state import BaseState
from gale.text import render_text
from gale.input_handler import InputData


import settings

class StartState(BaseState):
    def enter(self)-> None:
        # Configuramos el índice de la opción seleccionada y las opciones del menú
        self.selected = 1
        
        self.level2_unlock = False
        self.level3_unlock = False
        
        
        
    def on_input(self, input_id: str, input_data: InputData) -> None: 
        if input_id == "move_right" and input_data.pressed and self.selected == 1:
            self.selected = 2
        elif input_id == "move_right" and input_data.pressed and self.selected == 2:
            self.selected = 3
        elif input_id ==  "move_right" and input_data.pressed and self.selected == 3:
            self.selected = 1

        elif input_id == "move_left" and input_data.pressed and self.selected == 2:
            self.selected = 1
        elif input_id ==  "move_left" and input_data.pressed and self.selected == 3:
            self.selected = 2
        elif input_id ==  "move_left" and input_data.pressed and self.selected == 1:
            self.selected = 3
        
        # Confirmar la opción seleccionada con Enter o con 'confirm'
        elif input_id == "confirm" and input_data.pressed:
            if self.selected == 1:
                self.state_machine.change(
                "LevelSelectionState",
                level2_unlock = self.level2_unlock,
                level3_unlock = self.level3_unlock,
                arena_unlock = False
                )  
            elif self.selected == 2:  # Opción "Instructions"
                self.state_machine.change("instructions")
            elif self.selected == 3:  # Opción "Quit"
                pygame.quit()
                exit()

        
    
    def render(self, surface: pygame.Surface) -> None:        
        surface.blit(settings.TEXTURES["background"], (0, 0))   
        
        # Dibuja el título del juego     
        logo = settings.TEXTURES["logo"]
        logo_rect = logo.get_rect(center=(settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 4))
        surface.blit(logo, logo_rect)

        menu_y_position = settings.VIRTUAL_HEIGHT - 120  
        
        play_button = settings.TEXTURES["play_button"]
        if self.selected == 1:
            play_button = settings.TEXTURES["play_selected"]
        
        play_button_rect = play_button.get_rect(center=(settings.VIRTUAL_WIDTH // 4, menu_y_position))
        surface.blit(play_button, play_button_rect)

        instructions_button = settings.TEXTURES["instructions_button"]
        if self.selected == 2:
            instructions_button = settings.TEXTURES["instructions_selected"]
        instructions_button_rect = instructions_button.get_rect(center=(settings.VIRTUAL_WIDTH // 2, menu_y_position))
        surface.blit(instructions_button, instructions_button_rect)

        quit_button = settings.TEXTURES["quit_button"]
        if self.selected == 3:
            quit_button = settings.TEXTURES["quit_selected"]
        quit_button_rect = quit_button.get_rect(center=(3 * settings.VIRTUAL_WIDTH // 4, menu_y_position))
        surface.blit(quit_button, quit_button_rect)


    def update(self, dt: float) -> None:
       pass