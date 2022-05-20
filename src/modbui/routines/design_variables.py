"""
Design variables.
Geometric properties.
"""
import numpy as np


# Independent
R = 156.  # mm - Cylindrical zone radius TODO make dependent on file

b = 8.  # mm - Roving bandwidth
#alpha_0 = np.radians(40.)  # rad - Cylindrical zone angle TODO must vary with each ply
t_R = 0.15  # mm - Roving thickness
t_P = 0.65  # mm - Ply thickness TODO must depend on hoop / helical

pi = np.pi


# Derived TODO obsolete, remove


# r_0 = R * np.sin(alpha_0)  # mm - Polar opening

# r_b = r_0 + b
# r_2b = r_0 + 2 * b

# m_R = 2 * pi * R * np.cos(alpha_0) / b
# m_0 = 2 * pi * r_0 * np.cos(alpha_0) / b
# n_R = t_R / (2 * t_P)
