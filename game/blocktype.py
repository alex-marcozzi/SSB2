# Title: blocktype.py
# Description: Contains the BlockType enum class for Super Square Boy 2.
# Author: Alexander Marcozzi
# Date: 06/12/2021

from enum import Enum

class BlockType(Enum):
    """
    An enum class representing block types.

    ...

    Attributes
    ----------
    BLOCK : int
        a standard block that the player can travel on
    SPIKE : int
        a spike block that can kill the player
    END : int
        an end block that triggers the completion of a level
    """
    
    BLOCK = 1
    SPIKE = 2
    END   = 3