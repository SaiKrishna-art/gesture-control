import time


class Cooldown:
    def __init__(self, delay=1.0):
        self.delay = delay
        self.last_time = 0

    def ready(self):
        now = time.time()
        if now - self.last_time >= self.delay:
            self.last_time = now
            return True
        return False
