from block import Block

class Player(Block):
    def __init__(self, blockrect, speed, color):
        self.counter = 0
        Block.__init__(self, blockrect, speed, color)

    def update(self):
        Block.update(self)
        if (self.speed[1] < 10):
            if self.counter < 3:
                self.speed[1] += 1
            if self.counter >= 15:
                self.counter = 0
            self.counter += 1
            
    
    def jump(self):
        self.speed[1] = -10
        #print("called")
