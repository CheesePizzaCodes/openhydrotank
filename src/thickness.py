# coding=utf-8
"""
Thickness computation routine
TODO memoize t as polynomials
Run from '/temp' directory
"""
import sys

# Toggles if the code is rand standalone to graph
# or by Abaqus to plot the geometry
# True: graphing is enabled, i.e., running standalone, not in the abaqus interpreter
RUNNING_STANDALONE = 'ABQcaeK.exe' not in sys.executable  # TODO obsolete, will always run outside of abq

from typing import List, Optional, Tuple

import numpy as np
from numpy import pi

if RUNNING_STANDALONE:
    import matplotlib.pyplot as plt

from scipy.integrate import quad
from scipy.interpolate import interp1d

import routines.design_variables as dv
from routines.design_variables import b, t_R, t_P, max_y_hoop, t_hoop
from model import Curve, CurvesBunch, ValuesArray, CoordinatesArray


def define_global_variables(angle: float):
    """
    Calculates the global geometric parameters for this routine.
    These vary with respect to the angle of the layer.
    :param angle: alpha_0. Desired cylindrical-section winding angle.
    :return:
    """
    global r_0, m_R, m_0, r_b, r_2b, n_R, alpha_0, angle_deg
    angle_deg = angle
    alpha_0 = np.radians(angle)
    r_0 = R * np.sin(alpha_0)  # Polar opening radius. BC for initial drawing of each layer.
    m_R = 2 * pi * R * np.cos(alpha_0) / b
    m_0 = 2 * pi * r_0 * np.cos(alpha_0) / b
    r_b = r_0 + b
    r_2b = r_0 + 2 * b
    n_R = t_R / (2 * t_P)


def pd(degree):
    """
    Utility function / shorthand
    Returns substraction of powers of order :degree: for r_2b and r_b
    :param degree: exponent of the substraction of powers
    :return:
    """
    return r_2b ** degree - r_0 ** degree


def get_a_vec(angle):
    """
    Obtain vector of coefficients for the polynomial (cubic spline) for the thickness in region 1
    :param angle: nominal winding angle of the layer
    :return: vector of coefficients :a: of the polynomial such that dot(a, [x**0, x**1, x**2, x**3]) is a polynomial
    """
    # Setting up linear system: A c = a,
    # A is a matrix with the constraints and c is the independent-terms vector [TODO reference]
    A = np.array([
        [1., r_0, r_0 ** 2, r_0 ** 3],
        [1., r_2b, r_2b ** 2, r_2b ** 3],
        [0., 1., 2 * r_2b, 3 * r_2b ** 2],
        [pi * (pd(2)), 2 * pi / 3 * (pd(3)), pi / 2 * (pd(4)), 2 * pi / 5 * (pd(5))],
    ])

    # c - vector - independent terms
    c_0 = t_R * pi * R * np.cos(angle) / (m_0 * b)
    c_1 = m_R * n_R / pi * (np.arccos(r_0 / r_2b) - np.arccos(r_b / r_2b)) * t_P
    c_2 = m_R * n_R / pi * (r_0 / (r_2b * np.sqrt(pd(2))) - r_b / (r_2b * np.sqrt(r_2b ** 2 - r_b ** 2))) * t_P

    int_1, _ = quad(lambda r: r * np.arccos(r_0 / r), r_0, r_b)
    int_2, _ = quad(lambda r: r * np.arccos(r_0 / r_2b) - r * np.arccos(r_b / r_2b), r_b, r_2b)

    c_3 = 2. * m_R * n_R * t_P * (int_1 + int_2)

    c = np.array([c_0, c_1, c_2, c_3])

    _a_vec = np.linalg.solve(A, c)  # calculate vector of coefficients for the polynomial by inversion of A

    return _a_vec


# Use previous information to build Segments of the piecewise curve:
# Segment 1
# polynomial object. Already callable and vectorized.
def thickness_1():
    """
    :return: vectorized function that takes an array of r coordinates
    and returns an array of equal length of thickness values
    """
    # Callable and vectorized. To be called on array of "radius coordinate" values (lin-space)
    # Vector is flipped because of difference in nomenclature between reference and numpy
    return np.poly1d(np.flip(get_a_vec(alpha_0)))


# Segment 2
def thickness_2(r):  # Callable and vectorized. To be called on array of "r" values (lin-space)
    r = np.asarray(r)
    # remove numerical errors -- set undefined regions of the domain of arccos to 1, in order to return pi
    arg_1 = r_0 / r
    arg_1[arg_1 >= 1] = 1
    arg_2 = r_b / r
    arg_2[arg_2 >= 1] = 1
    t = (m_R * n_R / pi) * (np.arccos(arg_1) - np.arccos(arg_2)) * t_P
    return np.nan_to_num(t)


