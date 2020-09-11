__author__ = "github.com/wardsimon"
__version__ = "0.0.1"

import numpy as np


class Calculator1:
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
        self.amplitude = amplitude
        self.period = period
        self.x_shift = x_shift
        self.y_shift = y_shift

    def calculate(self, x_array: np.ndarray) -> np.ndarray:
        """
        For a given x calculate the corresponding y
        :param x_array: array of data points to be calculated
        :type x_array: np.ndarray
        :return: points calculated at `x`
        :rtype: np.ndarray
        """

        y_data = self.amplitude * np.sin(
            (2 * np.pi / self.period) * (x_array + self.x_shift)) + self.y_shift
        return y_data
