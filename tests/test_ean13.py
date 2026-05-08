"""
tests/test_ean13.py — pytest suite for ean13_tools.
"""

import pytest
from ean13_tools import (
    generate_ean13, validate_ean13, render_ascii, render_svg,
    InvalidPrefixLengthError, InvalidCharactersError,
    InvalidCheckDigitError, InvalidLengthError,
)


# ── generator ────────────────────────────────────────────────────────────────

class TestGenerator:
    def test_known_ean(self):
        assert generate_ean13("590123412345") == "5901234123457"

    def test_all_zeros(self):
        result = generate_ean13("000000000000")
        assert result == "0000000000000"
        assert len(result) == 13

    def test_short_prefix_raises(self):
        with pytest.raises(InvalidPrefixLengthError):
            generate_ean13("12345")

    def test_long_prefix_raises(self):
        with pytest.raises(InvalidPrefixLengthError):
            generate_ean13("1234567890123")

    def test_non_digit_raises(self):
        with pytest.raises(InvalidCharactersError):
            generate_ean13("59012341234X")


# ── validator ────────────────────────────────────────────────────────────────

class TestValidator:
    def test_valid_code(self):
        assert validate_ean13("5901234123457") is True

    def test_wrong_check_digit(self):
        assert validate_ean13("5901234123450") is False

    def test_wrong_length(self):
        assert validate_ean13("590123412345") is False

    def test_non_digits(self):
        assert validate_ean13("590123412345X") is False

    def test_raise_on_wrong_check(self):
        with pytest.raises(InvalidCheckDigitError):
            validate_ean13("5901234123450", raise_on_error=True)

    def test_raise_on_length(self):
        with pytest.raises(InvalidLengthError):
            validate_ean13("12345", raise_on_error=True)


# ── ascii renderer ────────────────────────────────────────────────────────────

class TestAsciiRenderer:
    def test_renders_without_error(self):
        output = render_ascii("5901234123457")
        assert isinstance(output, str)
        assert len(output) > 0

    def test_height_parameter(self):
        output = render_ascii("5901234123457", height=5)
        lines = output.split("\n")
        # height rows of bars + 1 digit row = 6
        assert len(lines) == 6

    def test_invalid_code_raises(self):
        with pytest.raises(Exception):
            render_ascii("5901234123450")  # wrong check digit


# ── SVG renderer ─────────────────────────────────────────────────────────────

class TestSvgRenderer:
    def test_svg_string(self):
        svg = render_svg("5901234123457")
        assert svg.startswith("<svg")
        assert "5901234123457" in svg

    def test_svg_writes_file(self, tmp_path):
        out = tmp_path / "test.svg"
        render_svg("5901234123457", path=str(out))
        assert out.exists()
        assert out.read_text().startswith("<svg")
