# unitconv

Tiny, dependency-free unit conversion (length, mass, volume) used by our logistics apps.

```python
from unitconv import convert
convert(5, "mi", "km")  # Decimal('8.0467')
```

Dev: `pip install -e ".[dev]" && ruff check . && pytest --cov=unitconv`
