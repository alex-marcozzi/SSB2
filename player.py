from block import Block

class Player(Block):
    jump_height = 10
    def __init__(self, blockrect, speed, color):
        self.counter = 0
        Block.__init__(self, blockrect, speed, color)

    def update(self):
        Block.update(self)
        if (self.speed[1] < 10):
            if self.counter < 3:
                self.speed[1] += 1
            if self.counter >= self.jump_height:
                self.counter = 0
            self.counter += 1
            
    
    def jump(self):
        if (self.speed[1] == 0):
            self.counter = 0
            self.speed[1] = -10
        #print("called")
