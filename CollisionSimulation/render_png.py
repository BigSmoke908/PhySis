from PIL import Image
import math


# db = Database from db.py
# file = file where the new image will be stored
# other Variables similar/same as in main.py
def create_png(db, file, size, container_col, container_pos, container_size, background_col):
    image = [[background_col for i in range(size[0])] for j in range(size[1])]

    image = draw_circle(image, container_pos, container_size, container_col)
    for p, point in enumerate(db.points):
        if point.size <= 0:
            db.remove_point(p)
            continue
        image = draw_circle(image, point.pos, point.size, point.col)
        # TODO: render trail as well?
    converted_image = []

    for row in image:
        for pixel in row:
            converted_image.append(pixel)
    img = Image.new('RGB', size, (0, 0, 0))
    img.putdata(converted_image)
    img.save(file)


def draw_circle(img, pos, size, col):
    for y in range(int(pos[1]) - size - 5, int(pos[1]) + size + 5):
        for x in range(int(pos[0]) - size - 5, int(pos[0]) + size + 5):
            if math.sqrt((y - pos[1]) ** 2 + (x - pos[0]) ** 2) <= size:
                img[y][x] = col
    return img
