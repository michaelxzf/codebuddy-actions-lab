"""Integration: carrier rate card in fixtures/rate_card.csv must convert cleanly to metric."""
import csv
from decimal import Decimal
from pathlib import Path

from unitconv import convert

CARD = Path(__file__).parent / "fixtures" / "rate_card.csv"


def test_rate_card_converts_to_metric():
    rows = list(csv.DictReader(CARD.open()))
    total_kg = sum(convert(Decimal(r["weight"]), r["unit"], "kg") for r in rows)
    assert total_kg > 0
