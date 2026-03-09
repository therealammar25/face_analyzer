import numpy as np

def distance(p1, p2):
    return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def calculate(landmarks):
    # Averaging multiple points for stability (professional technique)
    face_width     = (distance(landmarks[234], landmarks[454]) + distance(landmarks[239], landmarks[459])) / 2
    face_height    = distance(landmarks[10], landmarks[152])
    jaw_width      = (distance(landmarks[58], landmarks[288]) + distance(landmarks[61], landmarks[291])) / 2
    cheek_width    = (distance(landmarks[50], landmarks[280]) + distance(landmarks[101], landmarks[330])) / 2
    forehead_width = (distance(landmarks[103], landmarks[332]) + distance(landmarks[109], landmarks[338])) / 2
    chin_width     = distance(landmarks[175], landmarks[400])

    return {
        "width": face_width,
        "height": face_height,
        "jaw_width": jaw_width,
        "cheek_width": cheek_width,
        "forehead_width": forehead_width,
        "chin_width": chin_width
    }