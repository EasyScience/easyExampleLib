__author__ = "github.com/wardsimon"
__version__ = "0.0.1"

from typing import Callable

from easyCore.Objects.Inferface import InterfaceFactoryTemplate
from easyExampleLib.Interfaces import InterfaceTemplate


class InterfaceFactory(InterfaceFactoryTemplate):
    def __init__(self):
        super(InterfaceFactory, self).__init__(InterfaceTemplate._interfaces)

    def generate_sample_binding(self, name, *args, sample_interface_id=None, **kwargs) -> property:
        """
        Automatically bind a `Parameter` to the corresponding interface.
        :param name: parameter name
        :type name: str
        :return: binding property
        :rtype: property
        """
        return property(fget=self.__get_sample_item(self, sample_interface_id, name, external=True),
                        fset=self.__set_sample_item(self, sample_interface_id, name, external=True))

    def generate_instrument_binding(self, name, *args, instrument_interface_id=None, **kwargs) -> property:
        """
        Automatically bind a `Parameter` to the corresponding interface.
        :param name: parameter name
        :type name: str
        :return: binding property
        :rtype: property
        """
        return property(fget=self.__get_instrument_item(self, instrument_interface_id, name, external=True),
                        fset=self.__set_instrument_item(self, instrument_interface_id, name, external=True))

    def generate_binding(self, name, *args, **kwargs) -> property:
        """
        Automatically bind a `Parameter` to the corresponding interface.
        :param name: parameter name
        :type name: str
        :return: binding property
        :rtype: property
        """
        return property(self.__get_item(self, name, external=True), self.__set_item(self, name, external=True))

    @staticmethod
    def __get_item(obj, key: str, external: bool = True) -> Callable:
        """
        Access the value of a key by a callable object
        :param key: name of parameter to be retrieved
        :type key: str
        :return: function to get key
        :rtype: Callable
        """

        def inner():
            return obj().get_value(key, external)

        return inner

    @staticmethod
    def __set_item(obj, key, external: bool = True) -> Callable:
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
            obj().set_value(key, value, external)

        return inner

    @staticmethod
    def __get_sample_item(obj, sample, key: str, external: bool = True) -> Callable:
        """
        Access the value of a key by a callable object
        :param key: name of parameter to be retrieved
        :type key: str
        :return: function to get key
        :rtype: Callable
        """

        def inner():
            return obj().get_sample_value(sample, key, external)

        return inner

    @staticmethod
    def __set_sample_item(obj, sample, key, external: bool = True) -> Callable:
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
            obj().set_sample_value(sample, key, value, external)
        return inner

    @staticmethod
    def __get_instrument_item(obj, instrument, key: str, external: bool = True) -> Callable:
        """
        Access the value of a key by a callable object
        :param key: name of parameter to be retrieved
        :type key: str
        :return: function to get key
        :rtype: Callable
        """

        def inner():
            return obj().get_instrument_value(instrument, key, external)
        return inner

    @staticmethod
    def __set_instrument_item(obj, instrument, key, external: bool = True) -> Callable:
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
            obj().set_instrument_value(instrument, key, value, external)
        return inner
