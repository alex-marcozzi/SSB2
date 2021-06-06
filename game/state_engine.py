import pygame
from pygame.constants import K_ESCAPE
import pygame.freetype
from enum import Enum
from game.engine import Engine

# the different usable states
class State(Enum):
    MAIN         = 1
    LEVEL_SELECT = 2
    CREDITS      = 3
    PLAYING      = 4
    PAUSED       = 5

class StateEngine:
    def __init__(self, width, height, dt):
        pygame.key.set_repeat(0)
        self.width  = width
        self.height = height
        self.engine = Engine(width, height)
        self.state  = State.MAIN
        #self.clock  = pygame.time.Clock()
        self.dt     = dt
        self.FONT = pygame.freetype.Font(
                "assets/fonts/momcake/MomcakeBold-WyonA.ttf", 24)
        self.background_color = (0, 250, 255)
        self.font_color       = (255, 100, 4)

    def update(self, events):
        #keys = pygame.key.get_pressed()
        #print("here")
        #events = pygame.event.get()
        if self.state   == State.MAIN:
            self.updateMain(events)
        elif self.state == State.LEVEL_SELECT:
            self.updateLevelSelect(events)
        elif self.state == State.CREDITS:
            self.updateCredits(events)
        elif self.state == State.PLAYING:
            self.updatePlaying(events)
        elif self.state == State.PAUSED:
            self.updatePaused(events)
    
    def updateMain(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.state = State.LEVEL_SELECT
                elif event.key == pygame.K_2:
                    self.state = State.CREDITS
                elif event.key == pygame.K_3:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def updateLevelSelect(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.state = State.PLAYING
                    self.engine.loadLevel("assets/levels/level1.txt")
                    self.engine.reset()
                elif event.key == pygame.K_2:
                    self.state = State.PLAYING
                    self.engine.loadLevel("assets/levels/level2.txt")
                    self.engine.reset()
                elif event.key == pygame.K_3:
                    self.state = State.PLAYING
                    self.engine.loadLevel("assets/levels/level3.txt")
                    self.engine.reset()
                elif event.key == pygame.K_4:
                    self.state = State.PLAYING
                    self.engine.loadLevel("assets/levels/level4.txt")
                    self.engine.reset()
    
    def updateCredits(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if keys[K_ESCAPE]:
                    self.state = State.MAIN
    
    def updatePlaying(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = State.PAUSED
                    pygame.mixer.music.pause()
        self.engine.update(self.dt)
    
    def updatePaused(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_ESCAPE:
                    self.state = State.PLAYING
                    pygame.mixer.music.unpause()
                elif event.key == pygame.K_2:
                    self.state = State.MAIN

    def draw(self, screen):
        if self.state   == State.MAIN:
            self.drawMain(screen)
        elif self.state == State.CREDITS:
            self.drawCredits(screen)
        elif self.state == State.LEVEL_SELECT:
            self.drawLevelSelect(screen)
        elif self.state == State.PLAYING:
            self.drawPlaying(screen)
        elif self.state == State.PAUSED:
            self.drawPaused(screen)
    
    def drawMain(self, screen):
        screen.fill(self.background_color)
        self.drawTextXCenter(screen, "Super Square Boy", self.font_color, 100, self.height / 5)
        self.drawTextXCenter(screen, "1) Level Select", self.font_color, 70, self.height / 2)
        self.drawTextXCenter(screen, "2) Credits", self.font_color, 70, self.height / 2 + 100)
        self.drawTextXCenter(screen, "3) Exit Game", self.font_color, 70, self.height / 2 + 200)
    
    def drawLevelSelect(self, screen):
        screen.fill(self.background_color)
        self.drawTextXCenter(screen, "Level Select", self.font_color, 100, self.height / 5)
        self.drawTextXCenter(screen, "1) RPM", self.font_color, 50, self.height / 2 - 75)
        self.drawTextXCenter(screen, "2) Deep Blue", self.font_color, 50, self.height / 2)
        self.drawTextXCenter(screen, "3) Luminous", self.font_color, 50, self.height / 2 + 75)
        self.drawTextXCenter(screen, "4) Spectre", self.font_color, 50, self.height / 2 + 150)
    
    def drawCredits(self, screen):
        screen.fill(self.background_color)
        self.drawTextXCenter(screen, "Credits", self.font_color, 100, self.height / 5)

    def drawPlaying(self, screen):
        screen.fill(self.background_color)
        self.engine.draw(screen)

    def drawPaused(self, screen):
        screen.fill(self.background_color)
        self.drawTextXCenter(screen, "Paused", self.font_color, 200, self.height / 5)
        self.drawTextXCenter(screen, "1) Resume", self.font_color, 70, self.height / 2)
        self.drawTextXCenter(screen, "2) Main Menu", self.font_color, 70, self.height / 2 + 100)
        #self.FONT.render_to(screen, ((self.width / 2) - 250, self.height / 5), 
        #        "Paused", self.font_color)
    
    def drawTextXCenter(self, screen, text, color, size, y):
        text_rect = self.FONT.get_rect(text, size = size)
        text_rect.center = (self.width / 2, y)
        self.FONT.render_to(screen, text_rect, text, color, size = size)