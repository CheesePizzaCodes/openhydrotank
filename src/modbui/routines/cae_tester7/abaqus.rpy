# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2020 replay file
# Internal Version: 2019_09_13-19.49.31 163176
# Run by User on Mon May  2 18:17:21 2022
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=129.239593505859, 
    height=133.58332824707)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
import sys
sys.path.append(r'e:\ABQ2020FILES\Plugins\2020\WoundSimAbaqusPlugin\translate')
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
import atxPdb;atxPdb.debugFile(
    fileName='e:/Current Workspace/Codebase/hydrotank/src/modbui/build_model.py', 
    serverPort=61358)
import atxPdb;atxPdb.debugFile(
    fileName='e:/Current Workspace/Codebase/hydrotank/src/modbui/build_model.py', 
    serverPort=61358)
#: The model "model" has been created.
#: 0.197999954224
#: (3.18499994277954, ' --- Created')
#: 75.7419998646
#: 84.7239999771
#: 87.0379998684
#: (15.8309998512268, ' --- Cut')
#: (33.3949999809265, ' --- Assembled')
#: 0.0
