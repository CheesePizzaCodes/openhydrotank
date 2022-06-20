import sys, os

import numpy as np

sys.path.append('E:\\Current Workspace\\Codebase\\hydrotank\\src\\modbui\\routines')

# import abaqus modules
# from abaqus import *
# from abaqusConstants import *
# import __main__
# import section
# import regionToolset
# import displayGroupMdbToolset as dgm
# import part
# import material
# import assembly
# import step
# import interaction
# import load
# import mesh
# import optimization
# import job
# import visualization
# import xyPlot
# import displayGroupOdbToolset as dgo
# import connectorBehavior

from time import time

# import own modules
import routine_util as ru
from design_variables import R, angles, pi
import routine_constants as rc

filename = 'E:\\Current Workspace\\Codebase\\hydrotank\\src\\modbui\\routines\\liner.csv'

liner = np.loadtxt(open(filename), delimiter=",", skiprows=0)


def get_gamma(position, layer_number):
    # baseline = lines[layer_number]
    baseline = list(zip(*liner))
    gamma_array = np.arctan(np.gradient(baseline[0], baseline[1]))
    idx = (np.abs(baseline[1] - position)).argmin()
    return gamma_array[idx]


def get_alpha(position, layer_number):
    alpha_0 = np.radians(angles[layer_number - 1])
    try:
        alpha = np.arcsin(R * np.sin(alpha_0) / position)  # R * sin(alpha_0 / r)
    except FloatingPointError:
        alpha = 90 * pi / 180
    return alpha


def get_basis(element, layer_number):
    # Calculate centroid
    vertices = np.array([node.coordinates for node in element.getNodes()])[:, 0:2]  # TODO change to tuple for speed
    location = vertices.mean(axis=0)  # 0: x, radial; 1:y axial  # TODO change for faster routine

    # Calculate alpha
    alpha = get_alpha(location[0], layer_number)  # takes radial value
    # Calculate gamma
    gamma = get_gamma(location[1], layer_number)  # takes axial value
    # Calculate trig functions
    sa, ca, sg, cg = np.sin(alpha), np.cos(alpha), np.sin(gamma), np.cos(gamma)
    # Build rotation tensor

    tensor = np.eye(3)

    # beta_1 = np.array([[sa, -ca, 0.],
    #                    [ca, sa, 0.],
    #                    [0, 0, 1.]])

    beta_1 = np.eye(3)

    tensor = np.matmul(beta_1, tensor)

    # beta_2 = np.array([[1, 0., 0],
    #                    [0, 0., 1],
    #                    [0., 1, 0.]])

    beta_2 = np.eye(3)

    tensor = np.matmul(beta_2, tensor)

    beta_3 = np.array([[cg, -sg, 0.],
                       [sg, cg, 0.],
                       [0., 0., 1.]])

    tensor = np.matmul(beta_3, tensor)

    tensor = tensor.T

    g_1, g_2 = np.matmul(tensor, np.array([1, 0, 0])), np.matmul(tensor, np.array([0, 1, 0]))

    return element.label, np.concatenate((g_1, g_2), axis=0)


def main(_lines):
    global lines
    lines = _lines
    # # Define part
    prt = mdb.models['model'].parts['layup']

    # Extract array of Set objects

    sts = prt.sets

    sts = [(int(key.split("_")[-1]), sts[key]) for key in sts.keys() if key.startswith('set_layer')]  # Filter: only layer sets

    indices_list = []

    bases_list = []

    for layer_number, st in sts:
        for element in st.elements:
            idx, basis = get_basis(element, layer_number)
            indices_list.append(idx), bases_list.append(basis)

    indices_list, bases_list = tuple(np.array(indices_list).flatten()), tuple(np.array(bases_list).flatten())

    mdb.models[rc.MODEL].DiscreteField(name=rc.ORIENTATION,
                                       description='',
                                       location=ELEMENTS,
                                       fieldType=ORIENTATION,
                                       dataWidth=6,
                                       defaultValues=(1.0, 0.0, 0.0, 0.0, 1.0, 0.0),
                                       data=(('',
                                              6,
                                              indices_list,
                                              bases_list),),
                                       orientationType=CARTESIAN, partLevelOrientation=True)

l = (1,2,)
                                       
if __name__ == "__main__":
    main(l)
