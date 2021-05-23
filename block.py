import pygame
#pygame.init()

class Block:
    def __init__(self, blockrect, speed, color):
        self.blockrect = blockrect
        self.speed     = speed
        self.color     = color

    def update(self):
        self.blockrect = self.blockrect.move(self.speed)

    def left(self):
        return(self.blockrect.left)

    def right(self):
        return(self.blockrect.right)

    def top(self):
        return(self.blockrect.top)

    def bottom(self):
        return(self.blockrect.bottom)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.blockrect)
