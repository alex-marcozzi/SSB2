import pygame
import copy
from game.block  import Block
from game.player import Player
from game.frame  import Frame

class Engine:
    #State = Enum('State', 'home credits playing paused')
    #current_state = State.playing
    def __init__(self, width, height):
        self.is_dead         = False
        self.block_size      = 40#80
        self.block_speed     = [-0.5, 0]
        self.block_color     = (150, 150, 150)
        self.running_speed   = 5
        self.running_counter = 0
        self.max_counter     = 5
        self.frame_length    = int(width / self.block_size) + 2  # number of squares
        #self.frame_length = 12
        #print(self.frame_length)
        self.frame_height    = height - 100  # number of pixels
        self.player_color    = (255, 0, 0)
        self.player = Player(pygame.Rect(200, 200, self.block_size,
                self.block_size), [0, 1], self.player_color) 

    def loadLevel(self, filepath):
        # initialize the level's block layout
        self.blockmap = [[Block(pygame.Rect(0, self.frame_height,
                self.block_size, self.block_size), self.block_speed,
                self.block_color, False)]]

        for i in range(1, self.frame_length):
            self.blockmap.append([Block(pygame.Rect(self.block_size * i,
                    self.frame_height, self.block_size, self.block_size),
                    self.block_speed, self.block_color, False)])

        f = open(filepath, 'r')
        lines = f.readlines()
        for line in lines:
            line_blocks = []
            for i in range(len(line)):
                #print(count)
                #count += 1
                character = line[i]
                # load the regular blocks
                if (character == 'O'):
                    line_blocks.append(Block(pygame.Rect(
                            self.block_size * (self.frame_length - 1),
                            self.frame_height - (self.block_size * i),
                            self.block_size, self.block_size),
                            self.block_speed,
                            self.block_color, False))
                if (character == 'X'):
                    line_blocks.append(Block(pygame.Rect(
                            self.block_size * (self.frame_length - 1),
                            (self.frame_height - (self.block_size * i)) + self.block_size * 0.25,
                            self.block_size, self.block_size * 0.75),
                            self.block_speed,
                            (255, 255, 255), True))


            self.blockmap.append(line_blocks)

    def reset(self):
        #self.loadLevel("assets/levels/level1.txt")
        self.player = Player(pygame.Rect(200, 200, self.block_size,
                self.block_size), [0, 1], self.player_color)
        self.frame = Frame(copy.deepcopy(self.blockmap), self.frame_length)

        self.is_dead = False

    def update(self, clock):
        #print(self.player.top())
        keys = pygame.key.get_pressed()
        #self.running_counter += 1
        #if (self.running_counter <= self.running_speed):
        self.player.update(clock)
        self.frame.update(clock)
        current_blocks = self.frame.getRelevantBlocks()
        for block in current_blocks:
            if Block.isOnTop(self.player, block):
                if block.is_spike:
                    self.is_dead = True
                    #self.reset()
                self.player.speed[1] = 0
                Block.snapOnTop(self.player, block)
                if keys[pygame.K_UP]:
                    self.player.jump()
        #elif (self.running_counter >= self.max_counter):
        #    self.running_counter = 0

        #player.update()
        #frame.update()

    def draw(self, screen):
        #blockmap_copy = self.blockmap.copy()
        #frame = Frame(blockmap_copy, self.frame_length)

        #screen.fill((0, 0, 0))  # maybe shouldn't be here?
        if self.is_dead == False:
            self.player.draw(screen)
        self.frame.draw(screen)
            
    # we need a level engine to keep track of playing a level
    # but we also need an overall engine to handle the menus and stuff
