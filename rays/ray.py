import pygame
from pygame import Vector2, Color
from  math import sin, sqrt, cos, acos
from ground_gen import Material









# TO DO
# correct the fucking collision detection
# calc the strength of reflection for full internal reflection (is it 1? - i set it on one, it doent mean that it its correct)
# make so that rays can be spawned inside a material (idea: make rects/triangles     that depicts if the start is in a material)









EPS = 0.001
class Ray():
    def __init__(self, start, dir, lines, last_line:int = None, curr_material:Material = Material('black', 1, True), color:Color = Color(255, 255, 0), universal:Material = Material('black', 1, True), strength = 1):
        self.start:Vector2 = start
        self.dir:Vector2 = dir
        self.collision_point:Vector2 = None
        self.normal:Vector2 = None

        self.last_material = curr_material
        # self.temp_material = curr_material
        self.curr_material = curr_material

        self.universal = universal

        self.reflected_rays = []

        self.strength = strength

        self.lines = lines
        self.last_line = last_line
        self.color = Color(int(color.r * self.strength), int(color.g * self.strength), int(color.b * self.strength))
        
    
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
                self.normal = self.normal if self.normal.dot(self.dir) < 0 else -self.normal

                if not self.lines[i].material.is_passable:
                    # case light cannot possibly go through

                    #FULLY REFLECTED RAY
                    self.reflected_rays.append(Ray(self.collision_point, 
                                                   self.dir.reflect(self.normal), 
                                                   self.lines, 
                                                   i, 
                                                   curr_material=self.curr_material,  
                                                   universal = self.universal, 
                                                   strength= self.strength)) 
                    return True

                elif self.curr_material.light_bent_factor == self.lines[i].material.light_bent_factor:
                    # case that line exits the current material (eg. went through glass -> leaves glass)
                    
                    self.last_material = self.curr_material
                    self.curr_material = self.universal
                
                else:
                    #case that line enters new material

                    self.last_material = self.curr_material
                    self.curr_material = self.lines[i].material


                n1 = self.last_material.light_bent_factor
                n2 = self.curr_material.light_bent_factor

                alpha = acos(self.normal.dot(self.dir))
                
                #IF A RAY CAN PASS AN OBJECT AND PASSES THROUGH (NO INTERNAL REFLECTIONS)
                if sin(alpha) <= (n2 / n1) or n1 < n2:

                    strength_refl = self.strength * (((n2 - n1) / (n2 + n1)) ** 2)
                    strength_refr = 1 - strength_refl 
                    
                    new_dir = self.normal * ( - n1/n2 * cos(alpha) - sqrt(1 - ((n1/n2) ** 2) * (1 - cos(alpha) ** 2))) + n1/n2 * self.dir 

                    #ray that can pass through
                    self.reflected_rays.append(Ray(self.collision_point, 
                                                   new_dir, 
                                                   self.lines, 
                                                   i, 
                                                   self.curr_material, 
                                                   color = self.color, 
                                                   strength= strength_refr))
                    # reflected ray
                    if strength_refl > 0.004:
                        self.reflected_rays.append(Ray(self.collision_point, 
                                                   self.dir.reflect(self.normal), 
                                                   self.lines, 
                                                   i, 
                                                   curr_material=self.curr_material,  
                                                   universal = self.universal, 
                                                   strength= strength_refl)) 
                
                else: #IF A RAY CAN PASS AN MATERIAL BUT DO NOT PASSES THROUGH (FULL INTERNAL REFLECTION)

                    # reflected ray
                    self.reflected_rays.append(Ray(self.collision_point, 
                                                   self.dir.reflect(self.normal), 
                                                   self.lines, 
                                                   i, 
                                                   curr_material=self.curr_material,  
                                                   universal = self.universal, 
                                                   strength= self.strength)) 

                return True


        return False # przypadek równoległych lub jednoliniowych Wektorów
            

    
    def move(self, new_start, new_dir):
        self.start = new_start
        self.dir = new_dir
        
