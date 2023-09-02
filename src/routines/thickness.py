"""
Thickness computation routine

Run from 'routines' directory
"""
import sys

# Toggles if the code is rand standalone to graph
# or by Abaqus to plot the geometry
# True: graphing is enabled, i.e., running standalone, not in the abaqus interpreter
RUNNING_STANDALONE = 'ABQcaeK.exe' not in sys.executable

import numpy as np

if RUNNING_STANDALONE:
    import matplotlib.pyplot as plt
    from cycler import cycler

from scipy.integrate import quad
from scipy.interpolate import interp1d

import design_variables
from design_variables import b, t_R, t_P, pi

filename = r'..\resources\liner.csv'

liner = np.loadtxt(filename, delimiter=",", skiprows=0)

# extract points from liner
liner_r = liner[:, 0]
liner_y = liner[:, 1]

# Initialize global variables
r_0 = m_R = m_0 = r_b = r_2b = n_R = alpha_0 = angle_deg = 0.


def define_global_variables(angle):
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
    t = np.zeros(r.shape)

    # First case
    # extract polynomial for given globs
    polynomial = thickness_1()
    t += polynomial(r) * ((polynomial(r) >= 0) & (r <= r_2b))
    # Second case
    t += thickness_2(r) * (r_2b < r)

    t[r == r.max()] = 0.65

    tol = 0.085
    # tol = 0
    t[t < tol] = 0

    return t
def smoothen_curve(t, x, y):
    """
    Smoothing function for low-angles (helical layers)
    Makes layers seek the liner horizontally
    :param x:
    :param t:
    :param y:
    :return:
    """
    layer_mask = t > 0  # Logical Mask indicating the layer region
    # find index where layer peaks height
    idx = (y * layer_mask).argmax()  #

    target = np.argmin(np.abs(y[idx] - y[:idx - 1]))
    # ## build mask: True below layer maximum point value AND below flag idx
    # left of flag index
    aux_mask = np.zeros(y.shape, dtype="bool")
    aux_mask[:idx] = True
    # and below maximum y point
    aux_mask = np.logical_and(aux_mask, y < y[idx])
    # delete all points from all vectors that fulfill the condition

    try:
        x_target = np.where(aux_mask)[0][0]

        y[aux_mask] = y[idx]  # project points to target

        x[aux_mask] = np.linspace(x[x_target] + 1, x[idx], aux_mask.sum())

    except IndexError:
        x, y = x, y

    return x, y


def thickness_hoop(y):
    # Initialize arrays
    y = np.asarray(y)
    t = np.zeros(y.shape)

    y_0 = 378.
    t_0 = 0.72
    y_1 = y_0 - 20
    idx_0 = np.argmin(np.abs(y - y_0))
    idx_1 = np.argmin(np.abs(y - y_1))

    t[idx_0: idx_1] = t_0 * (np.linspace(0, 1, np.abs(idx_0 - idx_1))) ** 0.5
    t[idx_1:] = t_0

    return t


def calculate_cleaner_mask(x, y):
    dx = np.gradient(x)
    dy = np.gradient(y)
    ddx = np.gradient(dx)
    ddy = np.gradient(dy)

    curvature = np.abs(np.gradient(dx * ddy - dy * ddx)) / (dx ** 2 + dy ** 2) ** 1.5

    cleaner_mask = curvature < 0.1

    cleaner_mask[x < 40] = True
    return cleaner_mask


def draw_layer(r, g, make_smooth):
    """
    :param r: r coordinates of the liner (or previous topmost) points
    :param g: z coordinates of the liner bzw. previous topmost
    :return: Tuple of points belonging to the new layer
    """
    # calculate thickness distribution

    if angle_deg == 90:
        t = thickness_hoop(g)

    else:
        t = thickness(r)

    df = np.gradient(r)  # derivative wrt parameter, e.g., index
    dg = np.gradient(g)
    den = np.sqrt(df ** 2 + dg ** 2)
    # calculate new points
    x = r - t * dg / den
    y = g + t * df / den

    # --- smoothing ---
    if make_smooth:
        x, y = smoothen_curve(t, x, y)
    # ---
    cleaner_mask = calculate_cleaner_mask(x, y)

    x, y, r, g = x[cleaner_mask], y[cleaner_mask], r[cleaner_mask], g[cleaner_mask]

    # finally, evaluate returns. distinction between zero thickness considered vs deleted

    # define layer region: where previous top (g) deviates from new top (y)
    layer_mask = np.logical_not(np.logical_and(np.equal(x, r), np.equal(y, g)))

    if len(layer_mask) == 1:  # TODO
        first_true = np.where(layer_mask)[0]
    else:
        first_true = np.where(layer_mask)[0][0]

    layer_mask[first_true - 1] = True  # pad one time

    x_layer, y_layer = x[layer_mask], y[layer_mask]

    layer_points = (x_layer, y_layer)  # Both members of the tuple are a list of floats
    topmost_points = (x, y)  # used to calculate next layer. do not store.
    return layer_points, topmost_points


