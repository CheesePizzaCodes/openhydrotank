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
    start_time = time.time()

    # import stubs as stb

    print(time.time() - start_time)

    # --- Create materials and assign sections
    # --Layup
    mdb.models[rc.MODEL].Material(name=rc.LAYUP_MATERIAL)

    mdb.models[rc.MODEL].materials[rc.LAYUP_MATERIAL].Elastic(type=ENGINEERING_CONSTANTS,
                                                              table=(rc.LAYUP_MATERIAL_PROPS,))

    mdb.models[rc.MODEL].HomogeneousSolidSection(name=rc.LAYUP_SECTION,
                                                 material=rc.LAYUP_MATERIAL,
                                                 thickness=None)

    part = mdb.models[rc.MODEL].parts[rc.LAYUP_PART]
    region = part.sets[rc.LAYUP_SET]
    part.SectionAssignment(region=region, sectionName=rc.LAYUP_SECTION, offset=0.0,
                           offsetType=MIDDLE_SURFACE, offsetField='',
                           thicknessAssignment=FROM_SECTION)

    # --Orientations
    mdb.models[rc.MODEL].DiscreteField(name=rc.ORIENTATION, description='',
        location=ELEMENTS, fieldType=ORIENTATION, dataWidth=6, defaultValues=(
        1.0, 0.0, 0.0, 0.0, 1.0, 0.0), data=(
            ('', 6, (1, ), (1.0, 0.0, 0.0,
        0.0, 1.0, 0.0)), ), orientationType=CARTESIAN,
        partLevelOrientation=True)
    prt = mdb.models[rc.MODEL].parts[rc.LAYUP_PART]
    region = prt.sets[rc.LAYUP_SET]
    orientation = None
    mdb.models[rc.MODEL].parts[rc.LAYUP_PART].MaterialOrientation(region=region,
        orientationType=FIELD, axis=AXIS_3, fieldName=rc.ORIENTATION,
        localCsys=None, additionalRotationType=ROTATION_NONE, angle=0.0,
        additionalRotationField='', stackDirection=STACK_3)




    if rc.LINER_TOGGLE:
        # --Liner
        mdb.models[rc.MODEL].Material(name=rc.LINER_MATERIAL) #bn

        mdb.models[rc.MODEL].materials[rc.LINER_MATERIAL].Elastic(table=(rc.LINER_MATERIAL_PROPS,))

        mdb.models[rc.MODEL].HomogeneousSolidSection(name=rc.LINER_SECTION,
                                                     material=rc.LINER_MATERIAL,
                                                     thickness=None)

        part = mdb.models[rc.MODEL].parts[rc.LINER_PART]
        region = part.sets[rc.LINER_SET]
        part.SectionAssignment(region=region, sectionName=rc.LINER_SECTION, offset=0.0,
                               offsetType=MIDDLE_SURFACE, offsetField='',
                               thicknessAssignment=FROM_SECTION)

    # --- end Create materials

if __name__ == '__main__':
    main()
