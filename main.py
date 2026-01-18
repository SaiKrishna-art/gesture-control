import cv2

from camera.webcam import Webcam
from hand_tracking.detector import HandDetector
from gestures.gesture_classifier import classify_gesture as detect_gesture
from gestures.cooldown import Cooldown
from gestures.stabilizer import GestureStabilizer
from gestures.vertical_motion import VerticalMotion
from gestures.hold_detector import HoldDetector

from hand_tracking.landmarks import (
    get_index_finger_tip,
    get_hand_center_y,
)

from controllers.mouse_controller import MouseController
from controllers.volume_controller import VolumeController
from controllers.brightness_controller import BrightnessController
from controllers.media_controller import MediaController

from utils.smoothing import Smoother
from ui.overlay import draw_text

# ---------------- INITIALIZATION ---------------- #

cam = Webcam()
detector = HandDetector()

mouse = MouseController()
volume = VolumeController()
brightness = BrightnessController()
media = MediaController()

smoother = Smoother(factor=0.25)

stabilizer = GestureStabilizer(size=7)

cursor_cooldown = Cooldown(delay=0.02)
volume_motion = VerticalMotion(threshold=0.02)
volume_cooldown = Cooldown(delay=0.15)
action_cooldown = Cooldown(delay=1.2)

lock_hold = HoldDetector(hold_time=1.0)

system_locked = False
active_mode = None

# ---------------- MAIN LOOP ---------------- #

while True:
    frame = cam.get_frame()
    if frame is None:
        break

    results = detector.detect(frame)

    gesture = None

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]

        raw_gesture = detect_gesture(hand)
        gesture = stabilizer.stabilize(raw_gesture)

        draw_text(frame, f"Gesture: {gesture}")

        # 🔒 LOCK / UNLOCK (only when no active mode)
        if active_mode is None:
            if lock_hold.is_held(gesture == "LOCK"):
                system_locked = not system_locked

        # 🧠 MODE LOCKING
        if not system_locked:
            if active_mode is None and gesture in ["CURSOR", "VOLUME", "BRIGHTNESS"]:
                active_mode = gesture
            elif active_mode is not None:
                gesture = active_mode

            # 🖱️ CURSOR
            if gesture == "CURSOR" and cursor_cooldown.ready():
                x_norm, y_norm = get_index_finger_tip(hand)
                screen_x = int(x_norm * mouse.screen_w)
                screen_y = int(y_norm * mouse.screen_h)
                smooth_x, smooth_y = smoother.smooth(screen_x, screen_y)
                mouse.move(smooth_x, smooth_y)

            # 🔊 VOLUME
            elif gesture == "VOLUME":
                center_y = get_hand_center_y(hand)
                direction = volume_motion.get_direction(center_y)

                if direction == "UP" and volume_cooldown.ready():
                    volume.increase()
                elif direction == "DOWN" and volume_cooldown.ready():
                    volume.decrease()

            # 💡 BRIGHTNESS
            elif gesture == "BRIGHTNESS":
                center_y = get_hand_center_y(hand)
                direction = volume_motion.get_direction(center_y)

                if direction == "UP":
                    brightness.increase()
                elif direction == "DOWN":
                    brightness.decrease()

            # ▶️ PLAY / PAUSE (only when steady)
            elif gesture == "PLAY/PAUSE" and active_mode is None:
                if action_cooldown.ready():
                    media.toggle()

    else:
        # hand removed → reset mode
        active_mode = None

    # -------- STATUS OVERLAY -------- #

    status = "LOCKED" if system_locked else "UNLOCKED"
    color = (0, 0, 255) if system_locked else (0, 255, 0)

    cv2.putText(
        frame,
        f"System: {status}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2
    )

    cam.show(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ---------------- CLEANUP ---------------- #

cam.release()
cv2.destroyAllWindows()
