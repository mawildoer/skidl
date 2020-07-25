import pytest

from skidl import *

from .setup_teardown import *


def test_alias_1():
    vreg = Part("xess.lib", "1117")
    vreg.match_pin_regex = True
    vreg.set_pin_alias("my_alias", 1)
    vreg.set_pin_alias("my_alias", 2)
    assert len(vreg["my_alias"]) == 2
    assert len(vreg[".*"]) == 4


def test_alias_2():
    vreg = Part("xess.lib", "1117")
    vreg.set_pin_alias("my_alias", 1)
    vreg.set_pin_alias("my_alias", 2)
    with pytest.raises(ValueError):
        vreg.set_pin_alias("new_alias", "my_alias")


def test_alias_3():
    vreg = Part("xess.lib", "1117")
    vreg.match_pin_regex = True
    vreg[1].aliases = "my_alias_+"
    vreg[2].aliases = "my_alias_+"
    vreg[2].aliases += "my_other_alias"
    assert len(vreg["my_alias_+"]) == 2
    assert len((vreg["my_other_alias"],)) == 1
    assert len(vreg[".*"]) == 4
    with pytest.raises(NotImplementedError):
        vreg["my_alias_+"].aliases = "new_alias"
