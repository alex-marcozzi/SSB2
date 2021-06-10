import pygame
import copy
from game.block import Block
from game.blocktype import BlockType

class Player(Block):
    def __init__(self, blockrect, speed, image_path):
        self.jump_height = 3
        self.max_speed = 2
        self.base_image = pygame.image.load(image_path)#"assets/images/orange.png")
        Block.__init__(self, blockrect, speed, (0,0,0), BlockType.BLOCK)
        self.total_angle = 0

    def update(self, dt):
        Block.update(self, dt)
        #print(dt / 80.0)
        if (self.speed[1] < self.max_speed):
            self.speed[1] += dt / 80.0#0.2

    def rotate(self, angle):
        self.total_angle += angle

    def resetRotation(self):
        self.total_angle = 0

    def draw(self, screen, fade_pct):
        image = pygame.transform.rotate(self.base_image, self.total_angle)
        new_rect = image.get_rect(center = self.blockrect.center)
        image.set_alpha(255 * (1 - fade_pct))
        screen.blit(image, new_rect)
    
    def jump(self):
        if (self.speed[1] == 0):
            self.counter = 0
            self.speed[1] = -self.max_speed
