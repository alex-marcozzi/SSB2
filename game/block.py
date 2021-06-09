import pygame
from game.blocktype import BlockType
#pygame.init()

class Block:

    def __init__(self, blockrect, speed, color, block_type):
        self.blockrect  = blockrect
        self.speed      = speed
        self.color      = color
        self.block_type = block_type

    def update(self, dt):
        self.blockrect = self.blockrect.move([int(self.speed[0] * dt), 
            int(self.speed[1] * dt)])

    def left(self):
        return self.blockrect.left

    def right(self):
        return self.blockrect.right

    def top(self):
        return self.blockrect.top

    def bottom(self):
        return self.blockrect.bottom

    def draw(self, screen, fade_pct):
        #print([col * (1 - fade_pct) for col in self.color])
        if (self.block_type is BlockType.SPIKE):
             pygame.draw.polygon(screen, 
                     [col * (1 - fade_pct) for col in self.color],#self.color,
                     [[self.left(), self.bottom()], 
                         [int((self.left() + self.right()) / 2), self.top()],
                         [self.right(), self.bottom()]])
        elif (self.block_type is BlockType.BLOCK):
            pygame.draw.rect(screen, [col * (1 - fade_pct) for col in self.color],#self.color,
                    self.blockrect)

    @staticmethod
    def isOnTop(block1, block2):
        if block1.speed[1] < 0:
            return False

        if ((block2.block_type != BlockType.SPIKE and 
                abs(block1.bottom() - block2.top()) 
                <= (block2.bottom() - block2.top())/2) or
            (block2.block_type == BlockType.SPIKE and block1.bottom() >= block2.top() and 
                block1.bottom() <= block2.bottom())):
            if (block1.right() >= block2.left() and block1.right() <= block2.right()):
                return True
            if (block1.left() >= block2.left() and block1.left() <= block2.right()):
                return True
        return False

    @staticmethod
    def isCollision(block1, block2):
        if (((block1.bottom() - block2.top()) 
                > (block2.bottom() - block2.top()) / 2) and 
                ((block1.bottom() - block2.top()) 
                    <= (block2.bottom() - block2.top()))):# or
                #(((block1.top() - block2.top()) 
                #> (block2.bottom() - block2.top()) / 2) and 
                #((block1.top() - block2.top()) 
                #    < (block2.bottom() - block2.top())))):
            if (block1.right() >= block2.left() and block1.right() <= block2.right()):
                return True
            if (block1.left() >= block2.left() and block1.left() <= block2.right()):
                return True
        return False

    @staticmethod
    def snapOnTop(block1, block2):
        distance = block1.bottom() - block2.top()
        block1.blockrect = block1.blockrect.move(0, -distance)

