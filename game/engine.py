import pygame
import pygame.freetype
import copy
from game.block  import Block
from game.player import Player
from game.frame  import Frame
from game.blocktype import BlockType

class Engine:
    #State = Enum('State', 'home credits playing paused')
    #current_state = State.playing
    def __init__(self, width, height):
        self.width           = width
        self.height          = height
        self.is_dead         = False
        self.level_ended     = False
        self.block_size      = 40#80
        self.block_speed     = [-0.50, 0]
        self.running_speed   = 5
        self.running_counter = 0
        self.max_counter     = 5
        self.frame_length    = int(width / self.block_size) + 1  # number of squares
        #self.frame_length = 12
        #print(self.frame_length)
        self.frame_height    = height - 100  # number of pixels
        self.death_time   = -1
        self.end_time     = -1
        self.ground_time  = -1
        self.current_time = -1
        self.fade_time    = 3000
        self.fade_pct = 0.0
        self.attempts  = 1
        self.FONT = pygame.freetype.Font(
                "assets/fonts/momcake/MomcakeBold-WyonA.ttf", 48)
        self.death_sound = pygame.mixer.Sound("assets/sfx/death.mp3")
    
    def loadMetaInfo(self, lines):
        self.background_color = tuple(float(s) for s in lines[0].split(','))
        self.player_color     = tuple(float(s) for s in lines[1].split(','))
        self.block_color      = tuple(float(s) for s in lines[2].split(','))
        self.spike_color      = tuple(float(s) for s in lines[3].split(','))
        self.player_img       = lines[4][:(len(lines[4])-1)]
        pygame.mixer.music.load(lines[5][:(len(lines[5])-1)])

    def loadLevel(self, filepath):
        f = open(filepath, 'r')
        lines = f.readlines()
        self.loadMetaInfo(lines)
        self.player = Player(pygame.Rect(200, 200, self.block_size,
                self.block_size), [0, 1], self.player_color) 
        # initialize the level's block layout
        self.blockmap = [[Block(pygame.Rect(0, self.frame_height,
                self.block_size, self.block_size), self.block_speed,
                self.block_color, BlockType.BLOCK)]]

        for i in range(1, self.frame_length):
            self.blockmap.append([Block(pygame.Rect(self.block_size * i,
                    self.frame_height, self.block_size, self.block_size),
                    self.block_speed, self.block_color, BlockType.BLOCK)])

        for l in range(6, len(lines)):
            line = lines[l]
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
                            self.block_color, BlockType.BLOCK))
                if (character == 'X'):
                    line_blocks.append(Block(pygame.Rect(
                            self.block_size * (self.frame_length - 1),
                            (self.frame_height - (self.block_size * i)) + self.block_size * 0.25,
                            self.block_size, self.block_size * 0.75),
                            self.block_speed,
                            self.spike_color, BlockType.SPIKE))
                if (character == 'E'):
                    line_blocks.append(Block(pygame.Rect(
                            self.block_size * (self.frame_length - 1),
                            self.frame_height - (self.block_size * i),
                            self.block_size, self.block_size),
                            self.block_speed,
                            self.block_color, BlockType.END))



            self.blockmap.append(line_blocks)

    def reset(self):
        #self.loadLevel("assets/levels/level1.txt")
        self.player = Player(pygame.Rect(200, 200, self.block_size,
                self.block_size), [0, 1], self.player_color)
        self.frame = Frame(copy.deepcopy(self.blockmap), self.frame_length)

        self.is_dead      = False
        self.level_ended  = False
        self.death_time   = -1
        self.end_time     = -1
        self.ground_time  = -1
        self.current_time = -1
        self.fade_pct     = 0.0

        pygame.mixer.music.rewind()
        pygame.mixer.music.play()

    def update(self, dt):
        if (self.level_ended):
            self.current_time = pygame.time.get_ticks()
            if self.end_time == -1:
                self.end_time = self.current_time
            self.fade_pct = (self.current_time - self.end_time) / self.fade_time
            if self.fade_pct > 1:
                self.reset()
                self.attempts = 1
                return(True)
        # small pause after death before resetting
        if (self.is_dead):
            self.current_time = pygame.time.get_ticks()
            if self.death_time == -1:
                self.death_time = pygame.time.get_ticks()
            if self.current_time - self.death_time >= 2000:
                self.reset()
                self.attempts += 1
        else:
            keys = pygame.key.get_pressed()
            self.player.update(dt)
            self.frame.update(dt)
            current_blocks = self.frame.getRelevantBlocks()
            for block in current_blocks:
                if Block.isOnTop(self.player, block):
                    if block.block_type == BlockType.SPIKE:
                        self.is_dead = True
                        pygame.mixer.Sound.play(self.death_sound)
                        pygame.mixer.music.stop()
                    elif block.block_type == BlockType.BLOCK:
                        self.ground_time = pygame.time.get_ticks()
                        self.player.speed[1] = 0
                        self.player.resetRotation()
                        Block.snapOnTop(self.player, block)
                    if keys[pygame.K_UP]:
                        self.player.jump()
                elif Block.isCollision(self.player, block):
                    if block.block_type == BlockType.END:
                        self.level_ended = True
                    else:
                        self.is_dead = True
                        pygame.mixer.Sound.play(self.death_sound)
                        pygame.mixer.music.stop()
                else:
                    if pygame.time.get_ticks() - self.ground_time >= 50:
                        self.player.rotate(-0.5)
                    else:
                        self.player.resetRotation()

        return(False)

    def draw(self, screen):
        #blockmap_copy = self.blockmap.copy()
        #frame = Frame(blockmap_copy, self.frame_length)

        screen.fill([col * (1 - self.fade_pct) for col in self.background_color])#self.background_color)
        if self.is_dead == False:
            self.player.draw(screen, self.fade_pct)
        self.frame.draw(screen, self.fade_pct)
        self.FONT.render_to(screen, ((self.width / 2) - 100, self.height / 5), 
                "Attempt   " + str(self.attempts), [col * (1 - self.fade_pct) 
                    for col in self.player_color])
