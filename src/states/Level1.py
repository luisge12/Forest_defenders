from typing import TypeVar
import pygame
from math import sqrt
import pytmx
from pytmx import load_pygame
from gale. state import BaseState
from gale.input_handler import InputData
from gale.factory import Factory
from gale.text import render_text
from gale.timer import Timer
from src.Dron import Dron
from src.Bullet import Bullet
from src.Wild_robot import Wild_robot
from src.camera import Camera
from gale.animation import Animation

import settings
def load_map(path):
    tmx_data = load_pygame(path)
    return tmx_data

class Level1(BaseState):
    def enter(self, **params: dict) -> None:
        
        self.zoom_level = 1
        self.map = load_map("assets/graphics/tile_maps/Level1_map.tmx")
        settings.SOUNDS["level_1"].play(loops=-1)
        self.level2_unlock = params["level2_unlock"]
        self.level3_unlock = params["level3_unlock"]
        
        self.collidable_tile = []
        self.liquid_tile = []
        self.cofre_tile = []
        
        self.is_finished = False
        self.dron_factory = Factory(Dron)
        self.drones = []
        self.wcooldown = True
        self.ecooldown = True
    
        self.drones_spawn = [#(0-settings.DRON_WIDTH, 0-settings.DRON_HEIGHT),
                             (settings.MAP_WIDTH/2 - settings.DRON_WIDTH/2, 0 - settings.DRON_HEIGHT/2),
                             (settings.MAP_WIDTH, 0 -settings.DRON_HEIGHT),
                             #(settings.MAP_WIDTH, settings.MAP_HEIGHT//4 -  settings.DRON_HEIGHT/2),
                             (settings.MAP_WIDTH, settings.MAP_HEIGHT//2 -  settings.DRON_HEIGHT/2),
                             #(settings.MAP_WIDTH, settings.MAP_HEIGHT*3//4 -  settings.DRON_HEIGHT/2),
                             #(0-settings.DRON_WIDTH, settings.MAP_HEIGHT),
                             (settings.MAP_WIDTH/2 - settings.DRON_WIDTH/2, settings.MAP_HEIGHT),
                             (settings.MAP_WIDTH, settings.MAP_HEIGHT)
                             ]
       
        
        Timer.every(10,
            self.create_drones,
        )
               
        # Dimensiones del mapa
        map_width = (self.map.width * self.map.tilewidth)
        map_height = (self.map.height * self.map.tileheight)

        spawn_x, spawn_y = 0, 0
        for layer in self.map.layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.name == "eva_pos":
                        spawn_x = obj.x
                        spawn_y = obj.y
                        break
        
        self.bishio_bueno = Wild_robot(spawn_x, spawn_y)

        

        # Inicializa la cámara en la posición de inicio del robot
        self.camera = Camera(spawn_x, spawn_y, settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
        self.camera.attach_to(self.bishio_bueno)
        # Establece los límites de colisión de la cámara al tamaño del mapa
        self.camera.set_collision_boundaries(pygame.Rect(0, 0, map_width, map_height))
        self.create_drones()
        
    def create_drones(self):
        if len(self.drones)<=15:
            for pos in self.drones_spawn:           
                dron = self.dron_factory.create(pos[0],pos[1])
                dron.target_x = self.bishio_bueno.x
                dron.target_y = self.bishio_bueno.y
                self.drones.append(dron)  

    def on_input(self, input_id: str, input_data: InputData) -> None:
        # cositas de eva
         if input_id == "right_click" and input_data.pressed:
            pos = pygame.mouse.get_pos()
            map_posx = self.camera.x * 2+ pos[0] 
            map_posy = self.camera.y * 2+ pos[1] 
            self.bishio_bueno.move(map_posx,map_posy)    
        
         if input_id == "q" and input_data.pressed:
            pos = pygame.mouse.get_pos()
            map_posx = self.camera.x * 2 + pos[0] 
            map_posy = self.camera.y * 2 + pos[1] 
            self.bishio_bueno.propellants_hands(map_posx, map_posy)
        
         if input_id == "w" and input_data.pressed:
            if self.wcooldown:
                self.wcooldown = False
                Timer.after(10, lambda: self.w_cooldown())
                self.bishio_bueno.speed_boost()
            
         if input_id == "e" and input_data.pressed:
            if self.ecooldown:
                self.ecooldown = False
                Timer.after(10, lambda: self.e_cooldown()) 
                self.bishio_bueno.has_shield = True

         if input_id == "r" and input_data.pressed:           
            back_zone_x = 0
            back_zone_y = 0
            back_zone_width = 0
            back_zone_height = 0
            
            for layer in self.map.layers:
                if isinstance(layer, pytmx.TiledObjectGroup):
                    for obj in layer:
                        if obj.name == "back_zone":
                            back_zone_x =  obj.x
                            back_zone_y =  obj.y
                            back_zone_width = obj.width
                            back_zone_height = obj.height
                            break            
            self.bishio_bueno.x = back_zone_x + back_zone_width//2
            self.bishio_bueno.y =  back_zone_y + back_zone_height//2
            self.bishio_bueno.vx = 0
            self.bishio_bueno.vy = 0
            self.bishio_bueno.health = 10
            
            

    def update(self, dt: float) -> None:
        # Actualiza la posición de la cámara para que siga al robot
        self.camera.update()
        self.bishio_bueno.update(dt)
       

            
        #cargar cada drone y bullets 
        for d in self.drones:
            d.target_x = self.bishio_bueno.x
            d.target_y = self.bishio_bueno.y
            
            d.update(dt)
            if (sqrt((d.x-d.target_x)**2 + (d.y-d.target_y)**2) > d.range_radius):
                d.move(d.target_x,d.target_y)
            else:
                d.vx = 0
                d.vy = 0
                d.shoot(d.target_x,d.target_y)
            for b in d.bullets:
                b.update(dt)

        #check collitions
        for d in self.drones:
            if self.bishio_bueno.hand1.collides_with(d) or self.bishio_bueno.hand2.collides_with(d):
                settings.SOUNDS["drone_explode"].play()
                self.drones.remove(d)
            for b in d.bullets:
                if b.collides_with(self.bishio_bueno):
                    if self.bishio_bueno.has_shield:
                        self.bishio_bueno.has_shield = False
                        
                    else:
                        self.bishio_bueno.taking_damage()
                    d.pop()
        if self.bishio_bueno.health <= 0:
            self.game_over()
        
        
                
    def render(self, surface: pygame.Surface) -> None:
        
        surface1 = pygame.Surface((settings.MAP_WIDTH,settings.MAP_HEIGHT))
        surface2 = pygame.Surface((settings.VIRTUAL_WIDTH,settings.VIRTUAL_HEIGHT))
        if self.is_finished:
            surface2.fill((0, 143, 57))
            
            render_text(
               surface2,
               "!YOU WIN, you save the animals!",
               settings.FONTS["large"],
               settings.VIRTUAL_WIDTH // 2 -120,
               settings.VIRTUAL_HEIGHT // 2 -160,
               (212, 175, 55),
                   
            )
             
            render_text(
               surface2,
               "Level 2 UNLOCKED",
               settings.FONTS["large"],
               settings.VIRTUAL_WIDTH // 2 -80,
               settings.VIRTUAL_HEIGHT // 2 - 120,
               (212, 175, 55),
                   
            )
            
            chick = settings.TEXTURES["chick"]
            chick_rect = chick.get_rect(center=(settings.VIRTUAL_WIDTH // 4, settings.VIRTUAL_HEIGHT // 2))
            surface2.blit(chick, chick_rect)
            
            chicken = settings.TEXTURES["chicken"]
            chicken_rect = chicken.get_rect(center=(settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2))
            surface2.blit(chicken, chicken_rect)
            
            duck = settings.TEXTURES["duck"]
            duck_rect = duck.get_rect(center=(3 * settings.VIRTUAL_WIDTH // 4, settings.VIRTUAL_HEIGHT // 2))
            surface2.blit(duck, duck_rect)
          
        
        surface.fill((255, 155, 255))
       
        self.render_map(surface1)
        self.bishio_bueno.render(surface1)
        
        
         
        for d in self.drones:
            d.render(surface1)
            for b in d.bullets:
                b.render(surface1)
                
        
        surface.blit(surface1,(-self.camera.x,-self.camera.y))
        if self.is_finished:
          
            surface.blit(surface2,(0,0))

    def render_map(self, surface: pygame.Surface):
           
        for layer in self.map.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                self.render_layer(surface, layer)
                self.map_collision(layer)

            
            
    def render_layer(self, surface, layer):
        tile_width = self.map.tilewidth 
        tile_height = self.map.tileheight 

        for x, y, gid in layer:
            if gid:
                tile = self.map.get_tile_image_by_gid(gid)
                if tile:
        
                    screen_x = (x * tile_width) 
                    screen_y = (y * tile_height) 
                    surface.blit(tile, (screen_x, screen_y))
    
    def map_collision(self, layer):
        tile_width = self.map.tilewidth
        tile_height = self.map.tileheight
        
        robot_tile_x = self.bishio_bueno.x//tile_width
        robot_tile_y = self.bishio_bueno.y//tile_height
       
        
        for x, y, gid in layer:
            if gid:
                tile = self.map.get_tile_properties_by_gid(gid)
                if tile and 'solid' in tile and tile['solid']:
                    self.collidable_tile.append((x, y))
                if tile and 'liquid' in tile and tile['liquid']:
                    self.liquid_tile.append((x, y))
        
        end_zone_x = 0
        end_zone_y = 0
        end_zone_width = 0
        end_zone_height = 0
        
        for layer in self.map.layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.name == "end_zone":
                        end_zone_x = obj.x
                        
                        end_zone_y = obj.y
                        end_zone_width = obj.width
                        end_zone_height = obj.height
                        break

                
        if ((self.bishio_bueno.x + self.bishio_bueno.width > end_zone_x) and (self.bishio_bueno.x < end_zone_x + end_zone_width)
           and (self.bishio_bueno.y + self.bishio_bueno.height > end_zone_y) and (self.bishio_bueno.y < end_zone_y + end_zone_height)):
                    
            self.level2_unlock = True
            if not self.is_finished:
                Timer.clear()
            
            self.is_finished = True
            for d in self.drones:
                self.drones.remove(d)
            Timer.after(3, 
                        lambda: self.wining_()
                        ) 
            
                                    
                
        if (robot_tile_x, robot_tile_y) in self.collidable_tile:
            
            back = 0.25
            self.bishio_bueno.x -= self.bishio_bueno.vx * back
            self.bishio_bueno.y -= self.bishio_bueno.vy * back
            
            self.bishio_bueno.vx = 0
            self.bishio_bueno.vy = 0
        
        if (robot_tile_x, robot_tile_y) in self.liquid_tile:            
            back = 0.25
            self.bishio_bueno.x -= self.bishio_bueno.vx * back
            self.bishio_bueno.y -= self.bishio_bueno.vy * back
            self.bishio_bueno.taking_damage()
            self.bishio_bueno.vx = 0
            self.bishio_bueno.vy = 0
        
                               
    def wining_(self):
        
        settings.SOUNDS["level_1"].stop() 
        self.state_machine.change(
            "LevelSelectionState",
            level2_unlock=self.level2_unlock,
            level3_unlock=self.level3_unlock,
            arena_unlock=False
            )

    
    def game_over(self):
        settings.SOUNDS["level_1"].stop()  
        self.state_machine.change("Game_over", 
                                  level2_unlock = self.level2_unlock, 
                                  level3_unlock = self.level3_unlock, 
                                  arena_unlock = False)
        
    def w_cooldown(self):
        self.wcooldown = True
    
    def e_cooldown(self):
        self.ecooldown = True