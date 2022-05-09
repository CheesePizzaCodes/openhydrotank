import numpy as np
import scipy as sp

# 0

m_R = 2 * pi * R * np.cos(alpha_0) / b
n_R = t_R / (2 * t_p)

t = (m_R * n_R / pi) * (np.arccos(r_0 / r) - np.arccos((r_0 + b) / r)) * t_p



A = np.array([
    [1., r_0, r_0 ** 2, r_0 ** 3],
    [1, r_2b, r_2b ** 2, r_2b ** 3],
    [0, 1, 3 * r_2b, 3 * r_2b ** 2],
    []
])
