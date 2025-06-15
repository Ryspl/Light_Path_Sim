import pygame
from pygame import Vector2, Rect
import random

class Material():
    def __init__(self, color:str, light_bent_factor:float, is_passable:bool):
        self.color = color
        self.light_bent_factor = light_bent_factor
        self.is_passable = is_passable

        
class Line():
    def __init__(self, start:Vector2, end:Vector2, material:Material, is_full:bool):
        self.start = start
        self.end = end
        self.material = material
        self.dir = (end - start).normalize()
        self.vec_dir = (end - start)
        self.normal = Vector2(self.dir.y, -self.dir.x).normalize()
        # self.is_full = is_full
        
    
    def draw(self, screen):
        pygame.draw.line(screen, self.material.color, self.start, self.end)
        # pygame.draw.line(screen, 'red', self.start + self.vec_dir / 2, self.start + self.vec_dir / 2 + self.normal * 50)

class Ground():
    def __init__(self, ground_height, WIDTH, HEIGHT):
        self.ground_line = HEIGHT - ground_height
        self.ground_height = ground_height
        self.material = Material('red', None, False)
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.points = [Vector2(0, self.ground_line)]

    def generate(self, frequency):
        dist = self.WIDTH / frequency
        for i in range(1, frequency + 1):
            diff = random.randint(-40, 40)
            # if self.points[i - 1].y + diff > self.ground_height: diff = -1
            self.points.append(Vector2(i * dist, self.ground_line + diff))
        
        self.lines = []

        for i in range(len(self.points) - 1):
            self.lines.append(Line(self.points[i], self.points[i + 1], self.material, False))
        
        return self.lines
    
    def draw(self, screen):
        for line in self.lines:
            line.draw(screen)


class GlassBox():
    def __init__(self, pos:Vector2, size:Vector2):  
        self.pos = pos
        self.size = size
        self.material = Material('blue', 1.5, True)
        self.lines = [Line(self.pos, Vector2(self.pos.x + self.size.x, self.pos.y), self.material, True), 
                      Line(Vector2(self.pos.x, self.pos.y + self.size.y),self.pos, self.material, True),
                      Line(Vector2(self.pos.x + self.size.x, self.pos.y), self.pos + self.size, self.material, True),
                      Line(Vector2(self.pos.x, self.pos.y + self.size.y), self.pos + self.size, self.material, True)]


    
    def draw(self, screen):
        for line in self.lines:
            pygame.draw.line(screen, self.material.color, self.start, self.end)
