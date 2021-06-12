# Title: player.py
# Description: Contains the Player class for Super Square Boy 2.
# Author: Alexander Marcozzi
# Date: 06/12/2021

import pygame
from game.block import Block
from game.blocktype import BlockType

class Player(Block):
    """
    A class representing the player. Inherits from Block.

    All "magic numbers" and formulas were acquired from manual testing.

    ...

    Attributes
    ----------
    max_speed : int
        the maximum speed achievable (essentially terminal velocity)
    base_image : pygame image surface
        the image representing the player
    total_angle : int
        the angle that the player's block should be rotate

    Methods
    -------
    update(dt)
        Updates the position of the player
    draw(screen, fade_pct)
        Draws the player onto the screen
    rotate(angle)
        Rotates the player clockwise a specified number of degrees
    resetRotation()
        Resets the player's rotation angle back to 0
    jump()
        Increases the player's vertical speed, simulating a jump
    """

    def __init__(self, blockrect, speed, image_path):
        """
        Parameters
        ----------
        blockrect : pygame.Rect
            A pygame rectangle object that holds the positional and spatial
            information of the block
        speed : float
            The speed at which the block will move in the X and Y directions
        image_path : str
            The file path of the player image
        """
        Block.__init__(self, blockrect, speed, (0,0,0), BlockType.BLOCK)
        self.max_speed = blockrect.width / 20
        self.base_image = pygame.image.load(image_path)
        self.base_image = pygame.transform.smoothscale(
            self.base_image, (blockrect.width, blockrect.height))
        self.total_angle = 0

    def update(self, dt):
        """
        Updates the position of the player.

        Each call, the player's vertical speed will be reduced, until a certain
        point, simulating gravity.

        Parameters
        ----------
        dt : int
            The clock's tick rate
        """
        Block.update(self, dt)
        if (self.speed[1] < self.max_speed):
            self.speed[1] += (dt / 3200.0) * self.blockrect.width  # gravity

    def draw(self, screen, fade_pct):
        """
        Draws the player onto the screen.

        Adjusts the image's alpha based on the passed in fade percentage.

        Parameters
        ----------
        screen : pygame display surface
            The screen to draw onto
        fade_pct : float
            The amount the block should appear faded. 0 being no fade and 1
            being fully faded
        """
        image = pygame.transform.rotate(self.base_image, self.total_angle)
        new_rect = image.get_rect(center = self.blockrect.center)
        image.set_alpha(255 * (1 - fade_pct))
        screen.blit(image, new_rect)

    def rotate(self, angle):
        """
        Rotates the player clockwise a specified number of degrees.

        Parameters
        ----------
        angle: int
            The angle the player should be rotated
        """
        self.total_angle += angle

    def resetRotation(self):
        """
        Resets the player's rotation angle back to 0.
        """
        self.total_angle = 0
    
    def jump(self):
        """
        Increases the player's vertical speed, simulating a jump.
        """
        self.speed[1] = -self.max_speed
