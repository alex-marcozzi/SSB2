# Title: state_engine.py
# Description: Contains the StateEngine class for Super Square Boy 2.
# Author: Alexander Marcozzi
# Date: 06/12/2021

import pygame
import pygame.freetype
from enum import Enum
from game.engine import Engine

class State(Enum):
    """
    An enum class representing the states of the game.

    ...

    Attributes
    ----------
    MAIN : int
        the main menu
    LEVEL_SELECT : int
        the level select menu
    CREDITS : int
        the credits screen
    PLAYING : int
        the game is being played
    PAUSED : int
        the game is paused
    """
    MAIN         = 1
    LEVEL_SELECT = 2
    CREDITS      = 3
    PLAYING      = 4
    PAUSED       = 5

class StateEngine:
    """
    A class that handels the state of the game, including menu traversal.

    All "magic numbers" and formulas were acquired from manual testing.

    ...

    Attributes
    ----------
    width : int
        the width of the display, in pixels
    height : int
        the height of the display, in pixels
    engine : Engine
        the gameplay engine
    state : State
        the current state
    dt : int
        the clock's tick rate (fixed to avoid visual problems)
    FONT : pygame freetype font object
        the font to be rendered as text
    background_color : tuple(int)
        the color of the background in RGB format
    font_color : tuple(int)
        the color of the font in RGB format
    
    Methods
    -------
    update(events)
        Updates the game
    updateMain(events)
        Updates the main menu
    updateLevelSelect(events)
        Updates the level select menu
    updateCredits(events)
        Updates the credits screen
    updatePlaying(events)
        Updates the gampelay engine
    updatePaused(events)
        Updates the pause screen
    draw(screen)
        Draws the current state onto the screen
    drawMain(screen)
        Draws the main menu onto the screen
    drawLevelSelect(screen)
        Draws the level select menu onto the screen
    drawCredits(screen)
        Draws the credits screen
    drawPlaying(screen)
        Draws the state of the gameplay engine onto the screen
    drawPaused(screen)
        Draws the pause screen
    drawTextXCenter(screen, text, color, size, y)
        Draws text of a specified size and color onto the screen, centered
        on the X axis and at the specified location on the Y axis
    drawBackButton(screen)
        Draws the back button onto the screen in the lower left corner
    """

    def __init__(self, width, height, dt):
        """
        Parameters
        ----------
        width : int
            The width of the display, in pixels
        height : int
            The height of the display, in pixels
        dt : int
            The clock's tick rate
        """
        self.width  = width
        self.height = height
        self.engine = Engine(width, height)
        self.state  = State.MAIN
        self.dt     = dt
        self.FONT   = pygame.freetype.Font(
            "assets/fonts/momcake/MomcakeBold-WyonA.ttf", 24)
        self.background_color = (0, 250, 255)
        self.font_color       = (255, 100, 4)
        pygame.mixer.music.load("assets/music/menu.mp3")
        pygame.mixer.music.play()

    def update(self, events):
        """
        Updates the game.

        Parameters
        ----------
        events : list(pygame events)
            List of pygame events. Used for detecting key presses.
        """
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
        """
        Updates the main menu.

        Parameters
        ----------
        events : list(pygame events)
            List of pygame events. Used for detecting key presses.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.state = State.LEVEL_SELECT
                elif event.key == pygame.K_2:
                    self.state = State.CREDITS
                elif event.key == pygame.K_3:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def updateLevelSelect(self, events):
        """
        Updates the level select menu.

        Parameters
        ----------
        events : list(pygame events)
            List of pygame events. Used for detecting key presses.
        """
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
                elif event.key == pygame.K_6:
                    self.state = State.PLAYING
                    self.engine.loadLevel("assets/levels/secret.txt")
                    self.engine.reset()
                elif event.key == pygame.K_ESCAPE:
                    self.state = State.MAIN
    
    def updateCredits(self, events):
        """
        Updates the credits screen.

        Parameters
        ----------
        events : list(pygame events)
            List of pygame events. Used for detecting key presses.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = State.MAIN
    
    def updatePlaying(self, events):
        """
        Updates the gameplay engine.

        Parameters
        ----------
        events : list(pygame events)
            List of pygame events. Used for detecting key presses.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # return to main menu if escape is pressed at level
                    # complete screen
                    if self.engine.atLevelCompleteScreen():
                        self.state = State.MAIN
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("assets/music/menu.mp3")
                        pygame.mixer.music.play()
                    else:
                        self.state = State.PAUSED
                        pygame.mixer.music.pause()
        self.engine.update(self.dt)
    
    def updatePaused(self, events):
        """
        Updates the pause screen.

        Parameters
        ----------
        events : list(pygame events)
            List of pygame events. Used for detecting key presses.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_ESCAPE:
                    self.state = State.PLAYING
                    pygame.mixer.music.unpause()
                elif event.key == pygame.K_2:
                    self.state = State.MAIN
                    pygame.mixer.music.load("assets/music/menu.mp3")
                    pygame.mixer.music.play()

    def draw(self, screen):
        """
        Draws the current state onto the screen.

        Parameters
        ----------
        screen : pygame display surface
            The screen to draw onto
        """
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
        """
        Draws the main menu onto the screen.

        Parameters
        ----------
        screen : pygame display surface
            The screen to draw onto
        """
        screen.fill(self.background_color)
        self.drawTextXCenter(screen, "Super Square Boy 2", self.font_color,
            self.width / 10, self.height / 6, True)
        self.drawTextXCenter(screen, "1) Level Select", self.font_color,
            self.width / 17, self.height / 2 - self.height / 14)
        self.drawTextXCenter(screen, "2) Credits", self.font_color,
            self.width / 17, self.height / 2 + self.height / 14)
        self.drawTextXCenter(screen, "3) Exit Game", self.font_color,
            self.width / 17, self.height / 2 + self.height / 4.66)
    
    def drawLevelSelect(self, screen):
        """
        Draws the level select menu onto the screen.

        Parameters
        ----------
        screen : pygame display surface
            The screen to draw onto
        """
        screen.fill(self.background_color)
        self.drawTextXCenter(screen, "Level Select", self.font_color,
            self.width / 9, self.height / 6, True)
        self.drawTextXCenter(screen, "1) RPM", self.font_color,
            self.width / 18, self.height / 2 - self.height / 9.33)
        self.drawTextXCenter(screen, "2) Deep Blue", self.font_color,
            self.width / 18, self.height / 2)
        self.drawTextXCenter(screen, "3) Luminous", self.font_color,
            self.width / 18, self.height / 2 + self.height / 9.33)
        self.drawTextXCenter(screen, "4) Spectre", self.font_color,
            self.width / 18, self.height / 2 + self.height / 4.66)
        self.drawBackButton(screen)
    
    def drawCredits(self, screen):
        """
        Draws the credits screen.

        Parameters
        ----------
        screen : pygame display surface
            The screen to draw onto
        """
        screen.fill(self.background_color)
        self.drawTextXCenter(screen, "Credits", self.font_color,
            self.width / 10, self.height / 6, True)

        # personal information
        self.drawTextXCenter(screen, "Created by Alexander Marcozzi",
            self.font_color, self.width / 40, self.height / 6 + self.height / 9.33)
        self.drawTextXCenter(screen, "email: alex.marcozzi1_gmail.com",
            self.font_color, self.width / 40, self.height / 6 + self.height / 7)
        self.drawTextXCenter(screen, "github: github.com/alex-marcozzi",
            self.font_color, self.width / 40, self.height / 6 + self.height / 5.6)

        # music
        self.drawTextXCenter(screen, "Music", self.font_color, self.width / 17,
            self.height / 2 - self.height / 14)
        self.drawTextXCenter(screen, 
            "Main Menu: \"Away with the Fairies\" by Philanthrope",
                self.font_color, self.width / 24, self.height / 2)
        self.drawTextXCenter(screen, "Level 1: \"RPM\" by env",
            self.font_color, self.width / 24, self.height / 2 + self.height / 14)
        self.drawTextXCenter(screen, "Level 2: \"Deep Blue\" by K-391",
            self.font_color, self.width / 24, self.height / 2 + self.height / 7)
        self.drawTextXCenter(screen, "Level 3: \"Luminous\" by Lensko",
            self.font_color, self.width / 24, self.height / 2 + self.height / 4.66)
        self.drawTextXCenter(screen, "Level 4: \"Spectre\" by Alan Walker",
            self.font_color, self.width / 24, self.height / 2 + self.height / 3.5)
        self.drawTextXCenter(screen, "Level Complete: \"Synergy\" by AGST",
            self.font_color, self.width / 24, self.height / 2 + self.height / 2.79)

        self.drawBackButton(screen)
    
    def drawPlaying(self, screen):
        """
        Draws the state of the gameplay engine onto the screen.

        Parameters
        ----------
        screen : pygame display surface
            The screen to draw onto
        """
        screen.fill(self.background_color)
        self.engine.draw(screen)

    def drawPaused(self, screen):
        """
        Draws the pause screen.

        Parameters
        ----------
        screen : pygame display surface
            The screen to draw onto
        """
        screen.fill(self.background_color)
        self.drawTextXCenter(screen, "Paused", self.font_color, self.width / 6, self.height / 6, True)
        self.drawTextXCenter(screen, "1) Resume", self.font_color, self.width / 17, self.height / 2)
        self.drawTextXCenter(screen, "2) Main Menu", self.font_color, self.width / 17, self.height / 2 + self.height / 7)
    
    def drawTextXCenter(self, screen, text, color, size, y, underline = False):
        """
        Draws text of a specified size and color onto the screen, centered
        on the X axis and at the specified location on the Y axis.

        Parameters
        ----------
        screen : pygame display surface
            The screen to draw onto
        text : str
            The text to draw
        color : tuple(int)
            The color of the text, in RGB format
        size : int
            The size of the text
        y : int
            The location of the text on the Y axis (in pixels)
        underline : bool
            Whether the text should be underlined or not
        """
        self.FONT.underline = underline
        text_rect = self.FONT.get_rect(text, size = size)
        text_rect.center = (self.width / 2, y)
        self.FONT.render_to(screen, text_rect, text, color, size = size)
        self.FONT.underline = False
    
    def drawBackButton(self, screen):
        """
        Draws the back button onto the screen in the lower left corner.

        Parameters
        ----------
        screen : pygame display surface
            The screen to draw onto
        """
        text_rect = self.FONT.get_rect("ESC) Back", size = self.width / 40)
        text_rect.center = (self.width / 10, 9 * self.height / 10)
        self.FONT.render_to(screen, text_rect, "ESC) Back", self.font_color, size = self.width / 40)