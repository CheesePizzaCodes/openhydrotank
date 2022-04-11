'''
Medium-level abaqus routine
Creates axisymmetric part with twist

in: list of curves in the form of (x,y) that conform a closed shape
points = [(x,y)], list of tuples, each tuple is the coordinates of the line segment
out: axisymmentric part with twist generated inside CAE
'''


#import abaqus modules
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

import routine_util as ru

points = [(0,0), (1,1), (2,1), (2,0), (0,0)] #stub. TODO replace by xml read

#initialize model TODO separate to another routine
Mdb()
model = mdb.models['Model-1']


#initialize sketch
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                                 sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints

#draw symmetry line
s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))

#points = [(0,0), (1,1), (2,1), (2,0), (0,0)] #debug
#use passed list of curves to produce a closed section
ru.draw_line(s, points)

#Create part
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=AXISYMMETRIC,
                                    type=DEFORMABLE_BODY, twist=ON)
p = mdb.models['Model-1'].parts['Part-1']
p.BaseShell(sketch=s)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Part-1']
del mdb.models['Model-1'].sketches['__profile__']
    

