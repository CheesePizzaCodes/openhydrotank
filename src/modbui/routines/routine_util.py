import routine_constants as rc
import math

#####
# - obsolete

"""
Draws a line in the sketch that connects the points inside the passed list of tuples
:param sketch: Sketch
:param points: List of tuples e.g. [(0,0), (1,1), (2,1), (2,0), (0,0)]
:return:
"""


def draw_line(sketch, points):
    for i, point in enumerate(points):
        try:
            sketch.Line(point1=point, point2=points[i + 1])
        except:
            pass  # TODO refactor exception handling. This may cause problems.


def draw_lines(sketch, lines):
    """
    Draws a
    :param sketch:
    :param lines: a list of lists of tuples
    :return:
    """
    for line in lines:
        draw_line(sketch, line)


##Drawing things
# def draw_line(sketch, points):
#     pass
# ####

# - obsolete


#  create set on layup for contact with liner
def offset_point(point, direction):
    """
    this function recei
    :param point: location of the origin point of interest. tuple of floats in mm.
    :param direction: direction of offset. Angle in degrees.
    :return: location. Tuple of floats of the new location
    """
    tol = rc.TOL  # offset tolerance
    direction = math.radians(direction)  # offset direction in radians
    offset = (tol * math.cos(direction), tol * math.sin(direction), 0.)
    location = tuple(map(sum, zip(point, offset)))  # calculate new position by adding vectors
    return location
