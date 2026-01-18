class VerticalMotion:
    def __init__(self, threshold=0.02):
        self.prev_y = None
        self.threshold = threshold

    def get_direction(self, y):
        if self.prev_y is None:
            self.prev_y = y
            return None
        delta = self.prev_y - y
        self.prev_y = y

        if delta > self.threshold:
            return "UP"
        elif delta < -self.threshold:
            return "DOWN"

        return None