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

    start_time = time.time()

    lines, landmarks = thickness.main()
    print(time.time()-start_time, ' --- Thickness calculated')

    create_part.main()
    print(time.time()-start_time, ' --- Created')

    cut_face.main(lines)
    print(time.time() - start_time, ' --- Cut')

    assemble_parts.main()
    print(time.time() - start_time, ' --- Assembled')

    create_sets_surfs.main()
    print(time.time() - start_time, ' --- Sets and Surfaces')

    mesher.main()
    print(time.time() - start_time, ' --- Mesh')

    orient_elements.main()
    print(time.time() - start_time, ' --- Orientation Field')

    assign_property.main()
    print(time.time() - start_time, ' --- Properties')

    trivial.main()
    print(time.time() - start_time, ' --- Step, Load, Interaction')

if __name__ == '__main__':
    main()