# Joining two sections:
def thickness(r):
    """
    aggregates the thickness distribution of a layer from the two regions
    aggregation obtained as a piecewise function using logical masks for the regions
    :param r:
    :return:
    """
    r = np.asarray(r)
    t = np.zeros(r.shape)  # initialize thickness array to all zeros

    # First case: r <= r_2b
    # extract polynomial for given globs
    _thickness_1 = thickness_1()
    t += _thickness_1(r) * ((_thickness_1(r) >= 0) & (r <= r_2b))  # multiply by logical mask
    # Second case
    t += thickness_2(r) * (r_2b < r)  # multiply by logical mask

    t[r == r.max()] = t_R  # set cylindrical region as constant thickness

    return t


def smoothen_curve(t, x, y):  # TODO fix and refalctor
    """
    Smoothing function for low-angle helical layers, typically < 30°
    Makes layers seek the liner horizontally
    :param x:
    :param t:
    :param y:
    :return:
    """
    layer_mask = t > 0  # Logical Mask indicating the layer region
    # find index where layer peaks height
    max_y_idx = (y * layer_mask).argmax()  #

    target = np.argmin(np.abs(y[max_y_idx] - y[:max_y_idx - 1]))
    # ## build a mask that is: True below layer maximum point value AND before max_y_idx
    # left of flag index
    aux_mask = np.zeros(y.shape, dtype="bool")  # initialize as all false of the same shape as y
    aux_mask[:max_y_idx] = True
    # and below maximum y point
    aux_mask = np.logical_and(aux_mask, y < y[max_y_idx])

    x_indices = np.where(aux_mask)[0]
    if x_indices.size > 0:
        y[aux_mask] = y[max_y_idx]  # update y inside mask to be constant as the highest y value
        # create a linspace to distribute the x values
        x[aux_mask] = np.linspace(x[x_indices[0]] + 1, x[max_y_idx], aux_mask.sum())

    return x, y


def thickness_hoop(y, thickness_development=20):
    """
    Calculates the thickness distribution of hoop layers based on a given vertical position array.

    Parameters:
    - y (array-like): Array of vertical positions.
    - thickness_development (float, optional): Distance in mm it takes a hoop layer to achieve max thickness.
        Default is 20.

    Returns:
    - t (numpy array): Array representing the thickness distribution.
    """
    # Initialize arrays
    y = np.asarray(y)
    t = np.zeros(y.shape)

    y_start = max_y_hoop  # starting y position of the hoop layer
    t_0 = t_hoop

    y_end = y_start - thickness_development  # ending y position of the hoop development
    idx_start = np.argmin(np.abs(y - y_start))
    idx_end = np.argmin(np.abs(y - y_end))

    # Square root function is used to describe the thickness
    t[idx_start: idx_end] = t_0 * (np.linspace(0, 1, np.abs(idx_start - idx_end))) ** 0.5
    t[idx_end:] = t_0

    return t


def calculate_cleaner_mask(x, y):
    # ignore 1 cm to the right of the opening, where high curvature is expected
    ignored_region = x < x.min() + 10

    dx = np.gradient(x)
    dy = np.gradient(y)
    ddx = np.gradient(dx)
    ddy = np.gradient(dy)

    curvature = np.abs(np.gradient(dx * ddy - dy * ddx)) / (dx ** 2 + dy ** 2) ** 1.5
    curvature[ignored_region] = 0.
    cleaner_mask = curvature < 0.1

    return cleaner_mask


def detect_layer_and_topmost(r, g, x, y):
    # define layer region: where previous topmost points (r, g) deviate from new topmost (x, y)
    # ~( x = r ^ y = g )
    layer_mask = np.logical_not(np.logical_and(np.equal(x, r), np.equal(y, g)))
    first_true = np.argmax(layer_mask)
    layer_mask[first_true - 1] = True  # pad one time
    x_layer, y_layer = x[layer_mask], y[layer_mask]
    layer_points = (x_layer, y_layer)  # Both members of the tuple are a list of floats
    topmost_points = (x, y)  # used to calculate next layer. do not store.
    return layer_points, topmost_points


def calculate_layer_points(r, g, smoothing_threshold=30):
    """
    :param smoothing_threshold:
    :param r: r coordinates of the previous topmost points
    :param g: y coordinates of the previous topmost
    :return x:
    :return y:
    :return r:
    :return g:
    """
    # calculate the appropriate thickness distribution
    if angle_deg == 90:
        t = thickness_hoop(g)
    else:
        t = thickness(r)

    df = np.gradient(r)  # derivative wrt parameter, i.e., index
    dg = np.gradient(g)
    den = np.sqrt(df ** 2 + dg ** 2)
    # calculate new points
    x = r - t * dg / den
    y = g + t * df / den

    # --- smoothing to enter neck ---
    if angle_deg < smoothing_threshold:
        x, y = smoothen_curve(t, x, y)
    # --- cleaning points of high curvature
    g, r, x, y = remove_anomalous_points(x, y, r, g)

    layer_points, topmost_points = detect_layer_and_topmost(r, g, x, y)
    return layer_points, topmost_points


