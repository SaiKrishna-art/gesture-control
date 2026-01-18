class PokeDetector:
    def __init__(self, threshold=0.08):
        self.prev_z = None
        self.threshold = threshold

    def is_poke(self, z):
        if self.prev_z is None:
            self.prev_z = z
            return False

        delta = self.prev_z - z
        self.prev_z = z

        return delta > self.threshold
