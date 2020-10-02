__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

from typing import Union, List

import numpy as np

from easyCore.Utils.json import MontyDecoder
from easyCore.Objects.Base import Descriptor, Parameter, BaseObj
from easyCore.Objects.Groups import BaseCollection
from easyCore.Utils.decorators import memoized
from easyCore.Utils.classTools import addProp
from easyExampleLib.interface import InterfaceFactory

_decoder = MontyDecoder()


class Instrument(BaseObj):
    _name = 'instrument'
    _defaults = [
        {
            '@module':  'easyCore.Objects.Base',
            '@class':   'Parameter',
            '@version': '0.0.1',
            'name':     'zero_point',
            'value':    0.0
        },
        {
            '@module':  'easyCore.Objects.Base',
            '@class':   'Parameter',
            '@version': '0.0.1',
            'name':     'background',
            'value':    0.0
        }
    ]

    def __init__(self, interface_factory: InterfaceFactory = None):
        super().__init__(self.__class__.__name__, *[_decoder.process_decoded(default) for default in self._defaults])
        self.name = self._name
        self.interface = interface_factory
        if self.interface is not None:
            self.user_data['created'] = \
                self.interface().create_instrument(self, **{item['name']: item['value'] for item in self._defaults})
            self.interface.generate_bindings(self,
                                             ifun=self.interface.generate_instrument_binding,
                                             instrument_interface_id=self.user_data['created'])

    def __repr__(self):
        return f'{self.__class__.__name__}: x_shift={self.zero_point}, ' \
               f'y_shift={self.background} '


class Sample(BaseObj):
    _name = 'sample'
    _defaults = [
        {
            '@module':  'easyCore.Objects.Base',
            '@class':   'Parameter',
            '@version': '0.0.1',
            'name':     'amplitude',
            'value':    3.5,
            'min':      0.0
        },
        {
            '@module':  'easyCore.Objects.Base',
            '@class':   'Parameter',
            '@version': '0.0.1',
            'name':     'period',
            'value':    np.pi,
            'min':      0.0
        }
    ]

    def __init__(self, name=None, interface_factory: InterfaceFactory = None):
        super().__init__(self.__class__.__name__, *[_decoder.process_decoded(default) for default in self._defaults])
        if name is None:
            name = self._name
        self.name = name
        self.interface = interface_factory
        if self.interface is not None:
            self.user_data['created'] = self.interface().create_sample(self, **{item['name']: item['value'] for item in self._defaults})
            self.interface.generate_bindings(self,
                                             ifun=self.interface.generate_sample_binding,
                                             sample_interface_id=self.user_data['created'])

    def __repr__(self):
        return f'{self.__class__.__name__}: amplitude={self.amplitude}, period={self.period}'


class Phases(BaseCollection):
    _name = 'phases'

    def __init__(self, name, *args, interface_factory: InterfaceFactory = None):
        super(Phases, self).__init__(name, *args)
        self.interface = interface_factory

    @classmethod
    def default(cls, interface=None):
        return cls(cls._name, interface_factory=interface)

    @property
    def sample_labels(self) -> List[str]:
        return [sample.name for sample in self]

    def __getitem__(self, i: Union[int, slice]) -> Union[Parameter, Descriptor, BaseObj, 'BaseCollection']:
        if isinstance(i, str) and i in self.sample_labels:
            i = self.sample_labels.index(i)
        return super(Phases, self).__getitem__(i)

    def append(self, item: Sample):
        super(Phases, self).append(item)
        if self.interface is not None:
            self.interface().add_sample(item.user_data['created'])


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


class Model(BaseObj):
    _name = 'Model'

    def __init__(self, interface_factory: InterfaceFactory = None):
        super().__init__(self.__class__.__name__,
                         phases=Phases.default(interface=interface_factory),
                         instrument=Instrument(interface_factory))
        self.name = self._name
        self.interface = interface_factory

    def add_sample(self, sample: Sample):
        self.phases.append(sample)

    def remove_sample(self, index: Union[str, slice]):
        del self.phases[index]

    def __repr__(self):
        return f'{self.__class__.__name__}\nSamples:\n\t' + \
               '\n\t'.join([f'{sample.name}: amplitude={sample.amplitude}, period={sample.period}' for sample in
                          self.phases]) + '\n' + \
               f'Background: x_shift={self.instrument.zero_point}, y_shift={self.instrument.background}'
