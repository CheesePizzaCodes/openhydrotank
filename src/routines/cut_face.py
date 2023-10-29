"""
This routine cuts the layup

DONE
"""

# input: list of lines. Each line is a list of points. Each line defines a cut of the shape

# output: model containing layup cross-section part file

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

import time

# import own modules
import routine_util as ru
import routine_constants as rc

start_time = time.time()


def main(lines):
    print(time.time() - start_time)

    # set work part
    p = mdb.models[rc.MODEL].parts[rc.LAYUP_PART]
    # initialize cutting sketch
    f, e, d1 = p.faces, p.edges, p.datums
    s1 = mdb.models[rc.MODEL].ConstrainedSketch(name='cutting_sketch',
                                                sheetSize=1000)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models[rc.MODEL].parts[rc.LAYUP_PART]
    p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)

    c = 0
    for line in lines:
        c += 1
        s1.Spline(points=(line[:-1]),
                  constrainPoints=False)  # use points up to second-to-last-point to draw a spline
        ru.draw_line(s1, line[-2:])  # use last two points to go straight below
        print('Partition line {} of {} has been created'.format(c, len(lines)))

    print(time.time() - start_time)

    # cut part according to sketch
    p = mdb.models[rc.MODEL].parts[rc.LAYUP_PART]
    f = p.faces
    pickedFaces = f.getSequenceFromMask(mask=('[#1 ]',), )  # TODO refactor selection method
    e1, d2 = p.edges, p.datums
    p.PartitionFaceBySketch(faces=pickedFaces, sketch=s1)
    s1.unsetPrimaryObject()

    # remove excess material
    f = p.faces
    p.RemoveFaces(faceList=(f.findAt(coordinates=(0.1, 0.1, 0.0)),),
                  deleteCells=False)

    # remove faulty faces

    f = p.faces
    face_list = [face for face in f if face.getSize() < 10]

    try:
        p.RemoveFaces(faceList=face_list, deleteCells=False)
    except:
        print('No faces were removed')


    end_time = time.time()

    total_time = end_time - start_time

    print(total_time)


