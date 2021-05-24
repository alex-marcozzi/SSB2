import pygame # maybe not necessary, take out?

class Frame:
    pos = 0
    def __init__(self, level, length):
        self.level = level
        self.length = length

    def update(self):
        for i in range(self.pos, min(self.pos + self.length, len(self.level) - 1)):
            for block in self.level[i]:
                block.update()

        if (self.level[self.pos][0].right() < 0):
            self.pos += 1

    def draw(self, screen):
        for i in range(self.pos, min(self.pos + self.length, len(self.level) - 1)):
            for block in self.level[i]:
                block.draw(screen)
