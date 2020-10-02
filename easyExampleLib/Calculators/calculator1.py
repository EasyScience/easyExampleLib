__author__ = "github.com/wardsimon"
__version__ = "0.0.1"

import numpy as np


class Sin:
    def __init__(self, amplitude: float = 3.5, period: float = np.pi, x_shift: float = 0, y_shift: float = 0):
        self.amplitude = amplitude
        self.period = period
        self.x_shift = x_shift
        self.y_shift = y_shift

class Instrument:
    def __init__(self, x_offset: float = 0, background: float =0):
        self.x_offset = x_offset
        self.background = background


class Calculator1:
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
        self.sins = []
        self.instrument = None

    def add_sin(self, this_sin: Sin):
        self.sins.append(this_sin)

    def remove_sin(self, this_sin: Sin):
        idx = self.sins.index(this_sin)
        if idx is not None:
            del self.sins[idx]
        else:
            raise AttributeError

    def calculate(self, x_array: np.ndarray) -> np.ndarray:
        """
        For a given x calculate the corresponding y
        :param x_array: array of data points to be calculated
        :type x_array: np.ndarray
        :return: points calculated at `x`
        :rtype: np.ndarray
        """
        y_data = np.zeros(x_array.shape)
        for sin in self.sins:
            y_data += sin.amplitude * np.sin(
                (2 * np.pi / sin.period) * (x_array + sin.x_shift)) + sin.y_shift
        return y_data + self.instrument.background
