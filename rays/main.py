import pygame
from pygame import Vector2
from rays_emmiter import RaysEmmiter
from ground_gen import Ground, GlassBox

WIDTH, HEIGHT = 1280, 720
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)



ground = Ground(100, WIDTH, HEIGHT)
ground.generate(20)

glass = GlassBox(Vector2(500,200), Vector2(300,300))


lines = []
# lines.extend(ground.lines)
lines.extend(glass.lines)


start = Vector2(50,100)
end = Vector2(100, 100)
emmiter = RaysEmmiter(start, end, lines)
emmiter.move(Vector2(100, 100), 1) 


mouse_left = False
thing = None


while running:

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if Vector2(pygame.mouse.get_pos()).distance_to(emmiter.start) < 10:
                    thing = 0
                if Vector2(pygame.mouse.get_pos()).distance_to(emmiter.end) < 10:
                    thing = 1
        if event.type == pygame.MOUSEMOTION:
            if thing != None:
                emmiter.move(event.rel, thing)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                thing = None

    screen.fill("black")

    # emmiter.move(Vector2(pygame.mouse.get_pos())) 
    emmiter.move(Vector2(0, 0), 0)  #-----------------------------------------------------------------------------FOR SOME REASON IT HAVE TO BE MOVED EACH FRAME

    
    emmiter.draw(screen, my_font)
    for line in lines: line.draw(screen)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
