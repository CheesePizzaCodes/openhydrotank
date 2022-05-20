# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2020 replay file
# Internal Version: 2019_09_13-19.49.31 163176
# Run by User on Thu May  5 14:49:31 2022
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=129.239593505859, 
    height=126.0)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
import sys
sys.path.append(r'e:\ABQ2020FILES\Plugins\2020\WoundSimAbaqusPlugin\translate')
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
openMdb(
    pathName='E:/Current Workspace/Codebase/hydrotank/src/modbui/routines/cae_tester3/cae.cae')
#: The model database "E:\Current Workspace\Codebase\hydrotank\src\modbui\routines\cae_tester3\cae.cae" has been opened.
session.viewports['Viewport: 1'].setValues(displayedObject=None)
p1 = mdb.models['model'].parts['part']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
session.viewports['Viewport: 1'].view.setValues(nearPlane=1190.32, 
    farPlane=1330.98, width=602.331, height=236.325, viewOffsetX=55.8592, 
    viewOffsetY=146.166)
session.viewports['Viewport: 1'].view.rotate(xAngle=0, yAngle=0, zAngle=90, 
    mode=MODEL)
mdb.models['model'].parts['part'].setValues(geometryRefinement=EXTRA_FINE)
session.viewports['Viewport: 1'].view.setValues(nearPlane=1243.77, 
    farPlane=1277.52, width=144.902, height=56.8524, viewOffsetX=121.051, 
    viewOffsetY=165.479)
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
