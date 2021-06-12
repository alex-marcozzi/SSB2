from itertools import chain

class Frame:
    """
    A class representing the frame where gameplay takes place.

    Essentially, the entire level is stored and blocks will "become active" and
    enter the gameplay frame as the player progresses.

    ...

    Attributes
    ----------
    blockmap : list(list(Block))
        the entire level stored in blocks
    length : int
        the length of the frame (number of blocks in the frame horizontally)
    pos : int
        the position of the frame, in terms of blocks from the start
    
    Methods
    -------
    update(dt):
        Updates the position of each block currently in the frame
    draw(screen, fade_pct):
        Draws each block currently in the frame onto the screen
    getRelevantBlocks():
        Gets all blocks that could potentially interact with the player
    """

    def __init__(self, blockmap, length):
        """
        Parameters
        ----------
        blockmap : list(list(Block))
            The entire level stored in blocks
        length : int
            The length of the frame (number of blocks in the frame 
            horizontally)
        """
        self.blockmap = blockmap
        self.length   = length
        self.pos      = 0

    def update(self, dt):
        """
        Updates the position of each block currently in the frame.

        Parameters
        ----------
        dt : int
            The clock's tick rate
        """
        for i in range(self.pos, min(self.pos + self.length, len(self.blockmap))):
            for block in self.blockmap[i]:
                block.update(dt)

        # once the leftmost block goes out of frame, shift the frame over one
        if (self.blockmap[self.pos][0].right() <= 0):
            self.pos += 1

    def draw(self, screen, fade_pct):
        """
        Draws each block currently in the frame onto the screen.

        Parameters
        ----------
        screen : pygame display surface
            The screen to draw onto
        fade_pct : float
            The amount the block should appear faded. 0 being no fade and 1
            being fully faded
        """
        for i in range(self.pos, min(self.pos + self.length, len(self.blockmap))):
            for block in self.blockmap[i]:
                    block.draw(screen, fade_pct)

    def getRelevantBlocks(self):
        """
        Gets all blocks that could potentially interact with the player.
        """
        # check more than necessary to ensure nothing is missed
        return list(chain.from_iterable(self.blockmap[
            self.pos+3:self.pos+int(self.length / 2)]))