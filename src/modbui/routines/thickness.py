import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from scipy.integrate import quad

from design_variables import *

# TODO move to global definition
filename = 'E:\\Current Workspace\\Codebase\\hydrotank\\src\\modbui\\routines\\liner.csv'

liner = np.loadtxt(open(filename), delimiter=",", skiprows=1)

r_array = liner[:, 0]
g_array = liner[:, 1]



# for i, position in enumerate(r):
#     # find index of value closest to the position
#     idx = (np.abs(g_array - position)).argmin()
#     # set new g to correct value
#     g[i] = g_array[idx]
#
# idx = (np.abs(g_array - r)).argmin()
# g_array[idx]


def globs(angle):
    """
    Calculates the global geometric parameters for this routine. Function of alpha_0 and thus layer-dependent.
    :param angle: alpha_0. Desired cylindrical-section angle.
    :return:
    """

    global r_0, m_R, m_0, r_b, r_2b, n_R, alpha_0
    alpha_0 = np.radians(angle)
    r_0 = R * np.sin(angle)  # Polar opening radius
    m_R = 2 * pi * R * np.cos(angle) / b
    m_0 = 2 * pi * r_0 * np.cos(angle) / b
    r_b = r_0 + b
    r_2b = r_0 + 2 * b
    n_R = t_R / (2 * t_P)


# Define all grobal parameters
#globs(alpha_0)

# TODO massive refactor, check that everything makes sense...
r = np.linspace(0, R, num=501)  # TODO change to r_0, R. Layer dependent.
g = np.interp(r, r_array, g_array)

def pd(degree):
    """
    Utility function
    :param degree:
    :return:
    """
    return r_2b ** degree - r_0 ** degree


def a_vec(angle):
    """
    Obtain coefficients for the polynomial for the thickness in region 1
    :param angle:
    :return:
    """
    # Setting up linear system: Ac = a, A matrix
    A = np.array([
        [1., r_0, r_0 ** 2, r_0 ** 3],
        [1., r_2b, r_2b ** 2, r_2b ** 3],
        [0., 1., 2 * r_2b, 3 * r_2b ** 2],
        [pi * (pd(2)), 2 * pi / 3 * (pd(3)), pi / 2 * (pd(4)), 2 * pi / 5 * (pd(5))],
    ])

    # c - vector
    c_0 = t_R * pi * R * np.cos(angle) / (m_0 * b)
    c_1 = m_R * n_R / pi * (np.arccos(r_0 / r_2b) - np.arccos(r_b / r_2b)) * t_P
    c_2 = m_R * n_R / pi * (r_0 / (r_2b * np.sqrt(pd(2))) - r_b / (r_2b * np.sqrt(r_2b ** 2 - r_b ** 2))) * t_P

    int_1, err = quad(lambda r: r * np.arccos(r_0 / r), r_0, r_b)
    int_2, err = quad(lambda r: r * np.arccos(r_0 / r_2b) - r * np.arccos(r_b / r_2b), r_b, r_2b)

    c_3 = 2 * m_R * n_R * t_P * (int_1 + int_2)

    c = np.array([c_0, c_1, c_2, c_3])

    a_vec = np.linalg.solve(A, c)  # vector of coefficients for the polynomial

    return a_vec


# Segments of the piecewise curve:
# Segment 1
# polynomial object. Already callable and vectorized.
#


thickness_1 = np.poly1d(np.flip(a_vec(alpha_0)))

# Segment 2
def thickness_2(r):  # Callable and vectorized
    r = np.asarray(r)
    t = (m_R * n_R / pi) * (np.arccos(r_0 / r) - np.arccos(r_b / r)) * t_P
    t = np.nan_to_num(t)
    return t


# Joining two sections:
def thickness(r):
    r = np.asarray(r)
    t = np.zeros(r.shape)
    # First case
    t += thickness_1(r) * ((r_0 < r) & (r <= r_2b))
    # Second case
    t += thickness_2(r) * ((r_2b < r) & (r <= R))
    return t


def draw_layer(r, g):
    """

    :param r: r coordinates of the liner (or previous topmost) points
    :param g: z coordinates of the liner bzw. previous topmost
    :return: Tuple of points belonging to the new layer
    """
    t = thickness(r)
    dg = np.gradient(g, r)
    den = np.sqrt(1 + dg ** 2)

    x = r - t * dg / den

    y = g + t / den

    return x, y


angles = (15, 20, 40, 50, 89,)




x = r
y = g
plot(x, y)
for ang in angles:
    # set value for global variables
    globs(ang)
    x, y = draw_layer(r, y)
    plot(x, y)
    g = y  # update value of topmost as last layer



