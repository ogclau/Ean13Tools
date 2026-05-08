<div align="center">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=15&duration=700&pause=100&color=00FF99&center=true&vCenter=true&width=900&lines=%5B+0.001s+%5D+init+ean13.engine...;%5B+0.028s+%5D+loading+iso_iec_15420+tables...;%5B+0.061s+%5D+L.parity+table+%5BOK%5D;%5B+0.089s+%5D+G.parity+table+%5BOK%5D;%5B+0.112s+%5D+R.parity+table+%5BOK%5D;%5B+0.145s+%5D+check.digit+algorithm+ready;%5B+0.178s+%5D+validator+module+online;%5B+0.210s+%5D+ascii.renderer+active;%5B+0.244s+%5D+svg.engine+loaded;%5B+0.277s+%5D+png.engine+standby+(optional);%5B+0.301s+%5D+cli+registered+as+%60ean13%60;%5B+0.335s+%5D+16+tests+%5BPASS%5D;%5B+0.360s+%5D+integrity+check+%5BOK%5D;%5B+0.388s+%5D+ean13-tools+%3A+READY;%3E+BARCODE+ENGINE+ONLINE_)](https://git.io/typing-svg)

# EAN-13 TOOLS · v0.1.0

![Status](https://img.shields.io/badge/STATUS-ACTIVE-F02468?style=for-the-badge&labelColor=0d1117)
![Python](https://img.shields.io/badge/Python-3.9+-ffd700?style=for-the-badge&labelColor=0d1117)
![Tests](https://img.shields.io/badge/Tests-16%20passing-00ff99?style=for-the-badge&labelColor=0d1117)
![License](https://img.shields.io/badge/License-CC_BY--NC--ND_4.0-ff6b6b?style=for-the-badge&labelColor=0d1117)
![PyPI](https://img.shields.io/badge/PyPI-ready-ff00ff?style=for-the-badge&labelColor=0d1117)
![Deps](https://img.shields.io/badge/Dependencies-0_(core)-00cfff?style=for-the-badge&labelColor=0d1117)


**Generation · Validation · ASCII · SVG · PNG · CLI · ISO/IEC 15420**

*Modular, professional and reusable. Zero dependencies in the core.*

</div>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:ff00ff,50:00d4ff,100:00ff88&height=3&section=footer&reversal=true" width="100%"/>

## 📚 INDEX

- [⚡ Tech Stack](#-tech-stack)
- [🗂 Architecture](#-architecture)
- [🎯 Features](#-features)
- [📦 Installation](#-installation)
- [💻 Python API](#-python-api)
- [⌨️ CLI](#️-cli)
- [❗ Exceptions](#️-exceptions)
- [🧪 Tests](#-tests)

---

## ⚡ Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-3776ab?style=flat-square&logo=python&logoColor=white&labelColor=0d1117)
![Pillow](https://img.shields.io/badge/Pillow-optional-11a3d4?style=flat-square&logo=python&logoColor=white&labelColor=0d1117)
![PyPI](https://img.shields.io/badge/pip_installable-yes-success?style=flat-square&logo=pypi&logoColor=white&labelColor=0d1117)
![ISO](https://img.shields.io/badge/Std-ISO%2FIEC_15420-ffd700?style=flat-square&labelColor=0d1117)
![argparse](https://img.shields.io/badge/CLI-argparse-ff6b6b?style=flat-square&labelColor=0d1117)

</div>

| Module | Role | Deps |
|---|---|---|
| `generator.py` | EAN-13 check digit algorithm | — |
| `validator.py` | Full validation (length, chars, check digit) | — |
| `ascii_renderer.py` | ASCII barcode render using L/G/R tables | — |
| `image_renderer.py` | SVG export (built-in) and PNG (Pillow) | Pillow optional |
| `cli.py` | CLI installed as `ean13` command | — |
| `exceptions.py` | Custom descriptive exception hierarchy | — |

---

## 🗂 Architecture

```
ean13-tools/
│
├── ean13_tools/
│   ├── __init__.py          ← Public API of the package
│   ├── generator.py         ← Check digit calculation
│   ├── validator.py         ← ISO/IEC 15420 validation
│   ├── ascii_renderer.py    ← ASCII barcode (L, G, R tables)
│   ├── image_renderer.py    ← SVG built-in · PNG via Pillow
│   ├── cli.py               ← `ean13` terminal command
│   └── exceptions.py        ← Custom exception hierarchy
│
└── tests/
   └── test_ean13.py        ← 16 tests · pytest

```

---

## 🎯 Features

```
✔  Generate valid EAN-13 from a 12-digit prefix
✔  Validate complete EAN-13 (bool mode or raise mode)
✔  ASCII render in terminal using █ blocks
✔  Export to SVG with no external dependencies
✔  Export to PNG via Pillow (optional dependency)
✔  Installable CLI: `ean13` command available globally
✔  Descriptive exceptions with exact error messages
✔  16 automated tests with pytest
```

---

## 📦 Installation

**Core — no external dependencies:**
```bash
pip install ean13-tools
```

**With PNG support (Pillow):**
```bash
pip install "ean13-tools[image]"
```

**Development mode (editable):**
```bash
git clone https://github.com/ogclau/ean13tools
cd ean13-tools
pip install -e .
```

**Verify installation:**
```bash
ean13 --help
```

---

## 💻 Python API

### Generate EAN-13

```python
from ean13_tools import generate_ean13

code = generate_ean13("590123412345")
print(code)  # → 5901234123457
```

### Validate

```python
from ean13_tools import validate_ean13

validate_ean13("5901234123457")          # → True
validate_ean13("5901234123450")          # → False

# Strict mode — raises a descriptive exception
validate_ean13("5901234123450", raise_on_error=True)
# → InvalidCheckDigitError: expected 7, got 0
```

### ASCII in terminal

```python
from ean13_tools import render_ascii

print(render_ascii("5901234123457"))
# █ █   █ ██ █  ███ ██  ██  █  ██ ████ ...
# 5   9  0  1  2  3  4    1  2  3  4  5  7
```

### Export SVG

```python
from ean13_tools import render_svg

# As string
svg_str = render_svg("5901234123457")

# As file
render_svg("5901234123457", path="barcode.svg")
```

### Export PNG *(requires Pillow)*

```python
from ean13_tools import render_png

render_png("5901234123457", path="barcode.png")
render_png("5901234123457", path="barcode@2x.png", scale=4)
```

---

## ⌨️ CLI

Once installed, the `ean13` command is available in any terminal:

```bash
# Generate EAN-13 from a 12-digit prefix
ean13 generate 590123412345
# → 5901234123457

# Validate (exit 0 = valid · exit 1 = invalid)
ean13 validate 5901234123457   # ✓  5901234123457  →  valid
ean13 validate 5901234123450   # ✗  5901234123450  →  INVALID

# ASCII barcode in terminal
ean13 ascii 5901234123457
ean13 ascii 5901234123457 --height 12

# Export SVG
ean13 svg 5901234123457 output.svg

# Export PNG
ean13 png 5901234123457 output.png
```

> The CLI returns **exit code 1** when a code is invalid, making it scriptable:
> ```bash
> if ean13 validate "$CODE"; then echo "OK"; else echo "Invalid code"; fi
> ```

---

## ⚠️ Exceptions

All exceptions inherit from `EAN13Error` — catch them broadly or individually:

```python
from ean13_tools import EAN13Error, InvalidCheckDigitError

try:
    validate_ean13("1234567890000", raise_on_error=True)
except InvalidCheckDigitError as e:
    print(e)   # Invalid check digit: expected 5, got 0
except EAN13Error as e:
    print(e)   # any other package error
```

| Exception | When raised |
|---|---|
| `EAN13Error` | Base class — catches all package errors |
| `InvalidPrefixLengthError` | Prefix is not exactly 12 digits |
| `InvalidLengthError` | Code is not exactly 13 digits |
| `InvalidCharactersError` | Contains non-numeric characters |
| `InvalidCheckDigitError` | Check digit is incorrect |

---

## 🧪 Tests

```bash
pip install pytest
pytest tests/ -v

# 16 passed in 0.04s ✓
```

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:ff00ff,50:00d4ff,100:00ff88&height=3&section=footer&reversal=true" width="100%"/>

*Built with pure Python · ISO/IEC 15420 · Designed to be reused*

![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f?style=flat-square&logo=python&labelColor=0d1117)
![EAN-13](https://img.shields.io/badge/Standard-ISO%2FIEC_15420-00ff99?style=flat-square&labelColor=0d1117)

</div>