def remove_anomalous_points(x, y, r, g):
    cleaner_mask = calculate_cleaner_mask(x, y)
    x, y, r, g = x[cleaner_mask], y[cleaner_mask], r[cleaner_mask], g[cleaner_mask]  # TODO avoid unpacking

    return g, r, x, y


def interpolate_liner_by_arclength(liner: Curve):
    x = liner.x()
    y = liner.y()
    # Compute the cumulative arc length
    diff = np.diff(liner.points)
    distances = np.sqrt((diff ** 2).sum(axis=1))  # 1-D array
    cumulative_length = np.insert(np.cumsum(distances), 0, 0)
    # Interpolate based on arc length
    # Determine the desired distance between interpolated points
    desired_distance = 0.5  # mm - Adjust this value as needed
    s = np.arange(0, cumulative_length[-1], desired_distance)
    interpolator_kind = 'cubic'
    x_interp_func = interp1d(cumulative_length, x, kind=interpolator_kind)
    y_interp_func = interp1d(cumulative_length, y, kind=interpolator_kind)
    x = x_interp_func(s)
    y = y_interp_func(s)
    x[-1], y[-1] = liner.points
    return x, y


def calculate_layup(angles, x, y):
    global R
    # # Initialize topmost as shape of the liner
    topmost_points = (x, y)  # tuple containing two arrays
    # draw layup routine
    initial_line = tuple(zip(x, y))
    lines = (initial_line,)  # accum. for the splines that represent the layers
    landmarks = (initial_line[-1],)  # accum. for important landmarks
    for angle in angles:
        # overwrite globals
        define_global_variables(angle)
        # calculate outer contour of new layer
        # x = linespace used, y = topmost wrt whom to calculate

        R = topmost_points[0].max()

        layer_points, topmost_points = calculate_layer_points(topmost_points[0], topmost_points[1], 30)  # TODO points and index, no need to replicate data

        # extract points (redundant, readability)

        x = layer_points[0]
        y = layer_points[1]

        line2 = tuple(zip(x, y))
        landmark = line2[-1]

        lines += (line2,)
        landmarks += (landmark,)

        disp = "-o"
        if RUNNING_STANDALONE:
            global ax1, ax2
            # plot(*layer_points, disp)
            line1, = ax1.plot(x, y, disp)

            line2, = ax2.plot(x[x < 159], thickness(x)[x < 159], disp)
            # line2.set_label(f'alpha={angle}')
            # ax2.legend()
    return lines, landmarks


def main():
    filename = r'..\resources\liner.csv'
    liner = Curve(np.loadtxt(filename, delimiter=",", skiprows=0))

    # extract points from liner


    global R
    R = liner.x().max()
    angles = dv.get_angles()

    # initial values are those of the liner
    define_global_variables(angles[0])

    x, y = interpolate_liner_by_arclength(liner)

    if RUNNING_STANDALONE:
        initialize_plots(x, y)

    landmarks, lines = calculate_layup(angles, x, y)

    return lines, landmarks


def initialize_plots(x, y):
    global ax1, ax2, f1, f2
    f1, ax1 = plt.subplots()
    f1.suptitle('Plot of the stacked layers', fontsize=16)
    ax1.set_xlabel('radial coordinate -- x (mm)')
    ax1.set_ylabel('axial coordinate -- y (mm)')
    line, = ax1.plot(x, y, c="k")
    line.set_label('Liner outer shape')
    # ax1.legend()
    f2, ax2 = plt.subplots()
    custom_cycler = (cycler(color=['b', 'r', 'g', 'm', 'xkcd:purple']))
    ax2.set_prop_cycle(custom_cycler)
    f2.suptitle('Thickness progression at different winding angles', fontsize=16)
    ax2.set_xlabel('radial coordinate (mm)')
    ax2.set_ylabel('thickness(mm)')


if __name__ == "__main__":
    # Initialize global variables
    r_0 = m_R = m_0 = r_b = r_2b = n_R = alpha_0 = angle_deg = R = t_p = 0.
    f1 = ax1 = f2 = ax2 = None
    main()

    plt.show()

    # add_zoom(f1, ax1)

    # f2.savefig(r'D:\Simon\Documentos\Bewerbungen\CSE\test.svg')

    # y = np.linspace(500, 0, 1000)
    # r = thickness_hoop(y)
    # fig, ax = plt.subplots()
    #
    # fig.suptitle('Thickness progression for Hoop layers', fontsize=16)
    # ax.set_xlabel('axial coordinate y (mm)')
    # ax.set_ylabel('thickness t (mm)')
    # line, = ax.plot(y, r, c='b')
    # line.set_label('alpha = 90')
    # ax.invert_xaxis()
    # ax.legend()
