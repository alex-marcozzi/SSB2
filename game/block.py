import pygame
from game.blocktype import BlockType

class Block:
    """
    A class representing a block. See BlockType for the different types.

    ...

    Attributes
    ----------
    blockrect : pygame.Rect
        a pygame rectangle object that holds the positional and spatial
        information of the block
    speed : float
        the speed at which the block will move
    color : tuple(int)
        the color of the block in RGB format
    block_type: BlockType
        the type of the block
    
    Methods
    -------
    update(dt)
        Updates the position of the block
    draw(screen, fade_pct)
        Draws the block on the screen
    left()
        Returns the position of the left side of the block
    right()
        Returns the position of the right side of the block
    top()
        Returns the position of the top side of the block
    bottom()
        Returns the position of the bottom side of the block
    isOnTop(block1, block2)
        Decides whether the first block is on top of the second
    isCollision(block1, block2)
        Decides whether the first block has collided with the second
    snapOnTop(block1, block2)
        Moves the first block to be on top of the second
    """

    def __init__(self, blockrect, speed, color, block_type):
        """
        Parameters
        ----------
        blockrect : pygame.Rect
            A pygame rectangle object that holds the positional and spatial
            information of the block
        speed : float
            The speed at which the block will move
        color : tuple(int)
            The color of the block in RGB format
        block_type: BlockType
            The type of the block
        """

        self.blockrect  = blockrect
        self.speed      = speed
        self.color      = color
        self.block_type = block_type

    def update(self, dt):
        """
        Updates the position of the block.

        This is done by using the stored speed of the block and adjusting it 
        based on the clock's tick rate in order to achieve a constant movement
        speed independent of the FPS of the game.

        Parameters
        ----------
        dt : int
            The clock's tick rate
        """

        # use the pygame.Rect's move function on adjusted speed values
        self.blockrect = self.blockrect.move([int(self.speed[0] * dt), 
            int(self.speed[1] * dt)])
    
    def draw(self, screen, fade_pct):
        """
        Draws the block on the screen.

        Adjusts the colors based on the passed in fade percentage.

        Parameters
        ----------
        screen : pygame display surface
            The screen to draw onto
        fade_pct : float
            The amount the block should appear faded. 0 being no fade and 1
            being fully faded
        """

        if (self.block_type is BlockType.SPIKE):
            # draw a triangle to represent the spike
            pygame.draw.polygon(screen, 
                    [col * (1 - fade_pct) for col in self.color], # fade colors
                    [
                        [self.left(), self.bottom()], 
                        [int((self.left() + self.right()) / 2), self.top()],
                        [self.right(), self.bottom()]
                    ])
        elif (self.block_type is BlockType.BLOCK):
            # draw the block
            pygame.draw.rect(screen, [col * (1 - fade_pct) for col in self.color],
                    self.blockrect)

    def left(self):
        """
        Returns the position of the left side of the block
        """
        return self.blockrect.left

    def right(self):
        """
        Returns the position of the right side of the block
        """
        return self.blockrect.right

    def top(self):
        """
        Returns the position of the top side of the block
        """
        return self.blockrect.top

    def bottom(self):
        """
        Returns the position of the bottom side of the block
        """
        return self.blockrect.bottom

    @staticmethod
    def isOnTop(block1, block2):
        """
        Decides whether the first block is on top of the second.

        Spikes behave differently than regular blocks in order to prevent
        unfair deaths.

        Parameters
        ----------
        block1 : Block
            The first block
        block2 : Block
            The second block
        """
        # if the block is rising, it can't be on top of something
        if block1.speed[1] < 0:
            return False

        # if the block is not a spike, there is a block-sized window where
        # block1 is considered ontop of block2. this tolerance is to prevent
        # falling through blocks at higher speeds. if it is a spike, we want
        # to be exact to prevent unfair deaths
        if ((block2.block_type != BlockType.SPIKE and 
                abs(block1.bottom() - block2.top()) 
                <= (block2.bottom() - block2.top())/2) or
            (block2.block_type == BlockType.SPIKE and 
                block1.bottom() >= block2.top() and 
                block1.bottom() <= block2.bottom())):
            # the blocks must be vertically alligned in order to be stacked
            if (block1.right() >= block2.left() and block1.right() <= block2.right()):
                return True
            if (block1.left() >= block2.left() and block1.left() <= block2.right()):
                return True
        return False

    @staticmethod
    def isCollision(block1, block2):
        """
        Decides whether the first block has collided with the second

        Parameters
        ----------
        block1 : Block
            The first block
        block2 : Block
            The second block
        """

        # if the bottom of the first block hits the bottom half of the
        # second block, it is considered a collision rather than being
        # on top
        if (((block1.bottom() - block2.top()) 
                > (block2.bottom() - block2.top()) / 2) and 
                ((block1.bottom() - block2.top()) 
                    <= (block2.bottom() - block2.top()))):
            # the blocks must be vertically alligned in order to collide
            if (block1.right() >= block2.left() and block1.right() <= block2.right()):
                return True
            if (block1.left() >= block2.left() and block1.left() <= block2.right()):
                return True
        return False

    @staticmethod
    def snapOnTop(block1, block2):
        """
        Moves the first block to be on top of the second

        Parameters
        ----------
        block1 : Block
            The first block
        block2 : Block
            The second block
        """

        distance = block1.bottom() - block2.top()
        block1.blockrect = block1.blockrect.move(0, -distance)