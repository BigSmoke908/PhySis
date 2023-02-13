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

    def __str__(self):
        return str(self.Pos)
