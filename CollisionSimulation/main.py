import pygame


pygame.init()
UHD = (3840, 2160)
WQHD = (2560, 1440)
FHD = (1920, 1080)
screen = pygame.display.set_mode(WQHD)


def render():
    screen.fill()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
