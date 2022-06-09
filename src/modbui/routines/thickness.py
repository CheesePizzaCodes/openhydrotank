import sys, os, time

sys.path.append('E:\\Current Workspace\\Codebase\\hydrotank\\src')

sys.path.append('E:\\Current Workspace\\Codebase\\hydrotank\\src\\modbui')

sys.path.append('E:\\Current Workspace\\Codebase\\hydrotank\\src\\modbui\\routines')

import numpy as np
import scipy as sp
# import matplotlib.pyplot as plt
# from matplotlib.pyplot import plot
from scipy.integrate import quad
from scipy.interpolate import interp1d
from scipy.interpolate import make_interp_spline

from design_variables import *

# TODO move to global definition
filename = 'E:\\Current Workspace\\Codebase\\hydrotank\\src\\modbui\\routines\\liner.csv'

liner = np.loadtxt(open(filename), delimiter=",", skiprows=1)

liner_r = liner[:, 0]
liner_y = liner[:, 1]


def globs(angle):
    """
    Calculates the global geometric parameters for this routine. Function of alpha_0 and thus layer-dependent.
    :param angle: alpha_0. Desired cylindrical-section angle.
    :return:
    """

    global r_0, m_R, m_0, r_b, r_2b, n_R, alpha_0
    alpha_0 = np.radians(angle)
    r_0 = R * np.sin(alpha_0)  # Polar opening radius
    m_R = 2 * pi * R * np.cos(alpha_0) / b
    m_0 = 2 * pi * r_0 * np.cos(alpha_0) / b
    r_b = r_0 + b
    r_2b = r_0 + 2 * b
    n_R = t_R / (2 * t_P)


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

def thickness_1():
    t = np.poly1d(np.flip(a_vec(alpha_0)))
    return t


# Segment 2
def thickness_2(r):  # Callable and vectorized
    r = np.asarray(r)

    # remove numerical errors
    arg_1 = r_0 / r
    arg_1[arg_1 > 1] = 1

    arg_2 = r_b / r
    arg_2[arg_2 > 1] = 1

    t = (m_R * n_R / pi) * (np.arccos(arg_1) - np.arccos(arg_2)) * t_P
    t = np.nan_to_num(t)
    return t


# Joining two sections:
def thickness(r):
    """
    aggregates the thickness distribution of a layer
    :param r:
    :return:
    """
    r = np.asarray(r)
    t = np.zeros(r.shape)

    # First case
    # extract polynomial for given globs
    polynomial = thickness_1()
    # find lower bound as the first real root of polynomial
    lower_bound = np.real(polynomial.roots[np.isreal(polynomial.roots)][0])
    # t += polynomial(r) * ((r_0 <= r) & (r <= r_2b))
    t += polynomial(r) * ((polynomial(r) >= 0) & (r <= r_2b))
    # Second case
    t += thickness_2(r) * (r_2b < r)

    tol = 0.08
    t[t < tol] = 0

    return t


def smoothing(current, previous):
    """

    :param current: points of the current layer in the form (x, y)
    :param previous: points of the previous layer (x, y)
    :return:
    """
    x, y = current

    x_p, y_p = previous

    # # get max. From this position to the left, values will be overriden by smoothing.
    # idx = y.argmax()
    # # delete left of max
    # y[idx:] = 10
    # return x, y
    pass


def draw_layer(r, g, make_smooth):
    """

    :param r: r coordinates of the liner (or previous topmost) points
    :param g: z coordinates of the liner bzw. previous topmost
    :return: Tuple of points belonging to the new layer
    """
    # calculate thickness distribution
    t = thickness(r)
    dg = np.gradient(g, r)
    den = np.sqrt(1 + dg ** 2)
    x = r - t * dg / den
    y = g + t / den
    layer_mask = t > 0  # Logical Mask indicating the layer region preliminarily
    # --- smoothing ---

    if make_smooth:
        # find index where layer peaks height
        idx = (y * layer_mask).argmax()  #

        # build mask: True below layer maximum point value AND below flag idx

        # left of flag index
        aux_mask = np.zeros(y.shape, dtype="bool")
        aux_mask[:idx] = True

        # and below maximum y point
        aux_mask = np.logical_and(aux_mask, y < y[idx])

        # delete all points from all vectors that fulfill the condition
        # x, y, r, g = map(lambda v: np.delete(v, aux_mask), (x, y, r, g))

        y[aux_mask] = y[idx]

    # finally, evaluate returns. distinction between zero thickness considered vs deleted

    # redefine layer region: where previous top (g) deviates from new top (y)
    layer_mask = y != g
    first_true = np.where(layer_mask)[0][0]
    layer_mask[first_true - 1] = True

    x_layer, y_layer = x[layer_mask], y[layer_mask]

    x_layer = np.append(x_layer, x_layer[-1])
    y_layer = np.append(y_layer, 0)

    # x_layer[0] = r[first_true-1]
    # y_layer[0] = g[first_true-1]

    layer_points = (x_layer, y_layer)
    topmost_points = (x, y)  # used to calculate next layer. do not store.
    return layer_points, topmost_points


def main():
    # angles = [15, 20, 30, 40, 50, 60, 70]
    angles = [90, 90, 90, 90,
              15, 15, 15, 15, 15, 15, 15, 15,
              30, 30, 30, 30,
              40, 40, 40, 40,
              50, 50, 50, 50,
              54, 54, 54, 54,
              90, 90, 90, 90, 90, 90, 90, 90]
    result = []

    for _ in range(0):
        result += list(np.random.permutation(angles))

    angles = [a for a in angles if a != 90]

    # angles = result

    # initial values are those of the liner

    # TODO massive refactor, check that everything makes sense...
    globs(angles[0])
    # r = np.linspace(0, R, num=505)  # TODO change to r_0, R. Layer dependent.
    # g = np.interp(r, liner_r, liner_y)

    zone_1 = np.diff(liner_r) != 0

    zone_1 = np.append(zone_1, False)

    # initialize parametric curve to shape of liner
    r = liner_r[zone_1]
    g = liner_y[zone_1]

    ls = np.linspace(r.min(), r.max(), 200)

    interp = interp1d(r, g, kind="cubic")

    r = ls
    g = interp(r)

    # # Initialize topmost as shape of the liner
    topmost_points = (r, g)

    # f1 = plt.figure(1)  # TODO plot
    # plot(r, g, "-o")

    # draw layup routine TODO make method

    initial_line = tuple(zip(r, g))

    initial_line += ((r[-1], 0),)

    lines = (initial_line,)  # accum. for the splines that represent the layers
    landmarks = (initial_line[-1],)  # accum. for important landmarks

    for angle in angles:

        # overwrite globals
        globs(angle)
        # calculate outer contour of new layer
        # x = linespace used, y = topmost wrt whom to calculate
        if angle <= 20:
            make_smooth = True
        else:
            make_smooth = False  # TODO this breaks the code
        layer_points, topmost_points = draw_layer(topmost_points[0], topmost_points[1], make_smooth)

        # extract points (redundant, readability)

        x = layer_points[0]
        y = layer_points[1]

        line = tuple(zip(x, y))
        landmark = line[-1]

        lines += (line,)
        landmarks += (landmark,)

        disp = "-o"
        # if True:
        #     f1 = plt.figure(1)
        #     # plot(*layer_points, disp)
        #     plot(x, y, disp)
        #
        #     f2 = plt.figure(2)
        #     plot(x, thickness(x), disp)

    return lines, landmarks


if __name__ == "__main__":
    main()
