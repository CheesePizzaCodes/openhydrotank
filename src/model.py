"""
Data model for the GUI application
"""
from typing import List, Optional, Tuple
from dataclasses import dataclass

import numpy as np

CoordinatesArray = np.ndarray  # Nx2 size
ValuesArray = np.ndarray  # Nx1 size


@dataclass
class Curve:
    _points: CoordinatesArray
    _alpha_0: Optional[float] = None
    _layer_start_index: Optional[int] = None

    ### Constructors
    def __post_init__(self):
        if (len(s := self.points.shape)) != 2:
            raise ValueError(f"input, must be a Nx2 ndarray. Shape provided is {s}")

    @classmethod
    def from_unpacked_xy(cls, x, y):
        return cls(np.column_stack((x, y)))

    ### Properties
    @property
    def points(self) -> CoordinatesArray:
        return self._points

    @points.setter
    def points(self, value) -> None:
        self._points = value

    @property
    def x(self) -> ValuesArray:
        return self._points[:, 0]

    @property
    def y(self) -> ValuesArray:
        return self._points[:, 1]

    @property  # -> Tuple[Tuple[float, float]]
    def points_in_tuples(self):
        return tuple(zip(self.x, self.y))

    @property
    def layer_start_index(self) -> int:
        return self._layer_start_index

    @layer_start_index.setter
    def layer_start_index(self, value: int) -> None:
        self._layer_start_index = value

    @property
    def winding_angle(self) -> float:
        return self._alpha_0

    @winding_angle.setter
    def winding_angle(self, value) -> None:
        self._alpha_0 = value

    def unpack_xy(self) -> Tuple[ValuesArray, ValuesArray]:
        return self.x, self.y

    def apply_mask(self, logical_mask: ValuesArray):
        self._points = self._points[logical_mask]  # inplace modification

    def get_layer_unpacked_xy(self):
        if self.layer_start_index is not None:
            return self.x[self.layer_start_index:], self.y[self.layer_start_index:]
        return self.unpack_xy()

    def get_layer_points(self):
        if self.layer_start_index is None:
            return self.points
        return self.points[self.layer_start_index:]

    def get_non_layer_points(self):
        if self.layer_start_index is None:
            return self.points
        return self.points[:self.layer_start_index]





@dataclass
class CurvesBunch:
    _curves: List[Curve]

    def get_landmarks(self):
        pass

    @property
    def curves(self) -> List[Curve]: return self._curves

    def add_curve(self, curve: Curve) -> None: self._curves.append(curve)
