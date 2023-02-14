KEYPOINT_DICT = {
    'nose': 0,
    'left_eye': 1,
    'right_eye': 2,
    'left_ear': 3,
    'right_ear': 4,
    'left_shoulder': 5,
    'right_shoulder': 6,
    'left_elbow': 7,
    'right_elbow': 8,
    'left_wrist': 9,
    'right_wrist': 10,
    'left_hip': 11,
    'right_hip': 12,
    'left_knee': 13,
    'right_knee': 14,
    'left_ankle': 15,
    'right_ankle': 16
}

actions = ['Cobra', 'Corpse' ,'Lotus' ,'Mountain', 'Tree', 'Triangle']

cyan = (255, 255, 0)
magenta = (255, 0, 255)

EDGE_COLORS = {
    (0, 1): magenta,
    (0, 2): cyan,
    (1, 3): magenta,
    (2, 4): cyan,
    (0, 5): magenta,
    (0, 6): cyan,
    (5, 7): magenta,
    (7, 9): cyan,
    (6, 8): magenta,
    (8, 10): cyan,
    (5, 6): magenta,
    (5, 11): cyan,
    (6, 12): magenta,
    (11, 12): cyan,
    (11, 13): magenta,
    (13, 15): cyan,
    (12, 14): magenta,
    (14, 16): cyan
}

# Confidence score to determine whether a keypoint prediction is reliable.
MIN_CROP_KEYPOINT_SCORE = 0.2

ANGL_DICT = {
    'angl_left_elbow': [10,8,6],
    'angl_left_shoulder': [8,6,12],
    'angl_left_hip': [6,12,14],
    'angl_left_knee': [12,14,16],
    'angl_right_elbow': [9,7,5],
    'angl_right_shoulder': [7,5,11],
    'angl_right_hip': [5,11,13],
    'angl_right_knee': [11,13,15],
}