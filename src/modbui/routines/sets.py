'''

 ONLY EXECUTES CREATION OF PREDEFINED SETS IN THE ABAQUS TOOLS
 the sets and surfaces to be used in the model with descriptive names

each layer must be a set TODO done, sorting missing

each part TODO Done :D

each contact face with a descriptive name must be a surface #TODO done

regions with loads #TODO

regions with bc #TODO done :D


TODO convert annoying offset thing to function or something...
'''

import sys, os

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

import time

# import own modules
import routine_util as ru
import routine_constants as rc

start_time = time.time()

# import stubs as stb

print(time.time() - start_time)

sys.path.append('.')

# set work part
p = mdb.models[rc.MODEL].parts[rc.LAYUP_PART]
f = p.faces

# first remove small faces #TODO this is mainly debug. remove later.
# for face in f:
#     if face.getSize() < 1: #delete small faces
#         p.RemoveFaces(faceList=(face,),
#                       deleteCells=False)
# print("flag")

# create one set per layer
part = mdb.models[rc.MODEL].parts[rc.LAYUP_PART]
faces = part.faces
for index, face in enumerate(sorted(faces)):  # this required a workaround using findAt...
    location = face.pointOn  # extract face location
    face_array = part.faces.findAt(location)  # find face at location
    name = rc.LAYER_SET + str(index + 1)  # TODO refactor to global constant
    part.Set(faces=face_array, name=name)

#  create set on layup for contact with liner
part = mdb.models[rc.MODEL].parts[rc.LAYUP_PART]
tol = 0.1  # TODO refactor to reflect model geometric properties. maybe make global constant.
offset = (0., tol, 0.)  # offset in the y-direction
location = map(sum, zip(rc.ROOT_POINT, offset))  # TODO make this a routine utility function
edge = part.edges.findAt(location)
selection = edge.getEdgesByEdgeAngle(rc.GET_EDGES_BY_ANGLE)
part.Set(edges=selection, name=rc.LAYUP_INTERACTION_SET)  # TODO this naming may cause conflicts.

#  create set on liner for contact with layup #TODO this must be done in the assembly, not in the part... :/
part = mdb.models[rc.MODEL].parts[rc.LINER_PART]
tol = 0.1  # TODO refactor to reflect model geometric properties. maybe make global constant.
offset = (0., tol, 0.)  # offset in the y-direction
location = map(sum, zip(rc.ROOT_POINT, offset))  # TODO make this a routine utility function
edge = part.edges.findAt(location)
selection = edge.getEdgesByEdgeAngle(rc.GET_EDGES_BY_ANGLE)
part.Set(edges=selection, name=rc.LINER_INTERACTION_SET)  # TODO this naming may cause conflicts.

# ----create set for symmetry BC #TODO this must be done in the assembly, not in the part... :/ DONE :D
a1 = mdb.models[rc.MODEL].rootAssembly
tol = 0.1  # TODO refactor to reflect model geometric properties. maybe make global constant.

offset1 = (tol, 0., 0.)  # offset in the y-direction
location1 = map(sum, zip(rc.ROOT_POINT, offset1))  # TODO make this a routine utility function
edge1 = a1.instances[rc.LAYUP_INSTANCE].edges.findAt(location1)
selection1 = edge1.getEdgesByEdgeAngle(rc.GET_EDGES_BY_ANGLE)
# TODO DANGER CSYST DEFINITION IS CONFUSING! EVALUATE WHEN IT HAS EFFECT! MODELLING / SELECTING GEOMETRY INSIDE ASSEMBLY
offset2 = (-tol, 0., 0.)  # offset in the y-direction
location2 = map(sum, zip(rc.ROOT_POINT, offset2))  # TODO make this a routine utility function
edge2 = a1.instances[rc.LINER_INSTANCE].edges.findAt(location2)
selection2 = edge2.getEdgesByEdgeAngle(rc.GET_EDGES_BY_ANGLE)

a1.Set(edges=selection1+selection2, name=rc.SYM_BC_SET)  # TODO this naming may cause conflicts.

