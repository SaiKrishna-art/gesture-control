class Smoother:
    def __init__(self, factor=0.2):
        self.prev_x = None
        self.prev_y = None
        self.factor = factor

    def smooth(self, x, y):
        if self.prev_x is None:
            self.prev_x, self.prev_y = x, y
            return x, y

        sx = self.prev_x + (x - self.prev_x) * self.factor
        sy = self.prev_y + (y - self.prev_y) * self.factor

        self.prev_x, self.prev_y = sx, sy
        return sx, sy