import pygame
#pygame.init()

class Block:
    def __init__(self, blockrect, speed, color, is_spike):
        self.blockrect = blockrect
        self.speed     = speed
        self.color     = color
        self.is_spike  = is_spike

    def update(self, clock):
        #print(clock)
        self.blockrect = self.blockrect.move([int(self.speed[0] * clock), 
            int(self.speed[1] * clock)])

    def left(self):
        return self.blockrect.left

    def right(self):
        return self.blockrect.right

    def top(self):
        return self.blockrect.top

    def bottom(self):
        return self.blockrect.bottom

    def draw(self, screen):
        if (self.is_spike):
             pygame.draw.polygon(screen, self.color,
                     [[self.left(), self.bottom()], 
                         [int((self.left() + self.right()) / 2), self.top()],
                         [self.right(), self.bottom()]])
        else:
            pygame.draw.rect(screen, self.color, self.blockrect)

    @staticmethod
    def isOnTop(block1, block2):
        if block1.speed[1] < 0:
            return False

        #print(block1.bottom() - block2.top())
        #print((block2.bottom() - block2.top()) / 2)
        #print()
        if ((block2.is_spike == False and 
                abs(block1.bottom() - block2.top()) 
                <= (block2.bottom() - block2.top())/2) or
            (block2.is_spike and block1.bottom() >= block2.top() and 
                block1.bottom() <= block2.bottom())):
            #return False
        #if (block1.bottom() >= block2.top() and block1.bottom() <= block2.bottom()):
            if (block1.right() >= block2.left() and block1.right() <= block2.right()):
                return True
            if (block1.left() >= block2.left() and block1.left() <= block2.right()):
                return True
        return False

    @staticmethod
    def isCollision(block1, block2):
        #if (block1.bottom() >= block2.top() and block1.bottom() <= block2.bottom()):
        if abs(((block1.bottom() - block2.top()) 
                > (block2.bottom() - block2.top()) / 2) and 
                (abs(block1.bottom() - block2.top()) 
                    <= (block2.bottom() - block2.top()))):
            if (block1.right() >= block2.left() and block1.right() <= block2.right()):
                return True
            if (block1.left() >= block2.left() and block1.left() <= block2.right()):
                return True
        return False

    @staticmethod
    def snapOnTop(block1, block2):
        distance = block1.bottom() - block2.top()
        block1.blockrect = block1.blockrect.move(0, -distance)

