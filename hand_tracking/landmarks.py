def get_index_finger_tip(hand_landmarks):
    tip = hand_landmarks.landmark[8]  # index fingertip
    return tip.x, tip.y
