"""
generator.py — Generates valid EAN-13 codes from a 12-digit prefix.
"""

from .exceptions import InvalidPrefixLengthError, InvalidCharactersError


def _calc_check_digit(digits_12: str) -> int:
    """Calculate the EAN-13 check digit from the first 12 digits."""
    total = 0
    for i, ch in enumerate(digits_12):
        weight = 1 if i % 2 == 0 else 3
        total += int(ch) * weight
    return (10 - (total % 10)) % 10


def generate_ean13(prefix_12_digits: str) -> str:
    """
    Generate a valid EAN-13 from a 12-digit prefix.

    Args:
        prefix_12_digits: Exactly 12 numeric characters (e.g. '590123412345').

    Returns:
        A 13-digit EAN-13 string with the correct check digit appended.

    Raises:
        InvalidPrefixLengthError: If the prefix is not exactly 12 digits.
        InvalidCharactersError:   If the prefix contains non-digit characters.

    Example:
        >>> generate_ean13('590123412345')
        '5901234123457'
    """
    if not prefix_12_digits.isdigit():
        raise InvalidCharactersError()
    if len(prefix_12_digits) != 12:
        raise InvalidPrefixLengthError(len(prefix_12_digits))

    check = _calc_check_digit(prefix_12_digits)
    return prefix_12_digits + str(check)
