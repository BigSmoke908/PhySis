class Database:
    points = None

    # TODO: add feature to load/save database from file
    def __init__(self, file='noFile'):
        self.points = []

    def add_point(self, x, y, size=10, col=(200, 200, 200)):
        self.points.append(Point(x, y, size, col))


class Point:
    pos = None
    previousPos = None
    size = None
    col = None

    def __init__(self, x, y, s, col):
        self.pos = (x, y)
        self.previousPos = (x, y)
        self.size = s
        self.col = col
