import sys, pygame
from game.engine import Engine
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
pygame.init()

#size = width, height = 800, 600
size = width, height = 1200, 800

screen = pygame.display.set_mode(size)

filepath = "assets/levels/level1.txt"
engine = Engine(width, height)
engine.loadLevel(filepath)
engine.reset()
clock = pygame.time.Clock()
counter = 0
dt = clock.tick(60)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    counter += 1
    #dt = clock.tick(60)
    clock.tick(60)

    engine.update(dt)

    screen.fill((0, 0, 0))
    engine.draw(screen)
    pygame.display.flip()

    #if (counter >= 100):
    #    print(clock.get_fps())
    #    counter = 0
