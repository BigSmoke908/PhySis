import math
import random
import pygame
from db import Database
from render_png import create_png


pygame.init()
UHD = (3840, 2160)
WQHD = (2560, 1440)
FHD = (1920, 1080)
res = FHD
screen = pygame.display.set_mode(res)
bgCol = (10, 10, 13)
containerCol = (0, 0, 0)
containerSize = res[1] // 2 - 5
containerPos = (res[0] // 2, res[1] // 2)
db = Database()


# can also create a png instead of rendering to pygame
def render(to_png=False, file=None):
    screen.fill(bgCol)
    pygame.draw.circle(screen, containerCol, containerPos, containerSize)

    for p, point in enumerate(db.points):
        if point.size <= 0:
            db.remove_point(p)
            continue
        pygame.draw.circle(screen, point.get_col(), point.pos, point.size)

        for ind, t in enumerate(point.trail):
            pygame.draw.circle(screen, t[1], t[0], t[2] * ind / (len(point.trail) * 2))
    pygame.display.update()

    if to_png:
        create_png(db, file, res, containerCol, containerPos, containerSize, bgCol)


def gravity():
    for point in db.points:
        point.pos = (point.pos[0], point.pos[1] + 0.1)  # can be adjusted to different value -> different gravity forces


def centergravity():
    for point in db.points:
        point.pos = ((containerPos[0] - point.pos[0]) / 300 + point.pos[0], (containerPos[1] - point.pos[1]) / 300 + point.pos[1])


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
                x = point2.pos[0] - point1.pos[0]
                y = point2.pos[1] - point1.pos[1]
                d = length(x, y)
                if d < (point1.size + point2.size):
                    needed_distance = (point1.size + point2.size - d)/2  # how far each point has to be moved
                    vec = ((x * needed_distance) / d, (y * needed_distance) / d)
                    point1.pos = (-vec[0] + point1.pos[0], -vec[1] + point1.pos[1])
                    point2.pos = (vec[0] + point2.pos[0], vec[1] + point2.pos[1])


def distance_to_center(point):
    return length(point.pos[0] - containerPos[0], point.pos[1] - containerPos[1])


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
        point.move()


running = True
frames = 0
num = 0
saved = 0
save_frames = True
while running:
    if frames % 1 == 0:
        gravity()
        air_resistance()
        for i in range(1):
            detect_edge_collisions()
            detect_point_collision()

        move_points()
        if save_frames and frames % 5 == 0:
            render(to_png=True, file=f'files/{saved}.png')
        else:
            # render()
            pass

        if frames % 50 == 0 and len(db.points) < 50:
            # db.add_point(containerPos[0] + 400, containerPos[1] - 400, size=random.randrange(10, 40), col=(random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256)))
            db.add_point(containerPos[0] + 300, containerPos[1] - 200, size=random.randrange(15, 26), col=(220, 220, 220))
            # db.add_point(1280 + 450, 720 - 450, size=4, col=(0, 0, 0))
            # db.add_point(random.randrange(res[0]), random.randrange(res[1]), size=10, col=(0, 0, 0))
            frames = 0
        elif len(db.points) >= 50:
            db.remove_point(0)
            save_frames = True
        num += 1
        if save_frames:
            # db.save(f'files/{saved}.json')
            saved += 1
    frames += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.KEYDOWN:
            # db.add_point(random.randrange(res[0]), random.randrange(res[1]), size=10, col=(0, 0, 0))
            print(saved)
