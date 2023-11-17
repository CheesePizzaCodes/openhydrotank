import os
import subprocess

from src.thickness import main as calculate_layup

if __name__ == "__main__":
    # cmd = "abaqus"
    # cwd = "./"
    curves = calculate_layup().curves_to_abaqus_format()

    with open("./resources/a.txt", "w") as file:
        file.write(str(curves))

    p = subprocess.Popen(['powershell', 'abaqus cae script=../src/build_model.py'], cwd='./temp')
    p.wait()
