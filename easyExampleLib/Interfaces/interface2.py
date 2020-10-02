__author__ = "github.com/wardsimon"
__version__ = "0.0.1"

from typing import Callable, List

import numpy as np
import json

from easyExampleLib.Interfaces.interfaceTemplate import InterfaceTemplate
from easyExampleLib.Calculators.calculator2 import Calculator2


class Interface2(InterfaceTemplate):
    """
    A simple example interface using Calculator2
    """
    _link = {'amplitude': 'A',
             'period':    'p',
             'x_shift':   'dx',
             'y_shift':   'dy'}
    name = 'cosine'

    def __init__(self):
        # This interface will use calculator1
        self.calculator = Calculator2()

    def get_value(self, value_label: str, external: bool) -> float:
        """
        Method to get a value from the calculator
        :param value_label: parameter name to get
        :type value_label: str
        :return: associated value
        :rtype: float
        """
        if external and value_label in self._link.keys():
            value_label = self._link[value_label]
        file_read = json.loads(self.calculator.export_data())
        return file_read.get(value_label, None)

    def set_value(self, value_label: str, value: float, external: bool):
        """
        Method to set a value from the calculator
        :param value_label: parameter name to get
        :type value_label: str
        :param value: new numeric value
        :type value: float
        :return: None
        :rtype: noneType
        """
        if self._borg.debug:
            print(f'Interface1: Value of {value_label} set to {value}')
        if external and value_label in self._link.keys():
            value_label = self._link[value_label]
        file_read = json.loads(self.calculator.export_data())
        file_read[value_label] = value
        self.calculator.import_data(json.dumps(file_read))

    def bulk_update(self, value_label_list: List[str], value_list: List[float], external: bool):
        """
        Perform an update of multiple values at once to save time on expensive updates

        :param value_label_list: list of parameters to set
        :type value_label_list: List[str]
        :param value_list: list of new numeric values
        :type value_list: List[float]
        :param external: should we lookup a name conversion to internal labeling?
        :type external: bool
        :return: None
        :rtype: noneType
        """
        # This is a more complex case than interface1
        keys = self._link.keys()
        file_read = json.loads(self.calculator.export_data())

        for label, value in zip(value_label_list, value_list):
            if label in keys:
                if external:
                    file_read[self._link[label]] = value
                else:
                    file_read[label] = value
            else:
                raise AttributeError
        self.calculator.import_data(json.dumps(file_read))

    def fit_func(self, x_array: np.ndarray) -> np.ndarray:
        """
        Function to perform a fit
        :param x_array: points to be calculated at
        :type x_array: np.ndarray
        :return: calculated points
        :rtype: np.ndarray
        """
        return self.calculator.calculate(x_array)
