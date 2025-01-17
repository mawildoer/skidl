# -*- coding: utf-8 -*-

# The MIT License (MIT) - Copyright (c) 2016-2021 Dave Vandenbout.

"""
Import this file to reconfigure SKiDL for doing SPICE simulations.
"""
from __future__ import (  # isort:skip
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from future import standard_library

from skidl import *

from .tools import SKIDL, SPICE

standard_library.install_aliases()

# PySpice only works with Python 3, so don't set up SPICE simulation for Python 2.
try:
    from PySpice import *
    from PySpice.Unit import *

    from .libs.pyspice_sklib import *
except ImportError:
    pass
else:
    _splib = SchLib("pyspice", tool=SKIDL)  # Read-in the SPICE part library.

    set_default_tool(SPICE)  # Set the library format for reading SKiDL libraries.

    GND = gnd = Net("0")  # Instantiate the default ground net for SPICE.
    gnd.fixed_name = True  # Make sure ground keeps it's name of "0" during net merges.

    # Place all the PySpice parts into the namespace so they can be instantiated easily.
    _this_module = sys.modules[__name__]
    for p in _splib.get_parts():
        # Add the part name to the module namespace.
        setattr(_this_module, p.name, p)
        # Add all the part aliases to the module namespace.
        try:
            for alias in p.aliases:
                setattr(_this_module, alias, p)
        except AttributeError:
            pass
