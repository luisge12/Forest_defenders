#state to select level

import pygame
from gale.state import BaseState
from gale.text import render_text
from gale.input_handler import InputData

import settings

class LevelSelectionState(BaseState):
    def enter(self, **params: dict) -> None:
        self.selected = 0
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        self.level_1 = settings.TEXTURES["Level_1"]
        self.level_1_rect = self.level_1.get_rect(center=(settings.VIRTUAL_WIDTH // 4, settings.VIRTUAL_HEIGHT // 2))
     
        self.level2_unlock = params["level2_unlock"]
        self.level3_unlock = params["level3_unlock"]
        self.arena_unlock = params["arena_unlock"]

        self.Level_1_clip = settings.VIDEOS["level_1_vid"]
        self.Level_2_clip = settings.VIDEOS["level_2_vid"]
        self.Level_3_clip = settings.VIDEOS["level_3_vid"]


        self.Level_1_clip_time = 0
        self.Level_2_clip_time = 0
        self.Level_3_clip_time = 0

        self.Level_1_clip_playing = False
        self.Level_2_clip_playing = False
        self.Level_3_clip_playing = False

    def on_input(self, input_id: str, input_data: InputData) -> None:

        if pygame.mouse.get_pressed()[0] and self.selected == 1:
            self.state_machine.change("Level1", 
                                      level2_unlock = self.level2_unlock, 
                                      level3_unlock = self.level3_unlock, 
                                      arena_unlock = False)
        
        elif pygame.mouse.get_pressed()[0] and self.selected == 2 and self.level2_unlock == True:
            self.state_machine.change("Level2", 
                                      level2_unlock = self.level2_unlock,
                                      level3_unlock = self.level3_unlock, 
                                      arena_unlock = False)
        
        elif pygame.mouse.get_pressed()[0] and self.selected == 3 and self.level3_unlock == True:
            self.state_machine.change("Level3",
                                      level2_unlock = self.level2_unlock,
                                      level3_unlock = self.level3_unlock, 
                                      arena_unlock = False)
        

    


    def update(self, dt: float) -> None:
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.mouse_x = int(mouse_x * settings.SCALE_X)
        self.mouse_y = int(mouse_y * settings.SCALE_Y)

        if self.Level_1_clip_playing:
            self.Level_1_clip_time += dt

        if self.Level_2_clip_playing:
            self.Level_2_clip_time += dt

        if self.Level_3_clip_playing:
            self.Level_3_clip_time += dt


    def render(self, surface: pygame.Surface) -> None:
        
        if self.level2_unlock == False:
            self.level_2 = settings.TEXTURES["Level_2_b"]
        
        if self.level2_unlock == True:

            self.level_2 = settings.TEXTURES["Level_2"]
            
        if self.level3_unlock == False:
            self.level_3 = settings.TEXTURES["Level_3_b"]
        else:
            self.level_3 = settings.TEXTURES["Level_3"]
        
        if self.arena_unlock == True:
            self.state_machine.change("arena")
        surface.blit(settings.TEXTURES["background"], (0, 0))
        
        

        # level 1 banner render
        surface.blit(self.level_1, self.level_1_rect)        
        
        if self.level_1_rect.collidepoint(self.mouse_x, self.mouse_y):
            self.selected = 1
            self.on_input(self.selected, None)
            
            self.Level_1_clip_playing = True
            frame = self.Level_1_clip.get_frame(self.Level_1_clip_time)
            pygame_frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            pygame_frame = pygame.transform.scale(pygame_frame, self.level_1_rect.size)
            surface.blit(pygame_frame, self.level_1_rect.topleft)
        else:
            self.Level_1_clip_playing = False
            self.Level_1_clip_time = 0

  
        level_2_rect = self.level_2.get_rect(center=(settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2))
        surface.blit(self.level_2, level_2_rect)

        if level_2_rect.collidepoint(self.mouse_x, self.mouse_y):
            self.selected = 2
            self.on_input(self.selected, None)
            
            self.Level_2_clip_playing = True
            frame = self.Level_2_clip.get_frame(self.Level_2_clip_time)
            pygame_frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            pygame_frame = pygame.transform.scale(pygame_frame, level_2_rect.size)
            surface.blit(pygame_frame, level_2_rect.topleft)
        else:
            self.Level_2_clip_playing = False
            self.Level_2_clip_time = 0

        level_3_rect = self.level_3.get_rect(center=(3 * settings.VIRTUAL_WIDTH // 4, settings.VIRTUAL_HEIGHT // 2))
        surface.blit(self.level_3, level_3_rect)
        
        if level_3_rect.collidepoint(self.mouse_x, self.mouse_y):
            self.selected = 3
            self.on_input(self.selected, None)
            
            self.Level_3_clip_playing = True
            frame = self.Level_3_clip.get_frame(self.Level_3_clip_time)
            pygame_frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            pygame_frame = pygame.transform.scale(pygame_frame, level_3_rect.size)
            surface.blit(pygame_frame, level_3_rect.topleft)
        else:
            self.Level_3_clip_playing = False
            self.Level_3_clip_time = 0

        if self.level_1_rect.collidepoint(self.mouse_x, self.mouse_y) == False and level_2_rect.collidepoint(self.mouse_x, self.mouse_y) == False and level_3_rect.collidepoint(self.mouse_x, self.mouse_y) == False:
            self.selected = 0