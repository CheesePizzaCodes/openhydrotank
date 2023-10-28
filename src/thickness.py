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

    t[t <= 0.05] = 0.

    return t


def smoothen_curve(t: np.ndarray, curve: Curve):  # TODO fix and refalctor
    """
    Smoothing function for low-angle helical layers, typically < 30°
    Makes layers seek the liner horizontally
    :param x:
    :param t:
    :param y:
    :return:
    """
    x = curve.x
    y = curve.y
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
    curve.points = np.column_stack((x, y))
    return curve


def thickness_hoop(y, thickness_development=40):
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


def calculate_cleaner_mask(curve: Curve):
    # DEPRECATED
    # ignore 1 cm to the right of the opening, where high curvature is expected
    x, y = curve.unpack_xy()
    ignored_region = x < x.min() + 10  # Todo check the validity of these int literals

    dx = np.gradient(x)
    dy = np.gradient(y)
    ddx = np.gradient(dx)
    ddy = np.gradient(dy)

    curvature = np.abs(np.gradient(dx * ddy - dy * ddx)) / (dx ** 2 + dy ** 2) ** 1.5
    curvature[ignored_region] = 0.
    cleaner_mask = curvature < 0.05

    return cleaner_mask


def detect_layer_start(prev: Curve, new: Curve):
    # define layer region: where previous topmost points (r, g) deviate from new topmost (x, y)
    # ~( x = r ^ y = g )\
    r, g = prev.unpack_xy()
    x, y = new.unpack_xy()

    layer_mask = np.logical_not(np.logical_and(np.equal(x, r), np.equal(y, g)))
    first = np.argmax(layer_mask) - 1

    return first


def calculate_layer_points(previous_topmost: Curve, smoothing_threshold=30) -> Curve:
    """
    :param previous_topmost: previous curve
    :param smoothing_threshold: Minimum angle at which neck smoothing occurs
    """
    # unpack values
    x, y = previous_topmost.unpack_xy()

    # calculate the appropriate thickness distribution
    match angle_deg:
        case 90.:
            t = thickness_hoop(y)
        case _:
            t = thickness(x)

    dx = np.gradient(x)  # derivative wrt parameter of parametric curve, i.e., index
    dy = np.gradient(y)
    den = np.sqrt(dx ** 2 + dy ** 2)
    # calculate new points
    x = x - t * dy / den
    y = y + t * dx / den
    # compensate for the loss of a point when applying diff

    new_curve = Curve.from_unpacked_xy(x, y)

    # --- smoothing to enter neck ---
    if angle_deg < smoothing_threshold:
        new_curve = smoothen_curve(t, new_curve)
    # --- cleaning points of high curvature

    # cleaner_mask = calculate_cleaner_mask(new_curve)
    #
    # for _ in [new_curve, previous_topmost]:
    #     # _.apply_mask(cleaner_mask)
    #     pass

    start_idx = detect_layer_start(previous_topmost, new_curve)
    new_curve.layer_start_index = start_idx
    return new_curve



def interpolate_layer_region_constant_arclength(curve: Curve) -> Curve:
    pts = curve.get_layer_points().copy()

    # Compute the cumulative arc length
    diff = np.diff(pts, axis=0)
    distances = np.sqrt((diff ** 2).sum(axis=1))  # 1-D array
    cumulative_length = np.insert(np.cumsum(distances), 0, 0)
    # Interpolate based on arc length
    # Determine the desired distance between interpolated points
    desired_distance = 1.5  # mm - Adjust this value as needed
    s = np.arange(0, cumulative_length[-1], desired_distance)
    interpolator_kind = 'linear'
    interp_func = interp1d(cumulative_length, pts, kind=interpolator_kind, axis=0)

    if curve.layer_start_index is None:  # Liner
        curve.points = interp_func(s)
    else:
        head = curve.get_non_layer_points()
        tail = interp_func(s)
        curve.points = np.concatenate((head, tail), axis=0)
    curve.points[-1, -1] = 0.  # Guarantee that the curve finishes in y=0
    return curve


def calculate_layup(angles: List[float], liner: Curve) -> CurvesBunch:
    # data initialization
    curves = CurvesBunch([liner, ])  # initialize container
    global R
    R = liner.x.max()
    topmost_curve = liner

    for angle in angles:
        # overwrite globals
        define_global_variables(angle)
        # calculate new curve
        topmost_curve = calculate_layer_points(topmost_curve, 30)  # TODO points and index, no need to replicate data
        # add new Curve to Bunch
        topmost_curve = interpolate_layer_region_constant_arclength(topmost_curve)
        topmost_curve.winding_angle = angle
        curves.add_curve(topmost_curve)
        if RUNNING_STANDALONE:
            update_layup_graph(topmost_curve)

    return curves


def update_layup_graph(curve: Curve):
    x, y = curve.get_layer_unpacked_xy()

    disp = "-o"
    global ax1, ax2, ax3

    line1, = ax1.plot(x, y, disp)
    match curve.winding_angle:
        case 90:
            line3, = ax3.plot(y, thickness_hoop(y), disp)
        case None:
            pass
        case _:
            line3, = ax2.plot(x, thickness(x), disp)


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
