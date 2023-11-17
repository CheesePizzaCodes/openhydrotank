# This is the main loop. It calls all the required

# global packages

# my packages


import sys


sys.path.append('../src')


def main():
    from src.routines import create_part, cut_face, assemble_parts, create_sets_surfs, assign_property, orient_elements, trivial, mesher

    with open("../resources/a.txt", "r") as file:
        lines = eval(file.read())

    create_part.main()
    cut_face.main(lines)
    assemble_parts.main()
    create_sets_surfs.main(lines)
    mesher.main()
    orient_elements.main(lines)
    assign_property.main()
    trivial.main()

    print(" -- done -- ")


if __name__ == '__main__':

    main()
