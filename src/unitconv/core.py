from decimal import Decimal

# factor to the base unit of each dimension
UNITS = {
    "length": {"m": Decimal("1"), "km": Decimal("1000"), "cm": Decimal("0.01"), "mi": Decimal("1609.344"), "ft": Decimal("0.3048")},
    "mass": {"kg": Decimal("1"), "g": Decimal("0.001"), "t": Decimal("1000"), "lb": Decimal("0.45359237")},
    "volume": {"l": Decimal("1"), "ml": Decimal("0.001"), "m3": Decimal("1000"), "gal": Decimal("3.785411784")},
}


class UnknownUnit(ValueError):
    pass


class IncompatibleUnits(ValueError):
    pass


def _dimension(unit: str) -> str:
    for dim, table in UNITS.items():
        if unit in table:
            return dim
    raise UnknownUnit(unit)


def convert(value: float | Decimal, src: str, dst: str, places: int = 4) -> Decimal:
    """Convert value from src unit to dst unit, rounded to `places` decimals."""
    d1, d2 = _dimension(src), _dimension(dst)
    if d1 != d2:
        raise IncompatibleUnits(f"{src} ({d1}) -> {dst} ({d2})")
    base = Decimal(str(value)) * UNITS[d1][src]
    return round(base / UNITS[d2][dst], places)


def to_base(value, unit):
    import math
    dim = _dimension(unit)
    return Decimal(str(value)) * UNITS[dim][unit]
