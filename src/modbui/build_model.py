#This is the main loop. It calls all the required

#global packages

#my packages
from logics import *


def main():

    lg.generate_layup

    lg.process_geometry

    lg.assign_material

    lg.assemble_components

    lg.define_solver

    lg.define_interaction

    lg.define_load

    lg.define_mesh

    pass


if __name__ == '__main__':
    main()