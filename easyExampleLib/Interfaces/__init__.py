__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

try:
    from easyExampleLib.Interfaces.interface1 import Interface1  # noqa: F401
except ImportError:
    # TODO make this a proper message (use logging?)
    print('interface1 is not installed')

from easyExampleLib.Interfaces.interfaceTemplate import InterfaceTemplate
