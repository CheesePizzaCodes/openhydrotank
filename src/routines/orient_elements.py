import sys, os

import numpy as np


## import abaqus modules
from abaqus import *
from abaqusConstants import *
import __main__
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior

from time import time

# import own modules
import routine_util as ru
from design_variables import pi, get_angles
import routine_constants as rc

# Extract liner shape
filename = r'.\bin\liner.csv'

try:
    liner = np.loadtxt(open(filename), delimiter=",", skiprows=1)
except:
    alt_filename = 'liner.csv'
    liner = np.loadtxt(open(alt_filename), delimiter=",", skiprows=1)

angles = get_angles()


def get_gamma(position, layer_number):
    baseline = np.array(list(zip(*lines[layer_number])))

    x_vals = baseline[1]
    y_vals = baseline[0]

    x_lengths = np.gradient(x_vals)
    y_lengths = np.gradient(y_vals)

    vec_lengths = np.array([(x ** 2 + y ** 2)**0.5 for x, y in zip(x_lengths, y_lengths)])

    gamma_array = np.arccos(x_lengths / vec_lengths)

    # try:
    #     gamma_array = np.arctan(np.gradient(baseline[0], baseline[1]))
    # except FloatingPointError:
    #     mask_func = np.gradient(baseline[1]) != 0
    #     mask_func[np.where(mask_func == False)[0][0] - 1] = False
    #     mask_func[np.where(mask_func == False)[0][-1] + 1] = False
    #     mask_vert = np.invert(mask_func)
    #
    #     gamma_array = np.zeros(baseline.shape[1])
    #
    #     gamma_array[mask_vert] = - 90 * pi / 180
    #
    #     gamma_array[mask_func] = np.arctan(np.gradient(baseline[0][mask_func], baseline[1][mask_func]))

    idx = (np.abs(baseline[1] - position)).argmin()
    return gamma_array[idx]


def get_alpha(position, layer_number):
    """
    Calculate winding alngle with respect to meridional direction.
    According to Clariaut's equation.
    :param position: radial coordinate in mm
    :param layer_number: self explainatory, int
    :return: array of values for the angle Alpha.
    """
    alpha_0 = np.radians(angles[layer_number - 1])

    R = 160.

    try:  # TODO this is calculated on every layer. R can be dependent on layer number.
        alpha = np.arcsin(R * np.sin(alpha_0) / position)  # R * sin(alpha_0 / r)
        # alpha = np.arcsin(rc.R * np.sin(angle) / position)
    except FloatingPointError:
        alpha = 90 * pi / 180
    return alpha + 90 * pi / 180


def transform_tensor(tensor, transformation):
    _ = tensor
    _ = np.matmul(transformation, _)

    return _


def get_basis(element, layer_number):
    # Calculate centroid
    vertices = np.array([node.coordinates for node in element.getNodes()])[:, 0:2]  # TODO change to tuple for speed
    location = vertices.mean(axis=0)  # 0: x, radial; 1:y axial  # TODO change for faster routine

    # Calculate alpha
    alpha = get_alpha(location[0], layer_number)  #` takes radial value
    # Calculate gamma
    gamma = get_gamma(location[1], layer_number)  # takes axial value
    # Calculate trig functions
    sa, ca, sg, cg = np.sin(alpha), np.cos(alpha), np.sin(gamma), np.cos(gamma)
    # Build rotation tensor

    # initialize
    tensor = np.eye(3)

    # --------------- Permutate
    # beta_1 = np.eye(3)
    beta_1 = np.array([[0, 1, 0],
                       [0, 0, 1],
                       [1, 0, 0.]])
    tensor = transform_tensor(tensor, beta_1)

    # --------------- WRT liner direction
    beta_2 = np.eye(3)
    beta_2 = np.array([[cg, 0, -sg],
                       [0, 1, 0.],
                       [sg, 0., cg]]).T
    tensor = transform_tensor(tensor, beta_2)

    # --------------- With respect to material properties
    beta_3 = np.eye(3)
    beta_3 = np.array([[sa, -ca, 0.],
                       [ca, sa, 0.],
                       [0, 0, 1.]]).T

    tensor = transform_tensor(tensor, beta_3)

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


l = (1, 2,)

if __name__ == "__main__":
    main(l)
