"""
Main routine
"""

import sys
import os
import subprocess


def main():
    print(os.getcwd())

    subprocess.call([r'src\wrapper.bat'])

    output = 0
    return output


if __name__ == '__main__':
    main()
