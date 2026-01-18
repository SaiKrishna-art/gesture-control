import screen_brightness_control as sbc
import time


class BrightnessController:
    def __init__(self):
        self.last_time = 0
        self.cooldown = 0.2

    def _can_trigger(self):
        now = time.time()
        if now - self.last_time > self.cooldown:
            self.last_time = now
            return True
        return False

    def increase(self, step=5):
        if self._can_trigger():
            current = sbc.get_brightness()[0]
            sbc.set_brightness(min(current + step, 100))

    def decrease(self, step=5):
        if self._can_trigger():
            current = sbc.get_brightness()[0]
            sbc.set_brightness(max(current - step, 0))
