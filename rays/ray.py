import pygame
from pygame import Vector2, Color
from  math import sin, asin
from ground_gen import Material









# TO DO
# find the fucking new_dir when passing through new material
# make so that rays can be spawned inside a material (idea: make rects/triangles     that depicts if the start is in a material)









EPS = 0.001
class Ray():
    def __init__(self, start, dir, lines, last_line:int = None, curr_material = Material('black', 1, True), color = 'white', universal = Material('black', 1, True)):
        self.start:Vector2 = start
        self.dir:Vector2 = dir
        self.collision_point:Vector2 = None
        self.normal:Vector2 = None

        self.last_material = curr_material
        # self.temp_material = curr_material
        self.curr_material = curr_material

        self.universal = universal

        self.reflected_rays = []

        self.lines = lines
        self.last_line = last_line
        self.color = color #Color(255,255,255)
        
    
    def draw(self, screen, font):
        if self.collision_point != None:

            pygame.draw.line(screen, self.color, self.start, self.collision_point)
            pygame.draw.circle(screen, 'red', self.collision_point, 5)    
            return

        pygame.draw.line(screen, self.color, self.start, self.start + self.dir * 1000)

    
    def calculate(self):
        all_rays = [self]
        if not self.collide(): return all_rays

        for ray in self.reflected_rays:
            all_rays.extend(ray.calculate())

        return all_rays

    def collide(self): 
        for i in range(len(self.lines)):
            if self.last_line == i:
                continue   
            p:Vector2 = self.start + self.dir.normalize()
            r:Vector2 = 1000 * self.dir 
            q:Vector2 = self.lines[i].start
            s:Vector2 = self.lines[i].end - q
        
            if r.cross(s) == 0:
                return False


            # t = (q − p) × s / (r × s)
            t = (q - p).cross(s) / ( r.cross(s) )
            
            #u = (p - q) x r / (s x r)
            u = (p - q).cross(r) / s.cross(r)
            
            in_range:bool = t >= 0 and t <= 1 and u >= 0 and u <= 1

            if r.cross(s) != 0 and in_range:  # if collision occurs
                self.last_line = i

                self.collision_point = p + t * r
                self.normal = self.lines[i].normal

                #reflected ray (always present) (for update to weaken if other passed)

                self.reflected_rays.append(Ray(self.collision_point, self.dir.reflect(self.normal), self.lines, i, self.curr_material,  universal = self.universal))   

                #ray that can pass through

                if not self.lines[i].material.is_passable:
                    # case light cannot possibly go through

                    return True
                
                # elif not self.lines[i].is_full:
                #     # case that a line is a line not a border between materials
                #     self.temp_material = self.lines[i].material

                #     n1 = self.last_material.light_bent_factor
                #     n2 = self.temp_material.light_bent_factor
                #     alpha = self.dir.reflect(self.normal).angle_to(self.normal)

                #     beta = asin(sin(alpha) * n1 / n2)

                #     new_dir = self.dir.reflect(self.normal).rotate(-beta).reflect(self.lines[i].dir)

                #     self.reflected_rays.append(Ray(self.collision_point, new_dir, self.lines, i, self.curr_material))

                #     return True

                elif self.curr_material == self.lines[i].material:
                    # case that line exits the current material (eg. went through glass -> leaves glass)
                    
                    self.last_material = self.curr_material
                    self.curr_material = self.universal
                
                else:
                    #case that line enters new material

                    self.last_material = self.curr_material
                    self.curr_material = self.lines[i].material
                

                n1 = self.last_material.light_bent_factor
                n2 = self.curr_material.light_bent_factor

                # check if an angle is a limit angle and not to go through
                alpha = min((-self.dir).angle_to(self.normal), (-self.dir).angle_to(-self.normal))
                
                beta = asin(sin(alpha) * n1 / n2)

                thetha = alpha - beta

                new_dir = self.dir.reflect(self.normal).rotate(-thetha) #set angle between normal and dir to beta

                self.reflected_rays.append(Ray(self.collision_point, new_dir.reflect(self.normal), self.lines, i, self.curr_material, color='yellow'))
                    
                return True


        return False # przypadek równoległych lub jednoliniowych Wektorów
            

    
    def move(self, new_start, new_dir):
        self.start = new_start
        self.dir = new_dir
        