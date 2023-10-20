"""
Data model for the GUI application
"""
from typing import List, Optional
from dataclasses import dataclass

import numpy as np

CoordinateArray = np.ndarray  # Nx2 size


@dataclass
class Curve:
    points: CoordinateArray
    alpha_0: Optional[float] = None

    def __post_init__(self):
        ...

    def x(self): return self.points[:, 0]
    def y(self): return self.points[:, 0]


