__author__ = "github.com/wardsimon"
__version__ = "0.0.1"

import json
import numpy as np


class Sin:
    def __init__(self, amplitude: float = 3.5, period: float = np.pi, x_shift: float = 0, y_shift: float = 0):
        self.data = {
            'A':  amplitude,
            'p':  period,
            'dx': x_shift,
            'dy': y_shift
        }


class Calculator2:
    """
    Generic calculator in the style of crysPy
    """

    def __init__(self):
        """
        Create a calculator object with m and c
        :param m: gradient
        :type m: float
        :param c: intercept
        :type c: float
        """
        self._data = []

    def add_sin(self, amplitude: float = 3.5, period: float = np.pi, x_shift: float = 0, y_shift: float = 0):
        self._data.append(Sin(amplitude, period, x_shift, y_shift))

    def remove_sin(self, sin):
        del self._data[sin]

    def calculate(self, x_array: np.ndarray) -> np.ndarray:
        """
        For a given x calculate the corresponding y
        :param x_array: array of data points to be calculated
        :type x_array: np.ndarray
        :return: points calculated at `x`
        :rtype: np.ndarray
        """
        y_data = np.zeros(shape=x_array)
        for data in self._data:
            y_data = data['A'] * np.cos(
                (2 * np.pi / data['p']) * (x_array + data['dx'])) + data['dy']
        return y_data

    def export_data(self) -> str:
        return json.dumps(self._data)

    def import_data(self, input_str: str):
        self._data = json.loads(input_str)
