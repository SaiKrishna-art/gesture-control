from gestures.finger_count import count_fingers

def classify_gesture(hand_landmarks):
    fingers = count_fingers(hand_landmarks)
    if fingers == 0:
        return "LOCK"
    elif fingers == 1:
        return "CURSOR"
    elif fingers == 2:
        return "VOLUME"
    elif fingers == 3:
        return "BRIGHTNESS"
    elif fingers == 5:
        return "PLAY/PAUSE"

    return "NONE"
