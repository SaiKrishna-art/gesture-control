import screen_brightness_control as sbc

class BrightnessController:
    def change(self, delta):
        current = sbc.get_brightness()[0]
        sbc.set_brightness(min(100, max(0, current + delta)))