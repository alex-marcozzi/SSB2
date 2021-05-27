import pygame # maybe not necessary, take out?
from itertools import chain

class Frame:
    def __init__(self, blockmap, length):
        self.pos = 0
        self.blockmap = blockmap
        self.length = length

    def update(self, clock):
        for i in range(self.pos, min(self.pos + self.length, len(self.blockmap) - 1)):
            for block in self.blockmap[i]:
                block.update(clock)

        if (self.blockmap[self.pos][0].right() <= 0):
            self.pos += 1

    def draw(self, screen):
        for i in range(self.pos, min(self.pos + self.length, len(self.blockmap) - 1)):
            for block in self.blockmap[i]:
                block.draw(screen)

    def getRelevantBlocks(self):
        return list(chain.from_iterable(self.blockmap[self.pos+3:self.pos+int(self.length / 2)]))
