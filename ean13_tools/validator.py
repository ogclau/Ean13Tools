"""
validator.py — Validates complete EAN-13 codes.
"""

from .exceptions import (
    InvalidLengthError,
    InvalidCharactersError,
    InvalidCheckDigitError,
)
from .generator import _calc_check_digit


def validate_ean13(code: str, raise_on_error: bool = False) -> bool:
    """
    Validate a complete 13-digit EAN-13 code.

    Args:
        code:           A string to validate (should be 13 digits).
        raise_on_error: If True, raises a descriptive exception instead of
                        returning False.

    Returns:
        True if the code is a valid EAN-13, False otherwise
        (unless raise_on_error=True).

    Raises:
        InvalidLengthError:     If length != 13 and raise_on_error=True.
        InvalidCharactersError: If non-digit chars found and raise_on_error=True.
        InvalidCheckDigitError: If check digit is wrong and raise_on_error=True.

    Example:
        >>> validate_ean13('5901234123457')
        True
        >>> validate_ean13('5901234123450')
        False
    """
    try:
        if not code.isdigit():
            raise InvalidCharactersError()
        if len(code) != 13:
            raise InvalidLengthError(len(code))
        expected = _calc_check_digit(code[:12])
        if int(code[12]) != expected:
            raise InvalidCheckDigitError(expected, int(code[12]))
        return True
    except Exception:
        if raise_on_error:
            raise
        return False
