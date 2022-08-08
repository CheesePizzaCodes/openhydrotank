"""
Design variables.
Geometric properties.
"""
import numpy as np

_ = 1

if _ == 1:

    angles = np.array([
        90, 90, 90, 90, 90, 90, 90, 90,
        15, 15, 15, 15, 15, 15, 15, 15,
        30, 30, 30, 30,
        40, 40, 40, 40,
        50, 50, 50, 50,
        54, 54, 54, 54,
        60, 60, 60, 60,
        70, 70, 70, 70,
        # 80, 80, 80, 80,
        90, 90, 90, 90, 90, 90, 90, 90
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

    for _ in range(3):
        result += list(np.random.permutation(angles))
    angles = result

# Independent
# R = 156.  # mm - Cylindrical zone radius TODO make dependent on file

b = 16.  # mm - Roving bandwidth
# alpha_0 = np.radians(40.)  # rad - Cylindrical zone angle TODO must vary with each ply
t_R = 0.35  # mm - Roving thickness
t_P = 0.35  # mm - Ply thickness TODO must depend on hoop / helical

pi = np.pi

# Derived TODO obsolete, remove


# r_0 = R * np.sin(alpha_0)  # mm - Polar opening

# r_b = r_0 + b
# r_2b = r_0 + 2 * b

# m_R = 2 * pi * R * np.cos(alpha_0) / b
# m_0 = 2 * pi * r_0 * np.cos(alpha_0) / b
# n_R = t_R / (2 * t_P)
