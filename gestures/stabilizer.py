from collections import deque

class GestureStabilizer:
    def __init__(self, size=5):
        self.history = deque(maxlen=size)

    def stabilize(self, gesture):
        self.history.append(gesture)
        return max(set(self.history), key=self.history.count)
