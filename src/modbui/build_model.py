#This is the main loop. It calls all the required

#global packages

#my packages

import sys, os

sys.path.append('E:\\Current Workspace\\Codebase\\hydrotank\\src')

sys.path.append('E:\\Current Workspace\\Codebase\\hydrotank\\src\\modbui')

sys.path.append('E:\\Current Workspace\\Codebase\\hydrotank\\src\\modbui\\routines')

#TODO shift routines to lowest level actions eg ger surface cut from list of curves or assign material to set

from routines import create_part, cut_face, assemble_parts, create_sets_surfs, assign_property, trivial

def main():

    create_part.main()

    cut_face.main()

    assemble_parts.main()

    create_sets_surfs.main()

    assign_property.main()

    trivial.main()

if __name__ == '__main__':
    main()