"""
Design variables.
Geometric properties.
"""
import csv
import numpy as np


def get_angles():
    angles = None
    variant = 1

    if variant == 1:

        angles = np.array([
            90, 90, 90, 90, 90, 90,
            15, 15, 15, 15, 15, 15,
            30, 30, 30, 30, 30,
            40, 40, 40, 40,
            50, 50, 50, 50,
            54, 54, 54, 54,
            60, 60, 60, 60,
            70, 70, 70, 70,
            90, 90, 90, 90, 90, 90, 90,
        ])

    elif variant == 2:
        angles = [90, 90, 90, 90,
                  15, 15, 15, 15,
                  30, 30, 30, 30,
                  40, 40, 40, 40,
                  50, 50, 50, 50,
                  90, 90, 90, 90, 90, 90, 90, 90]

    elif variant == 3:
        angles = [15, 20, 30, 40, 50, 60, 70, 90]  # TODO obsolete

        result = []

        for variant in range(6):
            result += list(np.random.permutation(angles))
        angles = result

    elif variant == 4:
        """
        use user specified layup
        """
        _input_file = r'..\resources\sequence.csv'
        with open(_input_file) as fh:
            reader = csv.reader(fh)
            angles = list(reader)[0]
            angles = [int(ang.strip()) for ang in angles]

    elif variant == 5:
        angles = [15,
                  30,
                  40,
                  50,
                  70, ]
    elif variant == 6:
        angles = ([90, ] * 4 +
                  [15, ] * 10 +
                  [24, ] * 2 +
                  [40, ] * 4 +
                  [90, ] * 4 +
                  [56, ] * 6 +
                  [90, ] * 4 +
                  [66, ] * 4)

    return angles


b = 16.  # mm - Roving bandwidth
t_R = 0.65  # mm - Laminate thickness ar r = R (cylindrical part)
t_P = 0.35  # mm - Ply thickness
max_y_hoop = 378.
t_hoop = 0.72
