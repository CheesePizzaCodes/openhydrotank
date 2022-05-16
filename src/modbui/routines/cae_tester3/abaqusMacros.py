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
    mdb.models['model'].Material(name='Material-1')
    mdb.models['model'].materials['Material-1'].Elastic(type=ENGINEERING_CONSTANTS, 
        table=((1.0, 11.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), ))
    mdb.models['model'].Material(name='Material-2')
    mdb.models['model'].materials['Material-2'].Elastic(table=((1.0, 2.0), ))


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
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
        predefinedFields=ON, connectors=ON)


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
    pass


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
    mdb.models['model'].StaticStep(name='Step-1', previous='Initial')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')


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
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON, 
        constraints=ON, connectors=ON, engineeringFeatures=ON, 
        adaptiveMeshConstraints=OFF)


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
    pass


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
    p1 = mdb.models['model'].parts['liner']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models['model'].parts['liner']
    s = p.edges
    side1Edges = s.getSequenceFromMask(mask=('[#40000 ]', ), )
    p.Surface(side1Edges=side1Edges, name='Surf-1')


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
    mdb.models['model'].StaticStep(name='Step-2', previous='Initial', 
        maxNumInc=10000, initialInc=0.01, maxInc=0.1)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-2')


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
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
        predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=1257.15, 
        farPlane=1482.99, width=965.457, height=402.587, viewOffsetX=16.8036, 
        viewOffsetY=48.4371)
    a = mdb.models['model'].rootAssembly
    region = a.instances['liner_instance'].surfaces['set_load']
    mdb.models['model'].Pressure(name='Load-1', createStepName='Step-2', 
        region=region, distributionType=UNIFORM, field='', magnitude=12.0, 
        amplitude=UNSET)


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
    a = mdb.models['model'].rootAssembly
    region = a.sets['set_sym_bc']
    mdb.models['model'].YsymmBC(name='BC-1', createStepName='Step-2', 
        region=region, localCsys=None)


def Macro11():
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


def Macro12():
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
    mdb.models['model'].ContactProperty('IntProp-1')
    mdb.models['model'].interactionProperties['IntProp-1'].TangentialBehavior(
        formulation=FRICTIONLESS)
    mdb.models['model'].interactionProperties['IntProp-1'].NormalBehavior(
        pressureOverclosure=HARD, allowSeparation=ON, 
        constraintEnforcementMethod=DEFAULT)


def Macro13():
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
    a = mdb.models['model'].rootAssembly
    region1=a.instances['layup_instance'].surfaces['surf_contact_layup']
    a = mdb.models['model'].rootAssembly
    region2=a.instances['liner_instance'].surfaces['surf_contact_liner']
    mdb.models['model'].SurfaceToSurfaceContactStd(name='Int-1', 
        createStepName='Step-1', master=region1, slave=region2, sliding=SMALL, 
        thickness=OFF, interactionProperty='IntProp-1', 
        adjustMethod=OVERCLOSED, initialClearance=OMIT, datumAxis=None, 
        clearanceRegion=None, tied=OFF)


