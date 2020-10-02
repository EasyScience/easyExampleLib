__author__ = "github.com/wardsimon"
__version__ = "0.0.1"

from typing import Callable, List

import numpy as np
import collections

from easyExampleLib.Interfaces.interfaceTemplate import InterfaceTemplate
from easyExampleLib.Calculators.calculator1 import Calculator1, \
    Sin as CalcSin, \
    Instrument as CalcInstrument


class Interface1(InterfaceTemplate):
    """
    A simple example interface using Calculator1
    """

    _sample_link = {
        'amplitude': 'amplitude',
        'period':    'period',
        'x_shift':   'x_shift',
        'y_shift':   'y_shift'}

    _instrument_link = {
        'zero_point': 'x_offset',
        'background': 'background'
    }

    name = 'sine'

    def __init__(self):
        # This interface will use calculator1
        self.calculator = Calculator1()
        self._namespace = {}

    def get_item_from_namespace(self, obj_id):
        try:
            r = self._namespace.get(obj_id)
        except KeyError:
            r = None
        return r

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
        return getattr(self.calculator, value_label, None)

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
        setattr(self.calculator, value_label, value)

    def create_sample(self, external: bool, *args, **kwargs):

        if external:
            new_kwargs = {}
            for value_label in kwargs.keys():
                if value_label in self._sample_link.keys():
                    new_kwargs[self._sample_link[value_label]] = kwargs[value_label]
        else:
            new_kwargs = kwargs
        obj = CalcSin(*args, **new_kwargs)
        self._namespace[id(obj)] = obj
        return id(obj)

    def add_sample(self, sample_id):
        sample = self.get_item_from_namespace(sample_id)
        self.calculator.add_sin(sample)

    def remove_sample(self, sample_id):
        sample = self.get_item_from_namespace(sample_id)
        idx = self.calculator.sins.index(sample)
        if idx is None:
            raise AttributeError
        del self.calculator.sins[idx]

    def get_sample_value(self, sample_id, value_label: str, external: bool) -> float:
        """
        Method to get a value from the calculator
        :param value_label: parameter name to get
        :type value_label: str
        :return: associated value
        :rtype: float
        """
        sample = self.get_item_from_namespace(sample_id)
        if sample is None:
            raise AttributeError
        if external and value_label in Interface1._sample_link.keys():
            value_label = Interface1._sample_link[value_label]
        return getattr(sample, value_label, None)

    def set_sample_value(self, sample_id, value_label: str, value: float, external: bool):
        """
        Method to set a value from the calculator
        :param value_label: parameter name to get
        :type value_label: str
        :param value: new numeric value
        :type value: float
        :return: None
        :rtype: noneType
        """
        sample = self.get_item_from_namespace(sample_id)
        if sample is None:
            raise AttributeError
        if self._borg.debug:
            print(f'Interface1: Value of {value_label} set to {value}')
        if external and value_label in Interface1._sample_link.keys():
            value_label = Interface1._sample_link[value_label]
        setattr(sample, value_label, value)

    def create_instrument(self, external: bool, *args, **kwargs):

        if external:
            new_kwargs = {}
            for value_label in kwargs.keys():
                if value_label in Interface1._instrument_link.keys():
                    new_kwargs[Interface1._instrument_link[value_label]] = kwargs[value_label]
        else:
            new_kwargs = kwargs
        obj = CalcInstrument(*args, **new_kwargs)
        self._namespace[id(obj)] = obj
        self.calculator.instrument = obj
        return id(obj)

    def get_instrument_value(self, instrumemnt_id, value_label: str, external: bool) -> float:
        """
        Method to get a value from the calculator
        :param value_label: parameter name to get
        :type value_label: str
        :return: associated value
        :rtype: float
        """
        instrument = self.get_item_from_namespace(instrumemnt_id)
        if instrument is None:
            raise AttributeError
        if external and value_label in self._instrument_link.keys():
            value_label = self._instrument_link[value_label]
        return getattr(instrument, value_label, None)

    def set_instrument_value(self, instrumemnt_id, value_label: str, value: float, external: bool):
        """
        Method to set a value from the calculator
        :param value_label: parameter name to get
        :type value_label: str
        :param value: new numeric value
        :type value: float
        :return: None
        :rtype: noneType
        """
        instrument = self.get_item_from_namespace(instrumemnt_id)
        if instrument is None:
            raise AttributeError
        if self._borg.debug:
            print(f'Interface1: Value of {value_label} set to {value}')
        if external and value_label in self._instrument_link.keys():
            value_label = self._instrument_link[value_label]
        setattr(instrument, value_label, value)

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
        for label, value in zip(value_label_list, value_list):
            # This is a simple case so we will serially update
            self.set_value(label, value, external)

    def fit_func(self, x_array: np.ndarray) -> np.ndarray:
        """
        Function to perform a fit
        :param x_array: points to be calculated at
        :type x_array: np.ndarray
        :return: calculated points
        :rtype: np.ndarray
        """
        return self.calculator.calculate(x_array)
