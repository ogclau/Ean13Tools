# ean13-tools

> EAN-13 barcode generation, validation, ASCII rendering, and SVG/PNG export.  
> Modular · Zero dependencies (PNG optional) · CLI included · pip installable.

---

## Installation

```bash
pip install ean13-tools          # core (no extra deps)
pip install ean13-tools[image]   # + PNG rendering via Pillow
```

---

## Quick start

```python
from ean13_tools import generate_ean13, validate_ean13, render_ascii, render_svg

# Generate a complete EAN-13 from the first 12 digits
code = generate_ean13("590123412345")   # → '5901234123457'

# Validate any EAN-13
validate_ean13(code)                    # → True
validate_ean13("5901234123450")         # → False

# ASCII barcode (great for terminals and READMEs)
print(render_ascii(code))

# SVG file
render_svg(code, path="barcode.svg")

# PNG file (requires Pillow)
from ean13_tools import render_png
render_png(code, path="barcode.png")
```

---

## CLI

```bash
ean13 generate 590123412345       # print 5901234123457
ean13 validate 5901234123457      # ✓ valid (exit 0)
ean13 validate 5901234123450      # ✗ INVALID (exit 1)
ean13 ascii   5901234123457       # ASCII barcode in terminal
ean13 svg     5901234123457 out.svg
ean13 png     5901234123457 out.png
ean13 ascii   5901234123457 --height 12
```

---

## API reference

### `generate_ean13(prefix_12_digits: str) -> str`
Calculates the check digit and returns the full 13-digit EAN-13.  
Raises `InvalidPrefixLengthError` or `InvalidCharactersError` on bad input.

### `validate_ean13(code: str, raise_on_error: bool = False) -> bool`
Returns `True` for a valid code. Pass `raise_on_error=True` to get a
descriptive exception (`InvalidLengthError`, `InvalidCheckDigitError`, etc.).

### `render_ascii(code: str, height: int = 8) -> str`
Multi-line ASCII barcode. Follows the ISO/IEC 15420 L/G/R encoding tables.

### `render_svg(code: str, path: str = None, scale: int = 2) -> str`
Returns SVG markup and optionally saves to disk. No extra dependencies.

### `render_png(code: str, path: str, scale: int = 2)`
Saves a PNG file. Requires `pip install Pillow`.

---

## Exceptions

| Exception | When |
|---|---|
| `EAN13Error` | Base class |
| `InvalidPrefixLengthError` | Prefix ≠ 12 digits |
| `InvalidLengthError` | Code ≠ 13 digits |
| `InvalidCharactersError` | Non-digit characters |
| `InvalidCheckDigitError` | Wrong check digit |

---

## Architecture

```
ean13_tools/
├── __init__.py          # Public API
├── generator.py         # Check digit calculation + generation
├── validator.py         # Full EAN-13 validation
├── ascii_renderer.py    # ISO/IEC 15420 ASCII barcode
├── image_renderer.py    # SVG (built-in) + PNG (Pillow)
├── cli.py               # argparse CLI entry point
└── exceptions.py        # Custom exception hierarchy
```

---

## Publishing to PyPI

```bash
python -m build
python -m twine upload dist/*
# Then: pip install ean13-tools
```
