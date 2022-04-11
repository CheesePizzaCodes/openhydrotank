import routine_constants as rc


def draw_line(sketch, points):
    """
    Draws a line in the sketch that connects the points inside the passed list of tuples
    :param sketch: Sketch
    :param points: List of tuples e.g. [(0,0), (1,1), (2,1), (2,0), (0,0)]
    :return:
    """

    for i, point in enumerate(points):
        try:
            sketch.Line(point1=point, point2=points[i + 1])
        except:
            pass  # TODO refactor exception handling. This may cause problems.