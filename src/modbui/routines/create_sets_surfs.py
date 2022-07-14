'''

 ONLY EXECUTES CREATION OF PREDEFINED SETS IN THE ABAQUS TOOLS
 the sets and surfaces to be used in the model with descriptive names

each layer must be a set TODO done, sorting missing

each part TODO Done :D

each contact face with a descriptive name must be a surface #TODO done

regions with loads #TODO

regions with bc #TODO done :D


TODO convert annoying offset thing to function or something...
'''

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


def main(landmarks):
    start_time = time.time()

    # import stubs as stb

    print(time.time() - start_time)

    sys.path.append('.')

    # set work part
    p = mdb.models[rc.MODEL].parts[rc.LAYUP_PART]
    f = p.faces

    # first remove small faces #TODO this is mainly debug. remove later.
    # for face in f:
    #     if face.getSize() < 1: #delete small faces
    #         p.RemoveFaces(faceList=(face,),
    #                       deleteCells=False)
    # print("flag")

    # ---- create one set per layer
    part = mdb.models[rc.MODEL].parts[rc.LAYUP_PART]
    faces = part.faces

    for index, landmark in enumerate(landmarks):  # this required a workaround using findAt...
        location = ru.offset_point(landmark, 45)
        face_array = part.faces.findAt((location, (0., 0., 1.)))  # find face at location
        name = rc.LAYER_SET + str(index + 1)
        part.Set(faces=(face_array,), name=name)  # TODO layer 1 not included bug. Change angle for 45+90

    # ---- create surf on layup for contact with liner
    part = mdb.models[rc.MODEL].parts[rc.LAYUP_PART]
    landmark = landmarks[0]  # TODO debug loading set here
    location = ru.offset_point(landmark, 90)  # find location of edge above point
    edge = part.edges.findAt(location)
    selection = edge.getEdgesByEdgeAngle(rc.GET_EDGES_BY_ANGLE)
    part.Surface(side1Edges=selection, name=rc.LAYUP_INTERACTION_SURF)

    # ---- create surf on liner for contact with layup TODO remove, obsolete
    if rc.LINER_TOGGLE:
        part = mdb.models[rc.MODEL].parts[rc.LINER_PART]
        location = ru.offset_point(rc.ROOT_POINT, 90)  # find location of edge above point
        edge = part.edges.findAt(location)
        selection = edge.getEdgesByEdgeAngle(rc.GET_EDGES_BY_ANGLE)
        part.Surface(side1Edges=selection, name=rc.LINER_INTERACTION_SURF)

    # ---- create surf on liner for pressure loading

    if rc.LINER_TOGGLE:
        part = mdb.models[rc.MODEL].parts[rc.LINER_PART]
        location = ru.offset_point(rc.LINER_ROOT_POINT, 90)  # find location of edge above point
        edge = part.edges.findAt(location)
        selection = edge.getEdgesByEdgeAngle(rc.GET_EDGES_BY_ANGLE)
        part_vertices = part.vertices  # extract array of vertex objects

        for index, edge in enumerate(selection):  # loop through all selected edge objects in the selection edgeArray object
            edge_vert_indices = edge.getVertices()  # extract verts indices of the current edge

            if(
                    part_vertices[edge_vert_indices[0]].pointOn[0][1] >= rc.PRESSURE_END_POINT
                    and
                    part_vertices[edge_vert_indices[1]].pointOn[0][1] >= rc.PRESSURE_END_POINT
            ):
                pass
        part.Surface(side1Edges=selection, name=rc.LOAD_SURF)  # TODO removeedges above a certain location

    # ---- create set for symmetry BC
    a1 = mdb.models[rc.MODEL].rootAssembly
    landmark = landmarks[0]
    location = ru.offset_point(landmark, 0)  # to the right
    edge = a1.instances[rc.LAYUP_INSTANCE].edges.findAt(location)
    selection_1 = edge.getEdgesByEdgeAngle(rc.GET_EDGES_BY_ANGLE)
    # TODO DANGER CSYST DEFINITION IS CONFUSING! EVALUATE WHEN IT HAS EFFECT! MODELLING / SELECTING GEOMETRY INSIDE ASSEMBLY
    # seemingly, the assembly modelling environment respects the part modelling csyst despite adding a different csyst...

    if rc.LINER_TOGGLE:
        location = ru.offset_point(rc.ROOT_POINT, 180)
        edge = a1.instances[rc.LINER_INSTANCE].edges.findAt(location)
        selection_2 = edge.getEdgesByEdgeAngle(rc.GET_EDGES_BY_ANGLE)
        a1.Set(edges=selection_1 + selection_2, name=rc.SYM_BC_SET)  # TODO this naming may cause conflicts.
    else:
        a1.Set(edges=selection_1, name=rc.SYM_BC_SET)


if __name__ == '__main__':
    main()
