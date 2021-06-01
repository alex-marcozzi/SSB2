import sys, pygame
from game.engine import Engine
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
#os.putenv('SDL_AUDIODRIVER', 'alsa')
#os.putenv('SDL_AUDIODEV', '/dev/audio')
pygame.init()
#pygame.mixer.init()

#size = width, height = 800, 600
size = width, height = 1200, 800

flags = pygame.SCALED|pygame.DOUBLEBUF|pygame.HWSURFACE
screen = pygame.display.set_mode(size, flags)

filepath = "assets/levels/testlevel.txt"
engine = Engine(width, height)
engine.loadLevel(filepath)
engine.reset()
clock = pygame.time.Clock()
counter = 0
dt = clock.tick(60)
#death_time = -1
#current_time = -1
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    counter += 1
    clock.tick(60)

    if (engine.update(dt) == True):
        print("Win")

    screen.fill((0, 0, 0))
    #if (engine.is_dead):
    #    current_time = pygame.time.get_ticks()
    #    if death_time == -1:
    #        death_time = pygame.time.get_ticks()
    #    if current_time - death_time >= 2000:
    #        engine.reset()
    #        death_time = -1
    #        current_time = -1
    #else:
    #    engine.update(dt)


        #engine.reset()
    engine.draw(screen)
    pygame.display.flip()

    #if (counter >= 100):
    #    print(clock.get_fps())
    #    counter = 0
