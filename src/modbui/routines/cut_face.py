
#input: list of lines. Each line is a list of points. Each line defines a cut of the shape

#output: model containing layup cross-section part file

#import abaqus modules
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

#import own modules
import routine_constants as cts



#set work part
p = mdb.models[cts.MODEL_NAME].parts[cts.PART_NAME]
#initialize cutting sketch
f, e, d1 = p.faces, p.edges, p.datums
s1 = mdb.models[cts.MODEL_NAME].ConstrainedSketch(name='__profile__',
                                                  sheetSize=4.47, gridSpacing=0.11)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models[cts.MODEL_NAME].parts[cts.PART_NAME]
p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)

#draw cutting sketch
for line in lines:
    for i, point in enumerate(line):#TODO turn this into a low level utility function
        try:
            s.Line(point1=point, point2=points[i + 1])
        except:
            pass  # TODO refactor exception handling. This may cause problems.


    # s1.Line(point1=(-0.667778, 0.11), point2=(-0.3025, 0.33))
    # s1.Line(point1=(-0.3025, 0.33), point2=(0.1375, 0.4125))
    # s1.Line(point1=(0.1375, 0.4125), point2=(0.777778000052586, 0.4125))
    # debug stub TODO delete later
    #
    # s1.Line(point1=(-0.8525, -0.074722), point2=(-0.33, 0.165))
    # s1.Line(point1=(-0.33, 0.165), point2=(0.165, 0.2475))
    # s1.Line(point1=(0.165, 0.2475), point2=(0.537310928571969, 0.2475))
    # s1.Line(point1=(0.537310928571969, 0.2475), point2=(0.777778000052586, 0.2475))
    # s1.Line(point1=(-1.0725, -0.294722), point2=(-0.495, -0.055))
    # s1.Line(point1=(-0.495, -0.055), point2=(0.165, 0.0825))
    # s1.Line(point1=(0.165, 0.0825), point2=(0.605, 0.0825))
    # s1.Line(point1=(0.605, 0.0825), point2=(0.777778000052586, 0.0825))


#cut part according to sketch
p = mdb.models[cts.MODEL_NAME].parts[cts.PART_NAME]
f = p.faces
pickedFaces = f.getSequenceFromMask(mask=('[#1 ]', ), ) #TODO refactor selection method
e1, d2 = p.edges, p.datums
p.PartitionFaceBySketch(faces=pickedFaces, sketch=s1)
s1.unsetPrimaryObject()
del mdb.models[cts.MODEL_NAME].sketches['__profile__']