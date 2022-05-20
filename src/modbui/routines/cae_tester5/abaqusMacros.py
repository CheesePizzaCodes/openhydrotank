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
    pass


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
    session.viewports['Viewport: 1'].view.setValues(nearPlane=1129.96, 
        farPlane=1391.33, width=998.861, height=416.516, viewOffsetX=-6.27926, 
        viewOffsetY=94.4956)
    mdb.models['model'].DiscreteField(name='orientations', description='', 
        location=ELEMENTS, fieldType=ORIENTATION, dataWidth=6, defaultValues=(
        1.0, 0.0, 0.0, 0.0, 1.0, 0.0), data=(('', 6, (1, ), (1.0, 0.0, 0.0, 
        0.0, 1.0, 0.0)), ), orientationType=CARTESIAN, 
        partLevelOrientation=True)
    p = mdb.models['model'].parts['layup']
    region = p.sets['set_layup']
    orientation=None
    mdb.models['model'].parts['layup'].MaterialOrientation(region=region, 
        orientationType=FIELD, axis=AXIS_3, fieldName='orientations', 
        localCsys=None, additionalRotationType=ROTATION_NONE, angle=0.0, 
        additionalRotationField='', stackDirection=STACK_3)


