"""
ascii_renderer.py — Renders EAN-13 codes as ASCII art barcodes.

EAN-13 encoding tables follow the ISO/IEC 15420 standard.
"""

from .validator import validate_ean13
from .exceptions import InvalidLengthError, InvalidCharactersError

# L-code (left odd parity), G-code (left even parity), R-code (right)
_L = ["0001101","0011001","0010011","0111101","0100011",
      "0110001","0101111","0111011","0110111","0001011"]
_G = ["0100111","0110011","0011011","0100001","0011101",
      "0111001","0000101","0010001","0001001","0010111"]
_R = ["1110010","1100110","1101100","1000010","1011100",
      "1001110","1010000","1000100","1001000","1110100"]

# First digit determines the L/G pattern for digits 2–7
_FIRST_DIGIT_PARITY = [
    "LLLLLL","LLGLGG","LLGGLG","LLGGGL","LGLLGG",
    "LGGLLG","LGGGLL","LGLGLG","LGLGGL","LGGLGL",
]

_GUARD_NORMAL = "101"
_GUARD_CENTER = "01010"
_GUARD_END    = "101"


def _encode(code: str) -> str:
    """Return the full binary string for a 13-digit EAN-13."""
    parity = _FIRST_DIGIT_PARITY[int(code[0])]
    bits = _GUARD_NORMAL
    for i, digit in enumerate(code[1:7]):
        table = _L if parity[i] == "L" else _G
        bits += table[int(digit)]
    bits += _GUARD_CENTER
    for digit in code[7:]:
        bits += _R[int(digit)]
    bits += _GUARD_END
    return bits


def render_ascii(code: str, height: int = 8) -> str:
    """
    Render an EAN-13 code as an ASCII barcode string.

    Args:
        code:   A valid 13-digit EAN-13 code.
        height: Number of bar rows (default 8).

    Returns:
        A multi-line string containing the ASCII barcode.

    Raises:
        InvalidLengthError, InvalidCharactersError if the code is malformed.

    Example:
        >>> print(render_ascii('5901234123457'))
        █ ██ █ ██  ██ █ ██ █  ██ █ █ ██  ██ █ ██ █ ...
    """
    validate_ean13(code, raise_on_error=True)
    bits = _encode(code)

    bar_row = "".join("█" if b == "1" else " " for b in bits)
    lines = [bar_row] * height

    # Human-readable digits underneath
    # Spacing: guard(3) + 6×7 digits + center(5) + 6×7 digits + guard(3)
    left_digits  = " " + "  ".join(code[1:7])   # rough centering
    right_digits = " " + "  ".join(code[7:])
    digit_line   = f" {code[0]}  {left_digits}        {right_digits} "

    lines.append(digit_line)
    return "\n".join(lines)
