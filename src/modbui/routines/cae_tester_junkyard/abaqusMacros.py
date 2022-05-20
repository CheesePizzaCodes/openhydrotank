# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

def Macro1():
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
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    p = mdb.models['model'].parts['part']
    f = p.faces
    p.RemoveFaces(faceList=(f.findAt(coordinates=(0.1, 0.1, 0.0)), ), 
        deleteCells=False)


def Macro2():
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
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=959.883, 
        farPlane=1109.79, width=581.189, height=265.361, cameraPosition=(
        136.949, 279.145, 1034.83), cameraTarget=(136.949, 279.145, 0))
    s2.Spline(points=((80.0, 360.0), (125.0, 340.0), (85.0, 310.0), (120.0, 290.0), 
        (100.0, 265.0), (120.0, 245.0), (90.0, 225.0), (125.0, 215.0), (115.0, 
        195.0)))


def Macro3():
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
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(viewStyle=AXISYM)
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -0.5), point2=(0.0, 0.5))
    s.Spot(point=(0.0, 0.0))
    s.rectangle(point1=(0.0, 0.0), point2=(0.14, 0.14))
    p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=AXISYMMETRIC, 
        type=DEFORMABLE_BODY, twist=ON)
    p = mdb.models['Model-1'].parts['Part-1']
    p.BaseShell(sketch=s)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']


def outer_geom():
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
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    s = mdb.models['model'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints


 

def Macro5():
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
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    s1 = mdb.models['model'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.sketchOptions.setValues(viewStyle=AXISYM)
    s1.setPrimaryObject(option=STANDALONE)
    s1.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))


    s1.Line(point1=(152.145, 0.0), point2=(152.145, 376.74))
    s1.Line(point1=(190.877349853516, 376.720458984375), point2=(190.877349853515, 
        0.0))
    s1.Arc3Points(point1=(152.145, 376.74), point2=(0.0, 470.92499999851), point3=(
        86.94, 449.19))
    s1.Arc3Points(point1=(190.877349853516, 376.720458984375), point2=(0.0, 
        514.394999997914), point3=(115.92, 492.66))
    s1.Line(point1=(0.0, 470.92499999851), point2=(7.245, 478.17))
    s1.Line(point1=(7.245, 478.17), point2=(0.0, 481.626617431641))
    s1.Line(point1=(0.0, 481.626617431641), point2=(0.548710346221924, 
        481.922241210938))
    s1.Line(point1=(0.548710346221924, 481.922241210938), point2=(0.0, 
        482.335296630859))
    s1.Line(point1=(0.0, 482.335296630859), point2=(0.0, 514.394999997914))
    s1.Line(point1=(152.145, 0.0), point2=(190.877349853515, 0.0))


    p = mdb.models['model'].Part(name='part', dimensionality=AXISYMMETRIC, 
        type=DEFORMABLE_BODY, twist=ON)
    p = mdb.models['model'].parts['part']
    p.BaseShell(sketch=s1)
    s1.unsetPrimaryObject()
    p = mdb.models['model'].parts['part']
    del mdb.models['model'].sketches['__profile__']


def set_explore():
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
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=1255.67, 
        farPlane=1265.01, width=32.8889, height=13.6267, viewOffsetX=249.097, 
        viewOffsetY=62.4134)
    p = mdb.models['model'].parts['part']
    e = p.edges
    edges = e.getSequenceFromMask(mask=('[#7fd55402 #13469a6a #80001 ]', ), )
    p.Set(edges=edges, name='Set-2')


def Macro4():
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
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    p = mdb.models['model'].parts['part']
    e = p.edges
    edges = e.getSequenceFromMask(mask=('[#7fd55402 #13469a6a #80001 ]', ), )
    p.Set(edges=edges, name='Set-3')


def Macro6():
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
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    p = mdb.models['model'].parts['part']
    e = p.edges
    edges = e.findAt(((156.0, 92.125, 0.0), ), ((155.999977, 369.096605, 0.0), ), (
        (81.170196, 465.604991, 0.0), ), ((70.198523, 469.589496, 0.0), ), ((
        59.266901, 472.853661, 0.0), ), ((48.175256, 475.525721, 0.0), ), ((
        38.018894, 477.436949, 0.0), ), ((36.664315, 477.808372, 0.0), ), ((
        42.574745, 476.611439, 0.0), ), ((50.291689, 475.045756, 0.0), ), ((
        53.977505, 474.19497, 0.0), ), ((64.755209, 471.296848, 0.0), ), ((
        75.590258, 467.725689, 0.0), ), ((88.447952, 462.52105, 0.0), ), ((
        151.20131, 403.604307, 0.0), ), ((156.000135, 372.04114, 0.0), ), ((
        34.178707, 479.0994, 0.0), ), ((33.100846, 479.993008, 0.0), ), ((
        32.153366, 481.041068, 0.0), ), ((35.378911, 478.37429, 0.0), ), ((
        30.875487, 483.140924, 0.0), ), ((30.736898, 483.471726, 0.0), ), ((
        31.364912, 482.203373, 0.0), ), ((30.055843, 486.179896, 0.0), ), ((
        29.997859, 487.372025, 0.0), ), ((30.308927, 484.798166, 0.0), ), ((
        30.001778, 488.767555, 0.0), ), ((30.0, 491.893471, 0.0), ), ((
        30.003082, 490.201838, 0.0), ), ((30.0, 492.785645, 0.0), ), ((30.0, 
        496.190937, 0.0), ), ((30.0, 499.586266, 0.0), ))
    p.Set(edges=edges, name='Set-1')


def Macro7():
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
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=1253.08, 
        farPlane=1267.6, width=52.6597, height=14.215, viewOffsetX=240.171, 
        viewOffsetY=65.1418)
    p = mdb.models['model'].parts['part']
    f = p.faces
    faces = f.findAt(((156.480001, 61.422058, 0.0), ))
    p.Set(faces=faces, name='Set-2')


def Macro8():
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
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=1259.34, 
        farPlane=1261.34, width=4.79872, height=1.29537, viewOffsetX=-185.126, 
        viewOffsetY=68.134)
    p = mdb.models['model'].parts['part']
    f = p.faces
    p.RemoveFaces(faceList=(f.findAt(coordinates=(159.153051, 439.055196, 0.0)), ), 
        deleteCells=False)


def Macro9():
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
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=500.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(viewStyle=AXISYM)
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -250.0), point2=(0.0, 250.0))
    s.FixedConstraint(entity=g[2])
    s.rectangle(point1=(47.5, 75.0), point2=(67.5, 65.0))
    p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=AXISYMMETRIC, 
        type=DEFORMABLE_BODY, twist=ON)
    p = mdb.models['Model-1'].parts['Part-1']
    p.BaseShell(sketch=s)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']


def Macro10():
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
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=1464.2, 
        farPlane=1524.84, width=232.005, height=96.1258, viewOffsetX=14.5563, 
        viewOffsetY=143.912)
    p = mdb.models['model'].parts['part']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#10000000 ]', ), )
    p.Set(faces=faces, name='Set-1')


