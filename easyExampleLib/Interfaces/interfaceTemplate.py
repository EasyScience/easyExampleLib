__author__ = "github.com/wardsimon"
__version__ = "0.0.1"

import numpy as np
from typing import Callable, List
from abc import ABCMeta, abstractmethod

from easyCore import borg
from easyCore.Utils.json import MSONable
from easyCore.Objects.Base import Parameter, BaseObj


class InterfaceTemplate(MSONable, metaclass=ABCMeta):
    """
    This class is a template and defines all properties that an interface should have.
    """
    _interfaces = []
    _borg = borg
    _link = {}

    def __init_subclass__(cls, is_abstract: bool = False, **kwargs):
        """
        Initialise all subclasses so that they can be created in the factory

        :param is_abstract: Is this a subclass which shouldn't be dded
        :type is_abstract: bool
        :param kwargs: key word arguments
        :type kwargs: dict
        :return: None
        :rtype: noneType
        """
        super().__init_subclass__(**kwargs)
        if not is_abstract:
            cls._interfaces.append(cls)

    @abstractmethod
    def get_item_from_namespace(self, obj_id):
        pass

    @abstractmethod
    def create_sample(self, external: bool, *args, **kwargs):
        pass

    @abstractmethod
    def add_sample(self, sample_id):
        pass

    @abstractmethod
    def remove_sample(self, sample_id):
        pass

    @abstractmethod
    def get_value(self, value_label: str, external: bool) -> float:
        """
        Method to get a value from the calculator

        :param value_label: parameter name to get
        :type value_label: str
        :param external: should we lookup a name conversion to internal labeling?
        :type external: bool
        :return: associated value
        :rtype: float
        """
        pass

    @abstractmethod
    def set_value(self, value_label: str, value: float, external: bool):
        """
        Method to set a value from the calculator

        :param value_label: parameter name to set
        :type value_label: str
        :param value: new numeric value
        :type value: float
        :param external: should we lookup a name conversion to internal labeling?
        :type external: bool
        :return: None
        :rtype: noneType
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def fit_func(self, x_array: np.ndarray) -> np.ndarray:
        """
        Function to perform a fit

        :param x_array: points to be calculated at
        :type x_array: np.ndarray
        :return: calculated points
        :rtype: np.ndarray
        """
        pass
