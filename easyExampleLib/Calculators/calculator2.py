__author__ = "github.com/wardsimon"
__version__ = "0.0.1"

import json
import numpy as np

class Calculator2:
    """
    Generic calculator in the style of crysPy
    """

    def __init__(self, amplitude: float = 3.5, period: float = np.pi, x_shift: float = 0, y_shift: float = 0):
        """
        Create a calculator object with m and c
        :param m: gradient
        :type m: float
        :param c: intercept
        :type c: float
        """
        self._data = {
            'A': amplitude,
            'p': period,
            'dx': x_shift,
            'dy': y_shift
        }

    def calculate(self, x_array: np.ndarray) -> np.ndarray:
        """
        For a given x calculate the corresponding y
        :param x_array: array of data points to be calculated
        :type x_array: np.ndarray
        :return: points calculated at `x`
        :rtype: np.ndarray
        """

        y_data = self._data['A'] * np.cos(
            (2 * np.pi / self._data['p']) * (x_array + self._data['dx'])) + self._data['dy']
        return y_data

    def export_data(self) -> str:
        return json.dumps(self._data)

    def import_data(self, input_str: str):
        self._data = json.loads(input_str)