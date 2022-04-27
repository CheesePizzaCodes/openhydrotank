'''
Medium-level abaqus routine
Creates axisymmetric part with twist

in: list of curves in the form of (x,y) that conform a closed shape
points = [(x,y)], list of tuples, each tuple is the coordinates of the line segment
out: axisymmentric part with twist generated inside CAE
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

# import own modules
import routine_util as ru
import routine_constants as rc
import stubs as stb

import time

start_time = time.time()

points = stb.test_shape  # stub. TODO replace by xml read

# initialize model TODO separate to another routine

model = mdb.Model(name=rc.MODEL, modelType=STANDARD_EXPLICIT)

#  --------- create Layup part

# initialize sketch
s = mdb.models[rc.MODEL].ConstrainedSketch(name='__profile__', sheetSize=10)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints

# draw symmetry line
s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))  # TODO remove for optimization

# use passed list of curves to produce a closed section
ru.draw_line(s, points)

# Create part
p = mdb.models[rc.MODEL].Part(name=rc.LAYUP_PART, dimensionality=AXISYMMETRIC,
                              type=DEFORMABLE_BODY, twist=ON)
p = mdb.models[rc.MODEL].parts[rc.LAYUP_PART]
p.BaseShell(sketch=s)
s.unsetPrimaryObject()
p = mdb.models[rc.MODEL].parts[rc.LAYUP_PART]
del mdb.models[rc.MODEL].sketches['__profile__']

#  Create set containing all of the composite part
part = mdb.models[rc.MODEL].parts[rc.LAYUP_PART]
part.Set(faces=part.faces, name=rc.LAYUP_SET)  # TODO refactor names to global constants

# time script for debugging

end_time = time.time()

total_time = end_time - start_time

print(total_time)

#  --------- end create Layup part

#  --------- create liner part
acis = mdb.openAcis(rc.LINER_PATH, scaleFromFile=OFF)
mdb.models[rc.MODEL].PartFromGeometryFile(name=rc.LINER_PART, geometryFile=acis,
                                          combine=False, dimensionality=AXISYMMETRIC,
                                          type=DEFORMABLE_BODY,
                                          twist=ON)

#  create set containing part
part = mdb.models[rc.MODEL].parts[rc.LINER_PART]
part.Set(faces=part.faces, name=rc.LINER_SET)
#  --------- end create liner part
