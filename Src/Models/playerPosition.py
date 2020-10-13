from Src.Models.vector2 import Vector2

class PlayerPosition:
    '''
    This class represents the positions of each body part of a player.
    '''

    def __init__(self, h=Vector2(), n=[], b=[]):
        self.Head = h # (x,y)
        self.Neck = n # [(x1,y1), (x2,y2)...]
        self.Body = b # [(x1,y1), (x2,y2)...]
