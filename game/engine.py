import pygame
import pygame.freetype
import copy
from game.block  import Block
from game.player import Player
from game.frame  import Frame
from game.blocktype import BlockType

class Engine:
    """
    A class representing the game engine, handling moment-to-moment gameplay
    during levels.

    All "magic numbers" and formulas were acquired from manual testing.

    ...

    Attributes
    ----------
    width : int
        the width of the display, in pixels
    height : int
        the height of the display, in pixels
    block_size : int
        the side-length of each block, in pixels
    block_speed : list(float)
        the speed each block will move toward the player
    frame_length : int
        the length of the gameplay frame, in number of blocks
    frame_height : int
        the height of the gameplay frame, in pixels
    is_dead : bool
        whether the player is currently dead or not
    level_ended : bool
        whether the level has ended or not
    death_time : int
        the time when the player last died
    end_time : int
        the time when the player reached the end of the level
    ground_time : int
        the time when the player was last on the ground
    current_time : int
        the current time
    fade_duration : int
        the amount of time the fade transition should take (in milliseconds)
    fade_pct : float
        the percent the screen should be faded (0 being unfaded and 1 being 
        fully faded)
    attempts : int
        the current attempt the player is on
    FONT : pygame freetype font object
        the font to be rendered as text later
    death_sound : pygame mixer sound object
        the sound to be played when the player dies
    background_color : tuple(int)
        the color of the background in RGB format
    font_color : tuple(int)
        the color of the font in RGB format
    block_color : tuple(int)
        the color of the blocks in RGB format
    spike_color : tuple(int)
        the color of the spikes in RGB format
    player_img : str
        the file path of the player image
    player : Player
        the player's block object
    blockmap : list(list(Block))
        the entire level stored in blocks
    
    Methods
    -------
    update(dt)
        Updates the position of the block
    """
    def __init__(self, width, height):
        """
        Parameters
        ----------
        width : int
            The width of the display, in pixels
        height : int
            The height of the display, in pixels
        """
        self.width         = width
        self.height        = height
        self.block_size    = int(width / 30)
        self.block_speed   = [-(width / 2400.0), 0]
        self.frame_length  = int(width / self.block_size) + 1
        self.frame_height  = height - (height / 10)
        self.is_dead       = False
        self.level_ended   = False
        self.death_time    = -1
        self.end_time      = -1
        self.ground_time   = -1
        self.current_time  = -1
        self.fade_duration = 6150
        self.fade_pct      = 0.0
        self.attempts      = 1
        self.FONT          = pygame.freetype.Font(
                             "assets/fonts/momcake/MomcakeBold-WyonA.ttf", 48)
        self.death_sound   = pygame.mixer.Sound("assets/sfx/death.mp3")
    
    def loadMetaInfo(self, lines):
        """
        Loads the meta information of a level from the given lines into the
        engine.

        Example meta information (from level 1):
            0,250,255
            255,100,4
            0,0,0
            100,100,100
            assets/images/orange.png
            assets/music/music1.mp3

        Parameters
        ----------
        dt : int
            The clock's tick rate
        """
        self.background_color = tuple(float(s) for s in lines[0].split(','))
        self.font_color       = tuple(float(s) for s in lines[1].split(','))
        self.block_color      = tuple(float(s) for s in lines[2].split(','))
        self.spike_color      = tuple(float(s) for s in lines[3].split(','))
        self.player_img       = str(lines[4][:(len(lines[4])-1)])
        pygame.mixer.music.load(str(lines[5][:(len(lines[5])-1)]))

        
    def loadLevel(self, filepath):
        """
        Loads the level at the specified file path into the engine.

        The first six lines of the file should contain meta information for the
        level, including the background color, font color, block color, spike
        color, player image file path, and music file path, in that order, with
        all colors in RGB comma-separated format.

        The rest of the file should contain a combination of Os (normal
        blocks), Xs (spikes), and Es(end blocks), with each row of the file
        representing a column of the level.

        See one of the level text files in "assets/levels" for examples.

        Parameters
        ----------
        filepath : str
            The file path of the level
        """
        # read the file
        f = open(filepath, 'r')
        lines = f.readlines()

        # load the meta information and initialize the player
        self.loadMetaInfo(lines)
        self.player = Player(pygame.Rect(self.width / 6, self.height / 2, self.block_size,
                self.block_size), [0, 1], self.player_img)

        # initialize the level's block layout
        self.blockmap = [[Block(pygame.Rect(0, self.frame_height,
                self.block_size, self.block_size), self.block_speed,
                self.block_color, BlockType.BLOCK)]]

        # add one full frame worth of standard blocks before loading the level
        
        for i in range(1, self.frame_length):
            self.blockmap.append([Block(pygame.Rect(self.block_size * i,
                    self.frame_height, self.block_size * 1.1, self.block_size),
                    self.block_speed, self.block_color, BlockType.BLOCK)])

        # load the rest of the level
        for l in range(6, len(lines)):
            line = lines[l]
            line_blocks = []
            for i in range(len(line)):
                character = line[i]

                # load the regular blocks (the * 1.1 width helps smooth out
                # visual inconsistancies caused by framerate changes)
                if (character == 'O'):
                    line_blocks.append(Block(pygame.Rect(
                            self.block_size * (self.frame_length - 1),
                            self.frame_height - (self.block_size * i),
                            self.block_size * 1.1, self.block_size),
                            self.block_speed,
                            self.block_color, BlockType.BLOCK))

                # load the spikes (they are 25% shorter than other blocks for
                # balancing purposes and and overall better game-feel)
                if (character == 'X'):
                    line_blocks.append(Block(pygame.Rect(
                            self.block_size * (self.frame_length - 1),
                            (self.frame_height - (self.block_size * i)) + self.block_size * 0.25,
                            self.block_size, self.block_size * 0.75),
                            self.block_speed,
                            self.spike_color, BlockType.SPIKE))
                
                # load the end blocks
                if (character == 'E'):
                    line_blocks.append(Block(pygame.Rect(
                            self.block_size * (self.frame_length - 1),
                            self.frame_height - (self.block_size * i),
                            self.block_size, self.block_size),
                            self.block_speed,
                            self.block_color, BlockType.END))

            self.blockmap.append(line_blocks)
            self.attempts = 1

    def reset(self):
        #self.loadLevel("assets/levels/level1.txt")
        self.player = Player(pygame.Rect(self.width / 6, 8 * self.height / 10, self.block_size,
                self.block_size), [0, 1], self.player_img)
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
            self.fade_pct = (self.current_time - self.end_time) / self.fade_duration
        if self.atLevelCompleteScreen():
            return
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
            grounded = False
            for block in current_blocks:
                if Block.isOnTop(self.player, block):
                    if block.block_type == BlockType.SPIKE:
                        self.is_dead = True
                        pygame.mixer.Sound.play(self.death_sound)
                        pygame.mixer.music.stop()
                    elif block.block_type == BlockType.BLOCK:
                        grounded = True
                        self.ground_time = pygame.time.get_ticks()
                        self.player.speed[1] = 0
                        self.player.resetRotation()
                        Block.snapOnTop(self.player, block)
                    if keys[pygame.K_UP]:
                        self.player.jump()
                elif Block.isCollision(self.player, block):
                    if block.block_type == BlockType.END:
                        self.level_ended = True
                        pygame.mixer.music.load("assets/music/end.mp3")
                        pygame.mixer.music.play()
                    else:
                        self.is_dead = True
                        pygame.mixer.Sound.play(self.death_sound)
                        pygame.mixer.music.stop()

            if not grounded:
                if pygame.time.get_ticks() - self.ground_time >= 50:
                    self.player.rotate(-(dt / 3.2))
                else:
                    self.player.resetRotation()

    def draw(self, screen):
        if self.fade_pct >= 1:
                screen.fill((0,0,0))
                self.drawTextXCenter(screen, "Level Complete", (255,100,4), self.width / 12, self.height / 2)#100, self.height / 2)
                self.drawTextXCenter(screen, "ESC) Main Menu", (255,100,4), self.width / 40, 3 * self.height / 4)
        else:
            screen.fill([col * (1 - self.fade_pct) for col in self.background_color])
            if self.is_dead == False:
                self.player.draw(screen, self.fade_pct)
            self.frame.draw(screen, self.fade_pct)
            self.drawTextXCenter(screen, "Attempt   " + str(self.attempts), 
                [col * (1 - self.fade_pct) for col in self.font_color], 
                self.width / 25, self.height / 8)
            #self.FONT.render_to(screen, ((self.width / 2) - 100, self.height / 8), 
            #        "Attempt   " + str(self.attempts), [col * (1 - self.fade_pct) 
            #            for col in self.font_color])
    
    def drawTextXCenter(self, screen, text, color, size, y):
        text_rect = self.FONT.get_rect(text, size = size)
        text_rect.center = (self.width / 2, y)
        self.FONT.render_to(screen, text_rect, text, color, size = size)

    def atLevelCompleteScreen(self):
        return self.fade_pct >= 1