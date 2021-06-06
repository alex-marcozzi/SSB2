import sys, pygame
from game.state_engine import StateEngine
pygame.init()
pygame.mixer.init()

#size = width, height = 800, 600
size = width, height = 1200, 700

flags = pygame.SCALED|pygame.DOUBLEBUF|pygame.HWSURFACE|pygame.FULLSCREEN
screen = pygame.display.set_mode(size, flags)

clock = pygame.time.Clock()
state_engine = StateEngine(width, height, clock.tick(60))
while 1:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: sys.exit()

    clock.tick(60)
    #clock.tick_busy_loop(60)
    state_engine.update(events)

    screen.fill((0, 0, 0))
    state_engine.draw(screen)
    pygame.display.flip()