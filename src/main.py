'''
OpenHydroTank: Type IV Hydrogen Pressure Vessel Analysis Tool
Copyright (C) 2023 Simón Cadavid

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''
import subprocess

from src.thickness import main as calculate_layup

if __name__ == "__main__":
    # Calculate curves and transform to the abaqus format of List[Tuple[Tuple[float, float], ... ] ]
    curves = calculate_layup().to_abaqus_format()
    # Transform to string and write it to an intermediate text file
    with open("./resources/intermediate_file.txt", "w") as file:
        file.write(str(curves))
    # Call the build_model script in the abaqus python interpreter by using a PowerShell command
    p = subprocess.Popen(['powershell', 'abaqus cae script=../src/build_model.py'], cwd='./temp')
    p.wait()

