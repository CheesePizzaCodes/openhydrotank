'''
Medium-level abaqus routine
Creates axisymmetric part with twist

in: list of curves in the form of (x,y) that conform a closed shape
points = [(x,y)], list of tuples, each tuple is the coordinates of the line segment
out: axisymmentric part with twist generated inside CAE
'''

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

points = stb.test_shape  # stub. TODO replace by xml read

# initialize model TODO separate to another routine

model = mdb.Model(name=rc.MODEL_NAME, modelType=STANDARD_EXPLICIT)

# initialize sketch
s = mdb.models[rc.MODEL_NAME].ConstrainedSketch(name='__profile__',
                                                sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints

# draw symmetry line
s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))

# use passed list of curves to produce a closed section
ru.draw_line(s, points)

# Create part
p = mdb.models[rc.MODEL_NAME].Part(name=rc.PART_NAME, dimensionality=AXISYMMETRIC,
                                   type=DEFORMABLE_BODY, twist=ON)
p = mdb.models[rc.MODEL_NAME].parts[rc.PART_NAME]
p.BaseShell(sketch=s)
s.unsetPrimaryObject()
p = mdb.models[rc.MODEL_NAME].parts[rc.PART_NAME]
del mdb.models[rc.MODEL_NAME].sketches['__profile__']
