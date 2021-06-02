import pygame
import copy
from game.block import Block
from game.blocktype import BlockType

class Player(Block):
    def __init__(self, blockrect, speed, color):
        self.jump_height = 3
        self.max_speed = 2
        self.counter = 0
        #self.image = pygame.image.load("assets/images/square.png")#.convert()
        #self.base_image = self.image.copy()
        self.base_image = pygame.image.load("assets/images/orange.png")#.convert()
        Block.__init__(self, blockrect, speed, color, BlockType.BLOCK)
        self.total_angle = 0

    def update(self, clock):
        Block.update(self, clock)
        if (self.speed[1] < self.max_speed):
            self.speed[1] += 0.2

    def rotate(self, angle):
        self.total_angle += angle

    def resetRotation(self):
        self.total_angle = 0
        #self.image = self.base_image.copy()

    def draw(self, screen, fade_pct):
        #self.image = pygame.transform.rotate(self.base_image, self.total_angle)
        image = pygame.transform.rotate(self.base_image, self.total_angle)
        new_rect = image.get_rect(center = self.blockrect.center)
        image.set_alpha(255 * (1 - fade_pct))
        screen.blit(image, new_rect)
    
    def jump(self):
        if (self.speed[1] == 0):
            self.counter = 0
            self.speed[1] = -self.max_speed
