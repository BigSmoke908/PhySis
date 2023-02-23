import math
import random


class Database:
    points = None

    # TODO: add feature to load/save database from file
    def __init__(self, file='noFile'):
        self.points = []

    def add_point(self, x, y, size=10, col=(200, 200, 200)):
        self.points.append(Point(x, y, size, col))

    def remove_point(self, i):
        self.points.pop(i)


class Point:
    pos = None
    previousPos = None
    size = None
    col = None
    trail = None  # the last eight positions of the point + color at that moment

    def __init__(self, x, y, s, col):
        self.pos = (x, y)
        self.previousPos = (x - random.randrange(-12, 13), y - random.randrange(-12, 13))
        # self.previousPos = self.pos
        self.size = s
        self.col = col
        self.trail = []

    def get_col(self):
        '''
        # random colors
        r = max(min(self.col[0] - random.randrange(0, 11) + 5, 50), 0)
        g = max(min(self.col[1] - random.randrange(0, 11) + 5, 50), 0)
        b = max(min(self.col[2] - random.randrange(0, 11) + 5, 50), 0)
        '''
        # speedbased color (faster = lighter glow)
        x = 1 / (1 + 2 ** -(((self.pos[0] - self.previousPos[0]) ** 2 + (self.pos[1] - self.previousPos[1]) ** 2) - 1))
        r = x * 255
        g = (x * 2) ** 7
        b = 10
        self.col = (r, g, b)
        return self.col

    def move(self):
        previous = self.pos
        self.pos = ((self.pos[0] * 2) - self.previousPos[0], (self.pos[1] * 2) - self.previousPos[1])
        self.previousPos = previous

        if (((self.pos[0] - self.previousPos[0]) ** 2) + ((self.pos[1] - self.previousPos[1]) ** 2)) > 900:
            self.trail.append((self.pos, self.col, self.size))
            self.size -= 0.00000001 * (((self.pos[0] - self.previousPos[0]) ** 2) + ((self.pos[1] + self.previousPos[1]) ** 2))
            if len(self.trail) > 20:
                self.trail.pop(0)
            return
        if len(self.trail) > 0:
            self.trail.pop(0)
