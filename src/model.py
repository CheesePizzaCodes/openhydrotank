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
# Import necessary objects from the typing package
from typing import List, Optional, Tuple
from dataclasses import dataclass

import numpy as np
# Declare the custom type aliases
type Array2D = np.ndarray  # Nx2 size
type Array1D = np.ndarray  # Nx1 size
type Point = Tuple[float, float]
type UnpackedXY = Tuple[Array1D, Array1D]
type AbaqusCurveFormat = Tuple[Point, ...]





@dataclass
class Curve:
    # Private attributes. Will be handled as properties
    _points: Array2D
    _alpha_0: Optional[float] = None
    _layer_start_index: Optional[int] = None

    #  ## Constructors
    def __post_init__(self):
        # Check that the input has the correct shape
        if (len(s := self.points.shape)) != 2:
            raise ValueError(f"input, must be a Nx2 ndarray. Shape provided is {s}")

    @classmethod
    def from_unpacked_xy(cls, x, y):
        # alternative constructor
        return cls(np.column_stack((x, y)))

    #  ## Properties
    @property
    def points(self) -> Array2D:
        return self._points

    @points.setter
    def points(self, value) -> None:
        self._points = value

    @property
    def x(self) -> Array1D:
        return self._points[:, 0]

    @property
    def y(self) -> Array1D:
        return self._points[:, 1]


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


    def get_unpacked_xy(self) -> UnpackedXY:
        return self.x, self.y

    def get_layer_unpacked_xy(self) -> UnpackedXY:
        x, y = self.get_unpacked_xy()
        idx = self.layer_start_index
        if self.layer_start_index is not None:
            return x[idx:], y[idx:]
        return x, y

    def get_layer_points(self) -> Array2D:
        idx = self.layer_start_index
        if idx is None:
            return self.points
        return self.points[idx:]

    def get_non_layer_points(self) -> Array2D:
        idx = self.layer_start_index
        if idx is None:
            return self.points
        return self.points[:idx]
    def to_abaqus_format(self) -> AbaqusCurveFormat:
        return tuple(zip(*self.get_layer_unpacked_xy()))


class CurvesBunch:
    def __init__(self, initial_curve: Curve):
        self._curves: List[Curve] = [initial_curve, ]
    @property
    def curves(self) -> List[Curve]: return self._curves  # readonly

    def add_curve(self, value: Curve) -> None: self._curves.append(value)

    def to_abaqus_format(self) -> List[AbaqusCurveFormat]:
        return [curve.to_abaqus_format() for curve in self.curves]

