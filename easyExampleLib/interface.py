__author__ = "github.com/wardsimon"
__version__ = "0.0.1"

import numpy as np
from typing import Callable, List
from abc import ABCMeta, abstractmethod

from easyCore import borg
from easyCore.Utils.json import MSONable
from easyCore.Objects.Inferface import InterfaceFactoryTemplate
from easyExampleLib.Interfaces import InterfaceTemplate


class InterfaceFactory(InterfaceFactoryTemplate):
    def __init__(self):
        super(InterfaceFactory, self).__init__(InterfaceTemplate._interfaces)

    def generate_bindings(self, name, *args, **kwargs) -> property:
        """
        Automatically bind a `Parameter` to the corresponding interface.
        :param name: parameter name
        :type name: str
        :return: binding property
        :rtype: property
        """
        if name in self.current_interface._link.keys():
            return property(self.__get_item(self.current_interface._link[name]), self.__set_item(self, self.current_interface._link[name]))
        else:
            raise AttributeError

    @staticmethod
    def __get_item(key: str) -> Callable:
        """
        Access the value of a key by a callable object
        :param key: name of parameter to be retrieved
        :type key: str
        :return: function to get key
        :rtype: Callable
        """

        def inner(obj):
            obj().get_value(key)

        return lambda obj: inner(obj)

    @staticmethod
    def __set_item(obj, key):
        """
        Set the value of a key by a callable object
        :param obj: object to be created from
        :type obj: InterfaceFactory
        :param key: name of parameter to be set
        :type key: str
        :return: function to set key
        :rtype: Callable
        """

        def inner(value):
            obj().set_value(key, value)

        return inner
