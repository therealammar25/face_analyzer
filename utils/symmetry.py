import numpy as np

def calculate_symmetry(landmarks):

    left = landmarks[33]
    right = landmarks[263]
    nose = landmarks[1]

    d1 = np.sqrt((left.x - nose.x)**2 + (left.y - nose.y)**2)
    d2 = np.sqrt((right.x - nose.x)**2 + (right.y - nose.y)**2)

    diff = abs(d1 - d2)

    score = max(0, 1 - diff)

    return round(score, 2)