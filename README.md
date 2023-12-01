---
# OpenHydroTank: Type IV Hydrogen Pressure Vessel Analysis Tool

## Description
HydroSim is an open-source software tool designed to automate the structural Finite Element (FE) analysis of type IV hydrogen pressure vessels made from carbon-fiber reinforced polymers (CFRP) subjected to internal pressure loading in the commercial FE software Abaqus. For more information about Abaqus, please visit [Abaqus homepage](https://www.3ds.com/products-services/simulia/products/abaqus/). This tool is specifically developed to produce simulation models and results based on desired material properties, angle stacking sequences, and process parameters. It plays a crucial role in analyzing and optimizing the design of type IV hydrogen pressure vessels, ensuring they are light, safe, and reliable for commercial production.

### Key Features 
- Predicts the through-thickness geometry to produce an axisymmetric model
- Computes and assigns the material orientations element-wise
- Simulates the structural response of composite pressure vessels under internal pressure loading.
- Designed for future integration with other software for optimization and machine learning regression tasks.

## Installation
1. Clone the repository from [this link](https://github.com/sai-kalai/openhydrotank).
2. Ensure that you have the required commercial FE software ABAQUS installed and that the command `abaqus cae` is available in your system.
3. Install the required dependencies by running `pip install numpy scipy matplotlib`

## Usage
All commands are to be ran from `/`, the root directory of the cloned repository. First, you need to define the physical problem using input parameters like material properties, vessel dimensions, and internal pressure. These can be specified in `/src/design_variables.py` for the geometry and processing parameters, and in `/src/routines/routine_constants` for the material properties.
There are two use cases:
1. Plotting the predicted geometry
   - Specify the desired liner shape by replacing `/resources/liner.csv`
   - Run `python ./src/thickness.py`
   - There should appear the generated graphs.

When the user is happy with the generated layup, she can proceed to use case 2.
2. Set up a simulation
   - Run `python ./src/main.py`
   - Wait for the model to be setup and ran
   - Analyze the output for optimization and design validation. The odb as well as all simulation files are located in `/temp`

## Support
For support, queries, or contributions, please open an issue on the GitHub repository.

## Contributing
Contributions are welcome! Please open an issue and start a discussion.

## License
HydroSim is licensed under GPLv3, which allows for open-source use and distribution. Please find more information in `LICENSE.md`

## Authors and Acknowledgment
Developed by Simón Cadavid. Special thanks to M.Sc. Weili Jiang and the TUM chair for carbon composites for their guidance and support.

## Project Status
The project is currently in active development, with plans for future enhancements including integration with optimization algorithms and machine learning models.
