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
        return self.blockrect.left

    def right(self):
        return self.blockrect.right

    def top(self):
        return self.blockrect.top

    def bottom(self):
        return self.blockrect.bottom

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.blockrect)

    @staticmethod
    def isOnTop(block1, block2):
        if (block1.bottom() >= block2.top() and block1.bottom() <= block2.bottom()):
            if (block1.right() >= block2.left() and block1.right() <= block2.right()):
                return True
            if (block1.left() >= block2.left() and block1.left() <= block2.right()):
                return True
        return False

    @staticmethod
    def snapOnTop(block1, block2):
        distance = block1.bottom() - block2.top()
        block1.blockrect = block1.blockrect.move(0, -distance)

