'''
This file contains several constants used by the routines in the package
'''

#  ----- Design Variables -----
#  ----- Global Names -----
MODEL = 'model'

LAYUP_PART = 'layup'
LAYUP_INSTANCE = LAYUP_PART + '_instance'  # instance
LINER_PART = 'liner'
LINER_INSTANCE = LINER_PART + '_instance'  # instance

STEP = 'Step-1'
LOAD = 'Load-1'
BC = 'BC-1'
BC2 = 'BC-2'

ORIENTATION = 'orientation'

#  -- Sets and surfs --
bset = 'set'  # base name for sets
LAYER_SET = bset + '_layer_'

LAYUP_SET = bset + '_' + LAYUP_PART
LINER_SET = bset + '_' + LINER_PART

SYM_BC_SET = bset + '_sym_bc'

bsur = 'surf_'

LAYUP_INTERACTION_SURF = bsur + 'contact_layup'
LINER_INTERACTION_SURF = bsur + 'contact_liner'

LOAD_SURF = bsur + 'load'

#  ----- Geometry -----
LINER_TOGGLE = False

#  -- Position --
ROOT_POINT = (156., 0., 0.)
LINER_ROOT_POINT = (150., 0., 0.)  # TODO refactor these
PRESSURE_END_POINT = 472
#  -- Lengths --
TOL = 0.1

R_0 = 40  # Polar Opening Radius

#  -- Angle --
GET_EDGES_BY_ANGLE = 20

#  ----- Materials -----
#  -- Part --
LAYUP_MATERIAL = LAYUP_PART + '_material'

LAYUP_MATERIAL_PROPS = (
    139260.0,  # E1
    5989.0,  # E2
    5989.0,  # E3
    0.26,  # Nu12
    0.26,  # Nu13
    0.4,  # Nu23
    2612.0,  # G12
    2612.0,  # G13
    2139.0)  #


LAYUP_SECTION = LAYUP_PART + '_section'

#  -- Liner --
LINER_MATERIAL = LINER_PART + '_material'

LINER_MATERIAL_PROPS = (
    1325.0,  # E
    0.3,)  # Nu

LINER_SECTION = LINER_PART + '_section'
# TODO refactor this shit show

#  ----- Step -----

MAX_NUM_INC = 10000
INITIAL_INC = 0.01
MAX_INC = 0.1

#  ----- Load -----

LOAD_MAG = 75  # MPa  # Magnitude of internal pressure


#  ----- Mesh -----

LAYUP_MESH_SIZE = 1  # mm
