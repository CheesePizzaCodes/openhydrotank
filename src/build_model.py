# This is the main loop. It calls all the required

# global packages

# my packages

import os
import sys
import time

sys.path.append('./src')
os.chdir('./temp')


def main():
    from src.routines import thickness, create_part, cut_face, assemble_parts, create_sets_surfs, assign_property, \
        orient_elements, trivial, mesher
    st = time.time()

    lines, landmarks = thickness.main()
    print("thickness -- ", time.time() - st)
    create_part.main()
    print("part -- ", time.time() - st)
    cut_face.main(lines)
    print("cut -- ", time.time() - st)
    assemble_parts.main()
    print("assemble -- ", time.time() - st)
    create_sets_surfs.main(landmarks)
    print("sets -- ", time.time() - st)
    mesher.main()
    print("mesh -- ", time.time() - st)
    orient_elements.main(lines)
    print("orientation -- ", time.time() - st)
    assign_property.main()
    print("material -- ", time.time() - st)
    trivial.main()
    print("others -- ", time.time() - st)
    print(" -- done -- ")


if __name__ == '__main__':
    main()
