from game.block import Block

class Player(Block):
    def __init__(self, blockrect, speed, color):
        self.jump_height = 3
        self.max_speed = 2
        self.counter = 0
        Block.__init__(self, blockrect, speed, color, False)

    def update(self, clock):
        Block.update(self, clock)
        if (self.speed[1] < self.max_speed):
            #if self.counter < 2:
                #print("decreasing speed")
            #    self.speed[1] += 1
            #if self.counter >= self.jump_height:
            #    self.counter = 0
            #self.counter += 1
            self.speed[1] += 0.2
    
    def jump(self):
        if (self.speed[1] == 0):
            self.counter = 0
            self.speed[1] = -self.max_speed
        #print("called")
