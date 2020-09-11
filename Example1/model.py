__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

import numpy as np
from easyCore.Objects.Base import Descriptor, Parameter, BaseObj
from easyCore.Utils.decorators import memoized
from Example1.interface import InterfaceFactory
from easyCore.Utils.classTools import addProp


class Sin(BaseObj):
    _defaults = [Parameter('amplitude', 3.5, min=0.0),
                 Parameter('period', np.pi, min=0.0),
                 Parameter('x_shift', 0),
                 Parameter('y_shift', 0)]

    def __init__(self, interface_factory: InterfaceFactory = None):
        self.interface = interface_factory
        super().__init__(self.__class__.__name__, *self._defaults)
        self._set_interface()

    def _set_interface(self):
        if self.interface is not None:
            # If an interface is given, generate bindings
            for parameter in self.get_parameters():
                name = parameter.name
                setattr(parameter, '_callback',
                        property(fget=self.interface().get_item_fn(self.interface(), self.interface()._link[name]),
                                 fset=self.interface().set_item_fn(self.interface(), self.interface()._link[name])))

    def __repr__(self):
        return f'{self.__class__.__name__}: amplitude={self.amplitude}, period={self.period}, x_shift={self.x_shift}, ' \
               f'y_shift={self.y_shift} '


class DummySin(BaseObj):
    def __init__(self):
        _defaults = [Descriptor('amplitude', np.random.uniform(3.0, 4.0)),
                     Descriptor('period', np.random.uniform(np.pi * 0.9, np.pi * 1.1)),
                     Descriptor('x_shift', np.random.uniform(-np.pi * 0.25, np.pi * 0.25)),
                     Descriptor('y_shift', np.random.uniform(-0.5, 0.5))
                     ]
        super(DummySin, self).__init__(self.__class__.__name__, *_defaults)
        self.x_data = np.linspace(0, 10, 100)

    @property
    def y_data(self):
        return self.scatter_generator()

    @property
    def sy_data(self):
        return np.random.normal(1.5, 0.0, self.x_data.shape) * 0.3

    def scatter_generator(self, x_data: np.ndarray = None) -> np.ndarray:
        if x_data is None:
            x_data = self.x_data
        y_data = self.amplitude.raw_value * np.sin(
            (2 * np.pi / self.period.raw_value) * (x_data + self.x_shift.raw_value)) + self.y_shift.raw_value
        y_noise = np.random.normal(0, 0.5, x_data.shape)
        return y_data + y_noise
