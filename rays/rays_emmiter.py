import pygame
from pygame import Vector2
from ray import Ray
from ground_gen import Material

class RaysEmmiter():
    def __init__(self, start, end, lines):
        self.start:Vector2 = start
        self.end:Vector2 = end
        self.lines = lines

        self.universal_material =  Material('black', 1, True)

        #Rays initialisation

        dir:Vector2 = self.end - self.start
        self.how_many =  1#max(1, int(dir.length() / 12))
        
        self.rays_dist = dir / self.how_many   
        self.normal = Vector2(-dir.y, dir.x)
        self.rays = []
        self.initial_rays = [Ray(self.start + i * self.rays_dist, self.normal, self.lines, color = 'grey', curr_material =self.universal_material, universal = self.universal_material) for i in range(self.how_many + 1)]
        for ray in self.initial_rays:
            self.rays.extend(ray.calculate())
    

    def draw(self, screen, font):
        pygame.draw.line(screen, 'white', self.start, self.end, 2)
        for ray in self.rays:
            ray.draw(screen, font)
    
     
    def move(self, diff, ind): #(self, end)
        if ind == 0: self.start += diff
        else: self.end += diff 
        # self.end = end


        dir:Vector2 = self.end - self.start
        self.how_many:int =  1#max(1, int(dir.length() / 12))
        self.rays_dist:Vector2 = dir / self.how_many  
        self.normal = Vector2(-dir.y, dir.x)   

        self.rays = []
        self.initial_rays = [Ray(self.start + i * self.rays_dist, self.normal, self.lines, color= 'grey', curr_material = self.universal_material, universal = self.universal_material) for i in range(self.how_many + 1)]

        # for i, ray in enumerate(self.initial_rays): 
        #     ray.move(self.start + i * self.rays_dist, self.normal)

        for ray in self.initial_rays:
            self.rays.extend(ray.calculate())
    