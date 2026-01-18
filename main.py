from gestures.vertical_motion import VerticalMotion
from hand_tracking.landmarks import get_hand_center_y
from gestures.poke_detector import PokeDetector
from hand_tracking.landmarks import get_index_finger_tip_3d
from utils.smoothing import Smoother
from hand_tracking.landmarks import get_index_finger_tip
from gestures.stabilizer import GestureStabilizer
import cv2
from camera.webcam import Webcam
from hand_tracking.detector import HandDetector
from gestures.gesture_classifier import classify_gesture as detect_gesture
from gestures.cooldown import Cooldown
from controllers.mouse_controller import MouseController
from controllers.volume_controller import VolumeController
from controllers.brightness_controller import BrightnessController
from controllers.media_controller import MediaController
from ui.overlay import draw_text

# ---------------- INITIALIZATION ---------------- #

cam = Webcam()
detector = HandDetector()

cursor_cooldown = Cooldown(delay=0.02)  # ~50 FPS max
stabilizer = GestureStabilizer(size=5)

poke_detector = PokeDetector(threshold=0.05)
click_cooldown = Cooldown(delay=0.8)

volume_motion = VerticalMotion(threshold=0.02)
volume_cooldown = Cooldown(delay=0.15)

mouse = MouseController()
volume = VolumeController()
brightness = BrightnessController()
media = MediaController()

smoother = Smoother(factor=0.25)
system_locked = True
lock_cooldown = Cooldown(delay=1.5)
action_cooldown = Cooldown(delay=1.2)

# ---------------- MAIN LOOP ---------------- #

while True:
    # 1️⃣ Get frame FIRST
    frame = cam.get_frame()
    if frame is None:
        break

    # 2️⃣ Detect hand landmarks
    results = detector.detect(frame)
    gesture = None

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            raw_gesture = detect_gesture(hand)
            gesture = stabilizer.stabilize(raw_gesture)
            draw_text(frame, f"Gesture: {gesture}")

            # 🔒 Lock / Unlock system
            if gesture == "LOCK" and lock_cooldown.ready():
                system_locked = not system_locked

            # ▶️ Perform actions only if unlocked
            if not system_locked:

                if gesture == "CURSOR" and cursor_cooldown.ready():
                    x_norm, y_norm = get_index_finger_tip(hand)
                    screen_x = int(x_norm * mouse.screen_w)
                    screen_y = int(y_norm * mouse.screen_h)
                    smooth_x, smooth_y = smoother.smooth(screen_x, screen_y)
                    mouse.move(smooth_x, smooth_y)

                elif gesture == "VOLUME":
                    center_y = get_hand_center_y(hand)
                    direction = volume_motion.get_direction(center_y)

                    if direction == "UP" and volume_cooldown.ready():
                        volume.increase()
                        # draw_text(frame, "VOLUME UP")

                    elif direction == "DOWN" and volume_cooldown.ready():
                        volume.decrease()
                        # draw_text(frame, "VOLUME DOWN")

                elif gesture == "BRIGHTNESS":
                    center_y = get_hand_center_y(hand)
                    direction = volume_motion.get_direction(center_y)

                    if direction == "UP":
                        brightness.increase()
                        # draw_text(frame, "BRIGHTNESS UP", color=(255, 255, 0))

                    elif direction == "DOWN":
                        brightness.decrease()
                        # draw_text(frame, "BRIGHTNESS DOWN", color=(255, 165, 0))


                elif gesture == "PLAY/PAUSE" and action_cooldown.ready():
                    media.toggle()

    # 3️⃣ Draw system status overlay (AFTER frame exists)
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

    # 4️⃣ Show frame
    cam.show(frame)

    # 5️⃣ Exit key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ---------------- CLEANUP ---------------- #
cam.release()
cv2.destroyAllWindows()
