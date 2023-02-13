import math
import random

import pygame
from db import Database


pygame.init()
UHD = (3840, 2160)
WQHD = (2560, 1440)
FHD = (1920, 1080)
res = FHD
screen = pygame.display.set_mode(res)
bgCol = (25, 25, 25)
containerCol = (0, 0, 0)
containerSize = res[1] // 2 - 5
containerPos = (res[0] // 2, res[1] // 2)
db = Database()


def render():
    screen.fill(bgCol)
    pygame.draw.circle(screen, containerCol, (res[0] // 2, res[1] // 2), containerSize)

    for point in db.points:
        pygame.draw.circle(screen, point.col, point.pos, point.size)
    pygame.display.update()


def gravity():
    for point in db.points:
        point.pos = (point.pos[0], point.pos[1] + 0.1)  # can be adjusted to different value -> different gravity forces


# collision against the outside of the box
def detect_edge_collisions():
    for point in db.points:
        if distance_to_center(point) > containerSize - point.size:  # then put the point to the next valid position
            x = point.pos[0] - containerPos[0]
            y = point.pos[1] - containerPos[1]
            point.pos = ((x * (containerSize - point.size)) / math.sqrt(x ** 2 + y ** 2) + containerPos[0], (y * (containerSize - point.size)) / math.sqrt(x ** 2 + y ** 2) + containerPos[1])


def detect_point_collision():
    for i, point1 in enumerate(db.points):
        for j, point2 in enumerate(db.points):
            if i < j:  # one point should not collide against itself
                if point_distance(point1, point2) < (point1.size + point2.size):
                    needed_distance = (point1.size + point2.size - point_distance(point1, point2))/2  # how far each point has to be moved
                    x = point2.pos[0] - point1.pos[0]
                    y = point2.pos[1] - point1.pos[1]
                    point1.pos = ((-(x * needed_distance) / math.sqrt(x ** 2 + y ** 2)) + point1.pos[0], (-(y * needed_distance) / math.sqrt(x ** 2 + y ** 2)) + point1.pos[1])
                    point2.pos = (((x * needed_distance) / math.sqrt(x ** 2 + y ** 2)) + point2.pos[0], ((y * needed_distance) / math.sqrt(x ** 2 + y ** 2)) + point2.pos[1])


def distance_to_center(point):
    return length(point.pos[0] - containerPos[0], point.pos[1] - containerPos[1])


# distance between the centers of the two points
def point_distance(point1, point2):
    return length(point1.pos[0] - point2.pos[0], point1.pos[1] - point2.pos[1])


def length(x, y):
    return math.sqrt(x ** 2 + y ** 2)


# add some air resistance, to (hopefully) make things stable
def air_resistance():
    for point in db.points:
        x = (point.pos[0] - point.previousPos[0]) * 0.99 + point.previousPos[0]
        y = (point.pos[1] - point.previousPos[1]) * 0.99 + point.previousPos[1]
        point.pos = (x, y)


def move_points():
    for point in db.points:
        previous = point.pos
        point.pos = ((point.pos[0] * 2) - point.previousPos[0], (point.pos[1] * 2) - point.previousPos[1])
        point.previousPos = previous


running = True
frames = 0
num = 0
while running:
    if frames == 10000:
        gravity()
        air_resistance()
        for i in range(1):
            detect_edge_collisions()
            detect_point_collision()
        move_points()
        render()
        frames = 0

        if num % 50 == 0:
            db.add_point(containerPos[0] + 400, containerPos[1] - 400, size=random.randrange(10, 40), col=(random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256)))
            if len(db.points) == 75:
                db.remove_point(0)
            num = 0
        num += 1
    frames += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
