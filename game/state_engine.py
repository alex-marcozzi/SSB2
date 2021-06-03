import pygame
from pygame.constants import K_ESCAPE
import pygame.freetype
from enum import Enum
from game.engine import Engine

class State(Enum):
    MAIN         = 1
    CREDITS      = 2
    LEVEL_SELECT = 3
    PLAYING      = 4
    PAUSED       = 5

class StateEngine:
    def __init__(self, width, height):
        self.engine = Engine(width, height)
        self.state  = State.PLAYING#State.MAIN
        self.clock  = pygame.time.Clock()
        self.dt     = clock.tick(60)
        self.FONT = pygame.freetype.Font(
                "assets/fonts/momcake/MomcakeBold-WyonA.ttf", 48)
    
    def update(self):
        keys = pygame.key.get_pressed()
        if self.state == State.PLAYING:
            self.state = State.PAUSED
        
        if self.state == State.PLAYING:
            self.updatePlaying(keys)
            self.engine.update(self.dt, keys)
        elif self.state == State.PAUSED:
            self.updatePaused(keys)
            self.state = State.PLAYING
    
    def updateMain(self, keys):
        if keys[K_1]:
            self.state = State.LEVEL_SELECT
        elif keys[K_2]:
            self.state = State.CREDITS
        elif keys[K_3]:
            print("Quit?")

    def updateCredits(self, keys):
        if keys[K_ESCAPE]:
            self.state = State.MAIN

    def updateLevelSelect(self, keys):
        if keys[K_1]:
            self.state = State.PLAYING
            self.engine.loadLevel("assets/levels/level1.txt")
        elif keys[K_2]:
            self.state = State.PLAYING
            self.engine.loadLevel("assets/levels/level2.txt")
        elif keys[K_3]:
            self.state = State.PLAYING
            self.engine.loadLevel("assets/levels/level3.txt")
        elif keys[K_4]:
            self.state = State.PLAYING
            self.engine.loadLevel("assets/levels/level4.txt")
    
    def updatePlaying(self, keys):
        self.engine.update(self.dt, keys)
        if keys[pygame.K_ESCAPE]:
            self.state = State.PAUSED
    
    def updatePaused(self, keys):
        if keys[pygame.K_1] or keys[pygame.K_ESCAPE]:
            self.state = State.PLAYING
        elif keys[pygame.K_2]:
            self.state = State.MAIN
