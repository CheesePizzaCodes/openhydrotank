"""
Data model for the GUI application
"""
from typing import List
from dataclasses import dataclass

import numpy as np

CoordinateArray = np.ndarray  # Nx2 size


@dataclass
class Curve:
    points: CoordinateArray
    alpha_0: float

    def __post_init__(self):
        ...

