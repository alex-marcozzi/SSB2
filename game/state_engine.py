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
        #print("there")
        for event in events:
            #print("for")
            if event.type == pygame.KEYDOWN:
                #print("gah")
                if event.key == pygame.K_1:
                    self.state = State.LEVEL_SELECT
                    #print("hi")
                elif event.key == pygame.K_2:
                    self.state = State.CREDITS
                elif event.key == pygame.K_3:
                    print("Quit?")

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
        #print(self.dt)
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
        #self.TITLE_FONT.render_to(screen, ((self.width / 2) - 250, self.height / 5), 
                #"Super Square Boy", self.font_color)
        #text = "Super Square Bui"
        #text_rect = self.TITLE_FONT.get_rect(text, size = 50)
        #text_rect.center = (self.width / 2, self.height / 2)#screen.get_rect().center 
        #self.TITLE_FONT.render_to(screen, text_rect, text, (0,0,0), size = 50) 
        self.drawTextXCenter(screen, "Super Square Boy", self.font_color, 100, self.height / 5)
    
    def drawLevelSelect(self, screen):
        screen.fill(self.background_color)
        self.drawTextXCenter(screen, "Level Select", self.font_color, 100, self.height / 5)
        #self.FONT.render_to(screen, ((self.width / 2) - 250, self.height / 5), 
        #        "Level Select", self.font_color)
    
    def drawCredits(self, screen):
        screen.fill(self.background_color)
        self.drawTextXCenter(screen, "Credits", self.font_color, 100, self.height / 5)
        #self.FONT.render_to(screen, ((self.width / 2) - 250, self.height / 5), 
        #        "Credits", self.font_color)

    def drawPlaying(self, screen):
        screen.fill(self.background_color)
        self.engine.draw(screen)

    def drawPaused(self, screen):
        screen.fill(self.background_color)
        self.drawTextXCenter(screen, "Paused", self.font_color, 100, self.height / 5)
        #self.FONT.render_to(screen, ((self.width / 2) - 250, self.height / 5), 
        #        "Paused", self.font_color)
    
    def drawTextXCenter(self, screen, text, color, size, y):
        text_rect = self.FONT.get_rect(text, size = size)
        text_rect.center = (self.width / 2, y)
        self.FONT.render_to(screen, text_rect, text, color, size = size) 