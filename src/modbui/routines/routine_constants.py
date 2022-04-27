'''
This file contains several constants used by the routines in the package
'''

#  ----- Paths -----
LINER_PATH = 'E:/Current Workspace/Codebase/hydrotank/src/modbui/routines/caet_tester3/liner.sat'
ROUTINES_PATH = 'E:\\Current Workspace\\Codebase\\hydrotank\\src\\modbui\\routines'

#  ----- Global Names -----
MODEL = 'model'

LAYUP_PART = 'layup'
LAYUP_INSTANCE = LAYUP_PART + '_instance'  # instance
LINER_PART = 'liner'
LINER_INSTANCE = LINER_PART + '_instance'  # instance

#  -- Sets --
bs = 'set'  # base name for sets
LAYER_SET = bs + '_layer_'

LAYUP_SET = bs + '_' + LAYUP_PART
LINER_SET = bs + '_' + LINER_PART
LAYUP_INTERACTION_SET = bs + '_contact_layup'
LINER_INTERACTION_SET = bs + '_contact_liner'

SYM_BC_SET = bs + '_sym_bc'

LOAD_SET = bs + '_load'

#  ----- Geometry -----

#  -- Position --
ROOT_POINT = (156., 0., 0.)

#  -- Length --
TOL = 0.1

#  -- Angle --
GET_EDGES_BY_ANGLE = 20

#  ----- Materials -----
#  -- Part --
LAYUP_MATERIAL = LAYUP_PART + '_material'

# LAYUP_MATERIAL_PROPS = (
#     139260.0,  # E1
#     5989.0,  # E2
#     5989.0,  # E3
#     0.26,  # Nu12
#     0.26,  # Nu13
#     0.4,  # Nu23
#     2612.0,  # G12
#     2612.0,  # G13
#     2139.0)  #

LAYUP_MATERIAL_PROPS = (139260.0, 5989.0, 5989.0, 0.26, 0.26, 0.4, 2612.0, 2612.0, 2139.0)

LAYUP_SECTION = LAYUP_PART + '_section'

#  -- Liner --
LINER_MATERIAL = LINER_PART + '_material'

LINER_MATERIAL_PROPS = (
    1325.0,  # E
    0.3,)  # Nu

LINER_SECTION = LINER_PART + '_section'
# TODO refactor this shit show
