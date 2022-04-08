#This is the main loop. It calls all the required

#global packages

#my packages
from logics import assign_material as am




class Model(): #data container. Incrementally stores useful information. only methods are getters and setters...
    #eg store layup, each layer, curves, materials, sets... do not re-do what abq already does, just try to centralize
    #an incremental storage of useful information
    #eg stores elements and locations. gives easy handle to infrrmation from the abaqus world. each routine
    # #returns some value that is then added to Model in the logic script

    def __init__(self):
        pass

    def get_something(self):
        pass



def main():

    m = Model()

    print('this is the build model running')

    pass

    '''
    lg.generate_layup

    lg.process_geometry

    lg.assign_material

    lg.assemble_components

    lg.define_solver

    lg.define_interaction

    lg.define_load

    lg.define_mesh
    
    LG: ORIENT_ELEMENTS
    '''




if __name__ == '__main__':
    main()
    am.main()