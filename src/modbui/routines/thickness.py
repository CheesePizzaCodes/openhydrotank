import sys, os, time

cwd = os.getcwd()

sys.path.append('E:\\Current Workspace\\Codebase\\hydrotank\\src')

sys.path.append('E:\\Current Workspace\\Codebase\\hydrotank\\src\\modbui')

sys.path.append('E:\\Current Workspace\\Codebase\\hydrotank\\src\\modbui\\routines')

toggle = True

import numpy as np
import scipy as sp

if toggle:
    import matplotlib.pyplot as plt
    from matplotlib.pyplot import plot


from scipy.integrate import quad
from scipy.interpolate import interp1d
from scipy.interpolate import make_interp_spline

import design_variables
from design_variables import angles, b, t_R, t_P, pi

# TODO move to global definition

filename = cwd + '\\liner.csv'

liner = np.loadtxt(open(filename), delimiter=",", skiprows=1)

# extract points from liner
liner_r = liner[:, 0]
liner_y = liner[:, 1]


def globs(angle):
    """
    Calculates the global geometric parameters for this routine.
    These vary with respect to the angle of the layer.
    :param angle: alpha_0. Desired cylindrical-section angle.
    :return:
    """
    # TODO this is calculated on every layer.
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


def a_vec(angle):
    """
    Obtain vector of coefficients for the polynomial (cubic spline) for the thickness in region 1
    :param angle: nominal winding angle of the layer
    :return: vector of coefficients :a: of the polynomial such that dot(a, [x**0, x**1, x**2. x**3]) is a polynomial
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

    int_1, err = quad(lambda r: r * np.arccos(r_0 / r), r_0, r_b)
    int_2, err = quad(lambda r: r * np.arccos(r_0 / r_2b) - r * np.arccos(r_b / r_2b), r_b, r_2b)

    c_3 = 2 * m_R * n_R * t_P * (int_1 + int_2)

    c = np.array([c_0, c_1, c_2, c_3])

    _a_vec = np.linalg.solve(A, c)  # calculate vector of coefficients for the polynomial by inversion of A

    return _a_vec


# Use previous information to build Segments of the piecewise curve:
# Segment 1
# polynomial object. Already callable and vectorized.

def thickness_1(): # Callable and vectorized. To be called on array of "r" values (lin-space)
    t = np.poly1d(np.flip(a_vec(alpha_0))) #  Vector is flipped because of difference in nomenclature between reference and numpy
    return t


# Segment 2
def thickness_2(r):  # Callable and vectorized. To be called on array of "r" values (lin-space)
    r = np.asarray(r)

    # remove numerical errors -- set undefined regions of the domain of arccos to 1, in order to return pi
    arg_1 = r_0 / r
    arg_1[arg_1 >= 1] = 1  # TODO check if the correct default value is 1 or 0

    arg_2 = r_b / r
    arg_2[arg_2 >= 1] = 1

    t = (m_R * n_R / pi) * (np.arccos(arg_1) - np.arccos(arg_2)) * t_P
    t = np.nan_to_num(t)  # TODO remove, probably obsolete and may break something (test first)
    return t


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
    f = 1  # Size factor. Used to half the size of each layer to follow the double-pseudolayer approach

    # First case
    # extract polynomial for given globs
    polynomial = thickness_1()
    t += polynomial(r) * ((polynomial(r) >= 0) & (r <= r_2b))
    # Second case
    t += thickness_2(r) * (r_2b < r)

    tol = 0.085
    t[t < tol] = 0

    return t * f


def smooth(t, y):
    """
    Smoothing function for low-angles (helical layers)
    Makes layers seek the liner horizontally
    :param t:
    :param y:
    :return:
    """
    layer_mask = t > 0  # Logical Mask indicating the layer region ((((preliminarily))))
    # find index where layer peaks height
    idx = (y * layer_mask).argmax()  #
    # ## build mask: True below layer maximum point value AND below flag idx
    # left of flag index
    aux_mask = np.zeros(y.shape, dtype="bool")
    aux_mask[:idx] = True
    # and below maximum y point
    aux_mask = np.logical_and(aux_mask, y < y[idx])
    # delete all points from all vectors that fulfill the condition
    # x, y, r, g = map(lambda v: np.delete(v, aux_mask), (x, y, r, g))
    y[aux_mask] = y[idx]
    return y


def thickness_hoop(y):
    # Initialize arrays
    y = np.asarray(y)
    t = np.zeros(y.shape)
    #
    #
    # y_0 = 380.
    # d = 30.
    # t_0 = 0.6
    # y_d = y_0 - d
    #
    # matrix = np.array([
    #     [1, y_0, y_0 ** 2, y_0 ** 3],
    #     [1, y_d, y_d ** 2, y_d ** 3],
    #     [0, 1, 2 * y_0, 3 * y_0 ** 2],
    #     [0, 1, 2 * y_d, 3 * y_d ** 2],
    # ])
    #
    # vector = np.array([
    #     0., t_0, -1, 0.
    # ])
    #
    # coeffs = np.linalg.solve(matrix, vector)
    #
    # poly = np.poly1d(coeffs)
    #
    # t += poly(y) * ((y > y_0) & (y < y_d))
    #
    # t += t_0 * (y > y_d)

    y_0 = 385.
    t_0 = 0.3
    y_1 = y_0 - 20
    idx_0 = np.argmin(np.abs(y - y_0))
    idx_1 = np.argmin(np.abs(y - y_1))



    t[idx_0: idx_1] = t_0 * (np.linspace(0, 1, np.abs(idx_0 - idx_1))) ** 0.5
    t[idx_1:] = t_0

    return t



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
        y = smooth(t, y)

    # finally, evaluate returns. distinction between zero thickness considered vs deleted

    # define layer region: where previous top (g) deviates from new top (y)
    layer_mask = np.logical_not(np.logical_and(x == r, y == g))
    first_true = np.where(layer_mask)[0][0]
    layer_mask[first_true - 1] = True  # pad one time

    x_layer, y_layer = x[layer_mask], y[layer_mask]

    # Add straight lines towards the bottom of the tank
    # x_layer = np.append(x_layer, x_layer[-1])
    # y_layer = np.append(y_layer, 0)

    layer_points = (x_layer, y_layer)  # Both members of the tuple are a list of floats
    topmost_points = (x, y)  # used to calculate next layer. do not store.
    return layer_points, topmost_points





def main():
    global R
    R = liner_r.max()
    #  bullshit imports not working, bruteforce to bring angles
    angles = design_variables.angles



    # initial values are those of the liner

    # TODO massive refactor, check that everything makes sense...
    globs(angles[0])

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
    # aux_ls = np.linspace(490, 490, t_p)
    # ls = np.unique(np.concatenate((ls, aux_ls)))
    #
    # aux_ls = np.linspace(ls[0], ls[0] + 10, b_p)
    # ls = np.unique(np.concatenate((ls, aux_ls)))

    # modify original sampling to increase granularity in trailing section
    interp = interp1d(g, r, kind="cubic")

    g = ls
    r = interp(g)

    # # Initialize topmost as shape of the liner
    topmost_points = (r, g)

    if toggle:
        f1 = plt.figure(1)  # TODO plot
        plot(r, g, "-o")

    # draw layup routine TODO make method

    initial_line = tuple(zip(r, g))

    # initial_line += ((r[-1], 0),)  # pad end straight line

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
            make_smooth = False

        R = topmost_points[0].max()

        layer_points, topmost_points = draw_layer(topmost_points[0], topmost_points[1], make_smooth)  # TODO make_smooth parameter is obsolete since angle_deg is a global parameter now

        # extract points (redundant, readability)

        x = layer_points[0]
        y = layer_points[1]

        line = tuple(zip(x, y))
        landmark = line[-1]

        lines += (line,)
        landmarks += (landmark,)

        disp = "-o"
        if toggle:
            f1 = plt.figure(1)
            # plot(*layer_points, disp)
            plot(x, y, disp)

            f2 = plt.figure(2)
            plot(x, thickness(x), disp)

    return lines, landmarks


if __name__ == "__main__":
    main()
