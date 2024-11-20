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
from src.Final_Boss import Final_Boss

import settings
def load_map(path):
    tmx_data = load_pygame(path)
    return tmx_data

class arena(BaseState):
    def enter(self) -> None:
        
        self.zoom_level = 1
        self.map = load_map("assets/graphics/tile_maps/arena.tmx")
        settings.SOUNDS["arena"].play(loops=-1)
        
        self.collidable_tile = []
        self.liquid_tile = []
        self.dron_factory = Factory(Dron)
        self.fireball_factory = Factory(Bullet)
        self.drones = []
        self.fireballs = []
        self.is_already_shot = False
        
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
        
        self.fireballs_spawn = [
            (settings.ARENA_WIDTH*15/16, 0 - settings.BULLET_HEIGHT),
            (settings.ARENA_WIDTH*7/8, settings.ARENA_HEIGHT),
            (settings.ARENA_WIDTH*13/16, 0 - settings.BULLET_HEIGHT),
            (settings.ARENA_WIDTH*3/4, settings.ARENA_HEIGHT),
            (settings.ARENA_WIDTH*11/16, 0 - settings.BULLET_HEIGHT),
            (settings.ARENA_WIDTH*5/8, settings.ARENA_HEIGHT),
            (settings.ARENA_WIDTH*9/16, 0 - settings.BULLET_HEIGHT),
            (settings.ARENA_WIDTH/2, settings.ARENA_HEIGHT),
                                ]
       
        
        #Timer.every(6,
        #    self.create_drones,
        #)
               
        # Dimensiones del mapa
        map_width = (self.map.width * self.map.tilewidth)
        map_height = (self.map.height * self.map.tileheight)
        
        # Posicion del boss
        boss_pos_x, boss_pos_y = 0, 0
        spawn_x, spawn_y = 0, 0
        for layer in self.map.layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.name == "eva_pos":
                        spawn_x = obj.x
                        spawn_y = obj.y
                        break
                    
        for layer in self.map.layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:

                    if obj.name == "boss_pos":
                        boss_pos_x = obj.x
                        boss_pos_y = obj.y
            
        
        self.bishio_bueno = Wild_robot(spawn_x, spawn_y)
        self.animation = {}  
        self.list = {}
        self.explosionx_zone = 0
        self.explosiony_zone = 0
        self.current_animation = None
        self.frame_index = -1


        # Inicializa la cámara en la posición de inicio del robot
        self.camera = Camera(spawn_x, spawn_y, settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
        self.camera.attach_to(self.bishio_bueno)
        # Establece los límites de colisión de la cámara al tamaño del mapa
        self.camera.set_collision_boundaries(pygame.Rect(0, 0, map_width, map_height))
        
        self.bosito = Final_Boss(boss_pos_x, boss_pos_y)
        
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
        
         if input_id == "q" and input_data.released:
            pos = pygame.mouse.get_pos()
            map_posx = self.camera.x * 2 + pos[0] 
            map_posy = self.camera.y * 2 + pos[1] 
            self.bishio_bueno.propellants_hands(map_posx, map_posy)
        
         if input_id == "w" and input_data.pressed:
            self.bishio_bueno.speed_boost()
            
         if input_id == "e" and input_data.pressed:
            self.bishio_bueno.has_shield = True


    def update(self, dt: float) -> None:
        # Actualiza la posición de la cámara para que siga al robot
        self.camera.update()
        self.bishio_bueno.update(dt)
        self.bosito.update(dt)
        self.bosito.move(self.bishio_bueno.y)
        
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
                self.explosionx_zone = d.x
                self.explosiony_zone = d.y
                algo = Animation(
                [0,1,2,3,4,5,6,7,8,9,10,11,12],
                0.10,  # Given interval or zero
                0
                )
                self.animation["explosion"] = algo
                self.change_animation("explosion")
                self.drones.remove(d)

            for b in d.bullets:
                if b.collides_with(self.bishio_bueno):
                    if self.bishio_bueno.has_shield:
                        self.bishio_bueno.has_shield = False
                        
                    else:
                        self.bishio_bueno.taking_damage()
                    d.pop()
        for laser in self.bosito.lasers:
            if laser.collides_with(self.bishio_bueno) and laser.charged:
                if self.bishio_bueno.has_shield:
                    self.bishio_bueno.has_shield = False
                else:
                    self.bishio_bueno.taking_damage()
        
        for fire in self.fireballs:
            fire.update(dt)
            if fire.collides_with(self.bishio_bueno):
                if self.bishio_bueno.has_shield:
                    self.bishio_bueno.has_shield = False
                else:
                    self.bishio_bueno.taking_damage()
            if fire.y < 0-fire.height:
                self.fireballs.remove(fire)
            if fire.y > settings.ARENA_HEIGHT:
                self.fireballs.remove(fire)
        if self.bishio_bueno.hand1.collides_with(self.bosito) or self.bishio_bueno.hand2.collides_with(self.bosito):
            pass
        if self.bishio_bueno.hand1.collides_with(self.bosito.eye) or self.bishio_bueno.hand2.collides_with(self.bosito.eye):
            self.bosito.taking_damage()
        if self.bosito.health == 25 and self.bosito.taking_damage:
            self.shotfireballs()
        if self.bosito.health <= 0:
            self.wining()
        if self.bishio_bueno.health <= 0:
            self.game_over()
        
                
    def render(self, surface: pygame.Surface) -> None:
        
        surface1 = pygame.Surface((settings.MAP_WIDTH,settings.MAP_HEIGHT))
        
        surface.fill((0, 155, 255))
       
        self.render_map(surface1)
        self.bishio_bueno.render(surface1)
        self.bosito.render(surface1)
         
        for d in self.drones:
            d.render(surface1)
            for b in d.bullets:
                b.render(surface1)
        for fb in self.fireballs:
            fb.render(surface1)
        texture = settings.TEXTURES["explosions"]
        frame = settings.FRAMES["explosion"][self.frame_index]
        image = pygame.Surface((30, 29), pygame.SRCALPHA)
        image.blit(texture, (0, 0), frame)
        surface1.blit(image,(self.explosionx_zone,self.explosiony_zone))
        
        surface.blit(surface1,(-self.camera.x,-self.camera.y))

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
            
        final_pos_x, final_pos_y = 0, 0
        
        for layer in self.map.layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.name == "final_boss":
                        final_pos_x = obj.x
                        final_pos_y = obj.y
                        #if()
        
    def animation(self):  
        pass               
                    
    def change_animation(self, animation_id: str) -> None:
        new_animation = self.animation[animation_id]
        if new_animation != self.current_animation:
            self.current_animation = new_animation
            self.current_animation.reset()
            self.frame_index = self.current_animation.get_current_frame()
              
              
    def shotfireballs(self):
        if not self.is_already_shot:
            Timer.every(10,
                    lambda: self.shotfireballs(),
                    )
        self.is_already_shot = True
        for fb in self.fireballs_spawn:
            fireball = self.fireball_factory.create(fb[0], fb[1])
            if fb[1] == 0 - settings.BULLET_HEIGHT:
                fireball.vy = 100
            if fb[1] == settings.ARENA_HEIGHT:
                fireball.vy = -100
            self.fireballs.append(fireball)
            
    def wining(self):
        settings.SOUNDS["arena"].stop()
        self.state_machine.change("win")
    
    def game_over(self):
        settings.SOUNDS["arena"].stop()
        self.state_machine.change("Game_over")