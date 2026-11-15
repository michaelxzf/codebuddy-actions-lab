from decimal import Decimal

import pytest

from unitconv import IncompatibleUnits, UnknownUnit, convert


@pytest.mark.parametrize("v,src,dst,want", [(1, "km", "m", Decimal("1000")), (1, "mi", "km", Decimal("1.6093")), (2, "lb", "kg", Decimal("0.9072")), (1, "gal", "l", Decimal("3.7854"))])
def test_convert(v, src, dst, want):
    assert convert(v, src, dst) == want


def test_unknown_unit():
    with pytest.raises(UnknownUnit):
        convert(1, "parsec", "m")


def test_incompatible():
    with pytest.raises(IncompatibleUnits):
        convert(1, "kg", "m")


def test_to_base():
    from unitconv.core import to_base
    assert to_base(2, "km") == 2000
