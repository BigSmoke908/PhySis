import math


class Database:
    points = None
    connections = None  # connection = (p1, p2, length)
    # -> length = length when the connection was created -> trying to get to that length if not that length rn

    # TODO: add method to load an already existing database from a file + save the current db to a file
    def __init__(self, file='None'):
        self.points = []
        self.connections = []

    def add_point(self, x, y, fixed=False, visible=True):
        self.points.append(Point(x, y, fixed, visible))

    def remove_point(self, i):
        self.points.pop(i)

        for connection in self.connections:
            if i == connection[0] or i == connection[1]:
                self.connections.remove(connection)

    def add_connection(self, p1, p2, rope=False):
        if not rope or self.point_distance(p1, p2) < 10:  # just connect these 2 points
            self.connections.append((p1, p2, self.point_distance(p1, p2)))
        else:  # we create points between the 2 points and link those together -> connection looks like an actual rope
            length = self.point_distance(p1, p2) * 0.7
            vec = ((self.points[p2].Pos[0] - self.points[p1].Pos[0]) / length, (self.points[p2].Pos[1] - self.points[p1].Pos[1]) / length)

            for i in range(int(length//30)):
                self.add_point(self.points[p1].Pos[0] + vec[0] * i * 30, self.points[p1].Pos[1] + vec[1] * i * 30, visible=False)
                if i == 0:
                    self.connections.append((p1, len(self.points) - 1, self.point_distance(p1, -1)))
                else:
                    self.connections.append((len(self.points) - 2, len(self.points) - 1, self.point_distance(-2, -1)))
            self.connections.append((len(self.points) - 1, p2, self.point_distance(p2, -1)))

    def point_distance(self, p1, p2):
        return math.sqrt(((self.points[p1].Pos[0] - self.points[p2].Pos[0]) ** 2) + ((self.points[p1].Pos[1] - self.points[p2].Pos[1]) ** 2))


class Point:
    Pos = None
    previousPos = None
    fixed = False
    visible = True

    def __init__(self, x, y, fixed=False, visible=True):
        self.Pos = (x, y)
        self.previousPos = (x, y)
        self.fixed = fixed
        self.visible = visible
