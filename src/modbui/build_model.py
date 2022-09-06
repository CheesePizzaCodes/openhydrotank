#This is the main loop. It calls all the required

#global packages

#my packages

import sys, os, time

sys.path.append('E:\\Current Workspace\\Codebase\\hydrotank\\src')

sys.path.append('E:\\Current Workspace\\Codebase\\hydrotank\\src\\modbui')

sys.path.append('E:\\Current Workspace\\Codebase\\hydrotank\\src\\modbui\\routines')

#TODO shift routines to lowest level actions eg ger surface cut from list of curves or assign material to set

from routines import thickness, create_part, cut_face, assemble_parts, create_sets_surfs, assign_property, orient_elements, trivial, mesher

def main():
    lines, landmarks = thickness.main()
    create_part.main()
    cut_face.main(lines)
    assemble_parts.main()
    create_sets_surfs.main(landmarks)
    mesher.main()
    print("checkpoint")
    orient_elements.main(lines)
    assign_property.main()
    trivial.main()
if __name__ == '__main__':

    main()