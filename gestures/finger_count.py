def count_fingers(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = 0

    if hand_landmarks.landmark[tips[0]].x<hand_landmarks.landmark[tips[0]-1].x:
        fingers += 1

    for tip in tips[1:]:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip-2].y:
            fingers += 1

    return fingers