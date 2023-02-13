import math
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
db = Database()


def render():
    screen.fill(bgCol)
    pygame.draw.circle(screen, containerCol, (res[0] // 2, res[1] // 2), res[1] // 2 - 5)

    for point in db.points:
        pygame.draw.circle(screen, point.col, point.pos, point.size)
    pygame.display.update()


def gravity():
    for point in db.points:
        point.pos = (point.pos[0], point.pos[1] + 1)  # can be adjusted to different value -> different gravity forces


# collision against the outside of the box
def detect_edge_collisions():
    pass



# add some air resistance, to (hopefully) make things stable
def air_resistance():
    for point in db.points:
        x = (point.pos[0] - point.previousPos[0]) * 0.95 + point.previousPos[0]
        y = (point.pos[1] - point.previousPos[1]) * 0.95 + point.previousPos[1]
        point.pos = (x, y)


def move_points():
    for point in db.points:
        previous = point.pos
        point.pos = ((point.pos[0] * 2) - point.previousPos[0], (point.pos[1] * 2) - point.previousPos[1])
        point.previousPos = previous


running = True
frames = 0
db.add_point(res[0] // 2, res[1] // 2)
while running:
    if frames == 100:
        render()
        gravity()
        detect_edge_collisions()
        air_resistance()
        move_points()
        frames = 0
    frames += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
