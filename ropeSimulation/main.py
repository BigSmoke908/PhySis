import math
from db import Database
import pygame


pygame.init()
UHD = (3840, 2160)
WQHD = (2560, 1440)
FHD = (1920, 1080)
screen = pygame.display.set_mode(WQHD)

movePointCol = (70, 180, 70)
fixPointCol = (255, 70, 70)
connectionCol = (180, 180, 180)
bgCol = (50, 100, 170)
db = Database()


def render():
    screen.fill(bgCol)
    for connection in db.connections:
        pygame.draw.line(screen, connectionCol, (db.points[connection[0]].Pos[0], db.points[connection[0]].Pos[1]), (db.points[connection[1]].Pos[0], db.points[connection[1]].Pos[1]), 4)

    for point in db.points:
        if point.visible:
            if not point.fixed:
                pygame.draw.circle(screen, movePointCol, (point.Pos[0], point.Pos[1]), 10)
            else:
                pygame.draw.circle(screen, fixPointCol, (point.Pos[0], point.Pos[1]), 10)
    pygame.display.update()


def redo_forces():
    # gravity
    for point in db.points:
        if not point.fixed:
            if point.visible:
                point.Pos = (point.Pos[0], point.Pos[1] + 5)  # adjust the amount of gravity here
            else:
                point.Pos = (point.Pos[0], point.Pos[1] + 0.5)  # adjust the amount of gravity here

    # now forces for the connections
    for i in range(10):
        for connection in db.connections:
            current_length = db.point_distance(connection[0], connection[1])
            offset = (current_length - connection[2]) / 400
            pos_a = db.points[connection[0]].Pos
            pos_b = db.points[connection[1]].Pos

            if not db.points[connection[0]].fixed:
                db.points[connection[0]].Pos = (((pos_b[0] - pos_a[0]) * offset) + pos_a[0], ((pos_b[1] - pos_a[1]) * offset) + pos_a[1])
            if not db.points[connection[1]].fixed:
                db.points[connection[1]].Pos = (((pos_a[0] - pos_b[0]) * offset) + pos_b[0], ((pos_a[1] - pos_b[1]) * offset) + pos_b[1])


def move_points():
    for point in db.points:
        if not point.fixed:
            previous = point.Pos
            point.Pos = ((point.Pos[0] * 2) - point.previousPos[0], (point.Pos[1] * 2) - point.previousPos[1])
            point.previousPos = previous


frames = 0
running = True
mouse = (0, 0)
selected = -1  # index of the selected point
paused = False
while running:
    if frames % 20 == 0 and not paused:
        redo_forces()
        move_points()
    render()
    frames += 1

    # db.add_point(*mouse)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            buttons = pygame.mouse.get_pressed()
            if buttons[0]:  # add a normal point
                db.add_point(*mouse)
            elif buttons[2]:  # add a fixed point
                db.add_point(*mouse, True)
            elif buttons[1]:
                # add the point under the cursor + the previously selected one to a connection/remove their connection
                # this is the selected point if none was selected previously (-1)
                underCursor = -1
                hitboxSize = 10
                for i, point in enumerate(db.points):
                    if mouse[0] - hitboxSize < point.Pos[0] < mouse[0] + hitboxSize and mouse[1] - hitboxSize < point.Pos[1] < mouse[1] + hitboxSize and point.visible:
                        underCursor = i
                        break

                if selected == -1:
                    selected = underCursor
                elif underCursor != -1:
                    removed = False
                    for connection in db.connections:
                        if connection[0] == selected and connection[1] == underCursor or connection[1] == selected and connection[0] == underCursor:
                            db.connections.remove(connection)
                            removed = True
                            break
                    if not removed:
                        db.add_connection(selected, underCursor)
                    selected = -1
        elif event.type == pygame.KEYDOWN:
            paused = not paused

# TODO: being able to delete stuff like points would be pretty cool
