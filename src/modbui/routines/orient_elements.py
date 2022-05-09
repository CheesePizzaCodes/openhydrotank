import sys, os

import numpy as np

sys.path.append('E:\\Current Workspace\\Codebase\\hydrotank\\src\\modbui\\routines')

# import abaqus modules
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
import routine_constants as rc

filename = 'E:\\Current Workspace\\Codebase\\hydrotank\\src\\modbui\\routines\\liner.csv'

liner = np.loadtxt(open(filename), delimiter=",", skiprows=0)

y_coord = liner[:, 1]
gamma_array = np.arctan(np.gradient(liner[:, 0], y_coord))


def get_gamma(position):  # TODO this should depend on the bottom of each ply (or top?)
    idx = (np.abs(y_coord - position)).argmin()
    return gamma_array[idx]


def get_alpha(position):  # TODO this should depend on the layer number
    try:
        alpha = np.arcsin(rc.R_0 / position)  # R * sin(alpha_0 / r)
    except FloatingPointError:
        alpha = 90 * pi / 180
    return alpha


def get_basis(element):
    # Calculate centroid
    vertices = np.array([node.coordinates for node in element.getNodes()])[:, 0:2]  # TODO change to tuple for speed
    location = vertices.mean(axis=0)  # 0: x, radial; 1:y axial  # TODO change for faster routine

    # Calculate alpha
    alpha = get_alpha(location[0])  # takes radial value
    # Calculate gamma
    gamma = get_gamma(location[1])  # takes axial value
    # Calculate trig functions
    sa, ca, sg, cg = np.sin(alpha), np.cos(alpha), np.sin(gamma), np.cos(gamma)
    # Build rotation tensor
    beta_1 = np.array([[cg, -sg, 0.],
                       [sg, cg, 0.],
                       [0, 0., 1]])

    beta_2 = np.array([[1., 0., 0.],
                       [0., ca, -sa],
                       [0., sa, ca]])

    tensor = np.matmul(beta_1, beta_2)

    tensor = np.linalg.inv(tensor)

    g_1, g_2 = np.matmul(tensor, np.array([0, 1, 0])), np.matmul(tensor, np.array([0, 0, 1]))

    return element.label, np.concatenate((g_1, g_2), axis=0)


def main():
    # # Define part
    prt = mdb.models['model'].parts['layup']

    # Extract array of Set objects

    sts = prt.sets

    sts = [sts[key] for key in sts.keys() if key.startswith('set_layer')]  # Filter: only layer sets

    indices_list = []

    bases_list = []
    for st in sts:
        for element in st.elements:
            idx, basis = get_basis(element)
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


if __name__ == "__main__":
    main()
