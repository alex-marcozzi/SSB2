# Title: app.py
# Description: Contains the main app for Super Square Boy 2.
# Author: Alexander Marcozzi
# Date: 06/12/2021

import sys, pygame
from game.state_engine import StateEngine
pygame.init()
pygame.mixer.init()

infoObject = pygame.display.Info()
pygame.display.set_mode((infoObject.current_w, infoObject.current_h))

size = width, height = infoObject.current_w, infoObject.current_h

flags = pygame.SCALED|pygame.DOUBLEBUF|pygame.HWSURFACE|pygame.FULLSCREEN
screen = pygame.display.set_mode(size, flags)

clock = pygame.time.Clock()
state_engine = StateEngine(width, height, clock.tick_busy_loop(120))
while 1:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: sys.exit()

    clock.tick_busy_loop(120)
    state_engine.update(events)

    screen.fill((0, 0, 0))
    state_engine.draw(screen)
    pygame.display.flip()