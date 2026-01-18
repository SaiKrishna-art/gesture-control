def get_index_finger_tip(hand_landmarks):
    tip = hand_landmarks.landmark[8]  # index fingertip
    return tip.x, tip.y
def get_index_finger_tip_3d(hand_landmarks):
    tip = hand_landmarks.landmark[8]
    return tip.x, tip.y, tip.z
def get_hand_center_y(hand_landmarks):
    y_vals = [lm.y for lm in hand_landmarks.landmark]
    return sum(y_vals) / len(y_vals)
