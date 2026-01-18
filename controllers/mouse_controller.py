import pyautogui

class MouseController:
    def __init__(self):
        self.screen_w, self.screen_h = pyautogui.size()
        pyautogui.FAILSAFE = False

    def move(self, x, y):
        pyautogui.moveTo(x, y, duration=0)

    def click(self):
        pyautogui.click()