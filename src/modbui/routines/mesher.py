
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


def main():
    # --------- Layup ---------
    # ----- Element Types -----
    elemType1 = mesh.ElemType(elemCode=CGAX8R, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=CGAX6, elemLibrary=STANDARD)
    prt = mdb.models[rc.MODEL].parts[rc.LAYUP_PART]
    pickedRegions = prt.sets[rc.LAYUP_SET]
    prt.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
    # ----- Mesh Controls -----
    pickedRegions = prt.faces
    prt.setMeshControls(regions=pickedRegions, technique=FREE)
    # ----- Mesh Size -----
    prt.seedPart(size=rc.LAYUP_MESH_SIZE, deviationFactor=0.1, minSizeFactor=0.1)
    # ----- Mesh -----
    prt.generateMesh()


    # --------- Liner ---------
    # ----- Element Types -----
    if rc.LINER_TOGGLE:
        elemType1 = mesh.ElemType(elemCode=CGAX8R, elemLibrary=STANDARD)
        elemType2 = mesh.ElemType(elemCode=CGAX6, elemLibrary=STANDARD)
        prt = mdb.models[rc.MODEL].parts[rc.LINER_PART]
        pickedRegions = prt.sets[rc.LINER_SET]
        prt.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
        # ----- Mesh Controls -----
        pickedRegions = prt.faces
        prt.setMeshControls(regions=pickedRegions, technique=FREE)
        # ----- Mesh Size -----
        prt.seedPart(size=rc.LINER_MESH_SIZE, deviationFactor=0.1, minSizeFactor=0.1)
        # ----- Mesh -----
        prt.generateMesh()

if __name__ == '__main__':
    main()
