#This file must take currently modelled components and locate them in place

'''assembles pieces into correct position'''

#
import sys, os
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

#import python modules
import time

# import own modules
import routine_util as ru
import routine_constants as rc

def main():
    start_time = time.time()

    #  instantiate assembly
    a1 = mdb.models[rc.MODEL].rootAssembly

    #  create coordinate system
    a1.DatumCsysByThreePoints(coordSysType=CYLINDRICAL,
                              origin=(0.0, 0.0, 0.0),
                              point1=(1.0, 0.0, 0.0),
                              point2=(0.0, 0.0, -1.0)
                              )

    p1 = mdb.models[rc.MODEL].parts[rc.LAYUP_PART]
    a1.Instance(name=rc.LAYUP_INSTANCE, part=p1, dependent=ON)
    if rc.LINER_TOGGLE:
        p1 = mdb.models[rc.MODEL].parts[rc.LINER_PART]
        a1.Instance(name=rc.LINER_INSTANCE, part=p1, dependent=ON)

if __name__ == '__main__':
    main()

