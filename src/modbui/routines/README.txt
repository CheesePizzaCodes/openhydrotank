This folder contains the abaqus scripts.
The scripts are called at the end of individual modules to materialize the logic of each module int oan abaqus model.
The ulil file contains abaqus miscelaneous helper functions

each routine is responsible for modifying one single attribute of the model

These scripts are only intended to run from the abaqus python interpreter , and as such, must run in python 2.7