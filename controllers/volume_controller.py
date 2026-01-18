import pyautogui
import time


class VolumeController:
    def __init__(self):
        self.last_action_time = 0
        self.cooldown = 0.1  # seconds

    def _can_trigger(self):
        now = time.time()
        if now - self.last_action_time > self.cooldown:
            self.last_action_time = now
            return True
        return False

    def increase(self, steps=10):
        if self._can_trigger():
            for _ in range(steps):
                pyautogui.press("volumeup")

    def decrease(self, steps=10):
        if self._can_trigger():
            for _ in range(steps):
                pyautogui.press("volumedown")
