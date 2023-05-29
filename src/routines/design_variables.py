"""
Design variables.
Geometric properties.
"""
import csv
import numpy as np


def get_angles():
    angles = None
    _ = 6

    if _ == 1:

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

    elif _ == 2:
        angles = [90, 90, 90, 90,
                  15, 15, 15, 15,
                  30, 30, 30, 30,
                  40, 40, 40, 40,
                  50, 50, 50, 50,
                  90, 90, 90, 90, 90, 90, 90, 90]

    elif _ == 3:
        angles = [15, 20, 30, 40, 50, 60, 70, 90]  # TODO obsolete

        result = []

        for _ in range(6):
            result += list(np.random.permutation(angles))
        angles = result

    elif _ == 4:
        """
        use user specified layup
        """
        _input_file = r'..\resources\sequence.csv'
        with open(_input_file) as fh:
            reader = csv.reader(fh)
            angles = list(reader)[0]
            angles = [int(ang.strip()) for ang in angles]

    elif _ == 5:
        angles = [15,
                  30,
                  40,
                  50,
                  70, ]
    elif _ == 6:
        angles = ([90, ] * 4 +
                  [15, ] * 10 +
                  [24, ] * 2 +
                  [40, ] * 4 +
                  [90, ] * 4 +
                  [56, ] * 6 +
                  [90, ] * 4 +
                  [66, ] * 4)

    return angles


# Independent
# R = 156.  # mm - Cylindrical zone radius TODO make dependent on file

b = 16.  # mm - Roving bandwidth
# alpha_0 = np.radians(40.)  # rad - Cylindrical zone angle TODO must vary with each ply
t_R = 0.65  # mm - Roving thickness
t_P = 0.35  # mm - Ply thickness TODO must depend on hoop / helical

pi = np.pi

# Derived TODO obsolete, remove


# r_0 = R * np.sin(alpha_0)  # mm - Polar opening

# r_b = r_0 + b
# r_2b = r_0 + 2 * b

# m_R = 2 * pi * R * np.cos(alpha_0) / b
# m_0 = 2 * pi * r_0 * np.cos(alpha_0) / b
# n_R = t_R / (2 * t_P)
