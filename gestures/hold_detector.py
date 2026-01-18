import time

class HoldDetector:
    def __init__(self, hold_time=1.0):
        self.hold_time = hold_time
        self.start_time = None

    def is_held(self, condition):
        if condition:
            if self.start_time is None:
                self.start_time = time.time()
            elif time.time() - self.start_time >= self.hold_time:
                self.start_time = None
                return True
        else:
            self.start_time = None
        return False