def main():
    global R
    R = liner_r.max()
    angles = design_variables.get_angles()

    # initial values are those of the liner

    # TODO massive refactor, check that everything makes sense...
    define_global_variables(angles[0])

    zone_1 = np.diff(liner_r) != 0  # TODO delete this technicality, as parameter is now index. No need.

    zone_1 = np.append(zone_1, False)

    # initialize parametric curve to shape of liner  # TODO maybe this will be obsolete
    # r = liner_r[zone_1]
    # g = liner_y[zone_1]

    #  Obtain original guide points
    r = liner_r
    g = liner_y

    global t_p
    t_p = 100
    # b_p = 50
    #
    # create sampling points
    ls = np.linspace(g.max(), g.min(), 200)
    #
    aux_ls = np.linspace(440, 540, t_p)
    ls = np.unique(np.concatenate((ls, aux_ls)))
    ls = ls[::-1]
    #
    # aux_ls = np.linspace(ls[0], ls[0] + 10, b_p)
    # ls = np.unique(np.concatenate((ls, aux_ls)))

    # modify original sampling to increase granularity in trailing section
    interp = interp1d(g, r, kind="cubic")

    g = ls
    r = interp(g)

    # # Initialize topmost as shape of the liner
    topmost_points = (r, g)
    f2 = 0
    if RUNNING_STANDALONE:
        f1, ax1 = plt.subplots()
        f1.suptitle('Plot of the stacked layers', fontsize=16)
        ax1.set_xlabel('radial coordinate -- r (mm)')
        ax1.set_ylabel('axial coordinate -- y (mm)')
        line, = ax1.plot(r, g, c="k")
        line.set_label('Liner outer shape')
        ax1.legend()

        f2, ax2 = plt.subplots()
        custom_cycler = (cycler(color=['b', 'r', 'g', 'm', 'xkcd:purple']))
        ax2.set_prop_cycle(custom_cycler)
        f2.suptitle('Thickness progression at different winding angles', fontsize=16)
        ax2.set_xlabel('radial coordinate (mm)')
        ax2.set_ylabel('thickness(mm)')

    # draw layup routine TODO make method

    initial_line = tuple(zip(r, g))

    # initial_line += ((r[-1], 0),)  # pad end straight line2

    lines = (initial_line,)  # accum. for the splines that represent the layers
    landmarks = (initial_line[-1],)  # accum. for important landmarks

    # plt.set_cmap("Pastel1")

    for angle in angles:
        # overwrite globals
        define_global_variables(angle)
        # calculate outer contour of new layer
        # x = linespace used, y = topmost wrt whom to calculate
        if angle <= 30:
            make_smooth = True
        else:
            make_smooth = False

        R = topmost_points[0].max()

        layer_points, topmost_points = draw_layer(topmost_points[0], topmost_points[1],
                                                  make_smooth)  # TODO make_smooth parameter is obsolete since angle_deg is a global parameter now

        # extract points (redundant, readability)

        x = layer_points[0]
        y = layer_points[1]

        line2 = tuple(zip(x, y))
        landmark = line2[-1]

        lines += (line2,)
        landmarks += (landmark,)

        disp = "-o"
        if RUNNING_STANDALONE:
            # plot(*layer_points, disp)
            line1, = ax1.plot(x, y, '')

            line2, = ax2.plot(x[x < 159], thickness(x)[x < 159], disp)
            # line2.set_label(f'alpha={angle}')
            ax2.legend()

    if RUNNING_STANDALONE:
        return lines, landmarks, f1, ax1, f2, ax2
    else:
        return lines, landmarks


if __name__ == "__main__":
    _, _, f1, ax1, f2, ax2 = main()

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
