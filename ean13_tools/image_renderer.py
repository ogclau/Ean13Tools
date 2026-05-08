"""
image_renderer.py — Generates PNG and SVG barcode images for EAN-13 codes.

PNG rendering requires Pillow: pip install Pillow
SVG rendering has no extra dependencies.
"""

from __future__ import annotations
from pathlib import Path
from .validator import validate_ean13
from .ascii_renderer import _encode

_BAR_WIDTH = 2          # pixels per module
_BAR_HEIGHT = 100       # pixels, barcode bars
_QUIET_ZONE = 14        # modules each side
_FONT_SIZE = 12         # px for digit labels in SVG


def render_svg(code: str, path: str | None = None, scale: int = 2) -> str:
    """
    Render an EAN-13 code as an SVG barcode.

    Args:
        code:  A valid 13-digit EAN-13 code.
        path:  Optional file path to save the SVG. If None, returns the string.
        scale: Module width in pixels (default 2).

    Returns:
        SVG string. Also writes to *path* if provided.
    """
    validate_ean13(code, raise_on_error=True)
    bits = _encode(code)

    module_w = scale
    total_w  = (_QUIET_ZONE * 2 + len(bits)) * module_w
    total_h  = _BAR_HEIGHT + _FONT_SIZE + 12

    rects = []
    x = _QUIET_ZONE * module_w
    for bit in bits:
        if bit == "1":
            rects.append(
                f'<rect x="{x}" y="0" width="{module_w}" height="{_BAR_HEIGHT}" fill="#000"/>'
            )
        x += module_w

    # Digit labels
    left_x  = _QUIET_ZONE * module_w
    center_x = left_x + (3 + 6 * 7) * module_w
    right_x  = center_x + 5 * module_w
    y_text   = _BAR_HEIGHT + _FONT_SIZE

    texts = []
    texts.append(f'<text x="{left_x - 2}" y="{y_text}" text-anchor="end" font-size="{_FONT_SIZE}" font-family="monospace">{code[0]}</text>')
    for i, d in enumerate(code[1:7]):
        tx = left_x + (3 + i * 7 + 3) * module_w
        texts.append(f'<text x="{tx}" y="{y_text}" text-anchor="middle" font-size="{_FONT_SIZE}" font-family="monospace">{d}</text>')
    for i, d in enumerate(code[7:]):
        tx = right_x + (i * 7 + 3) * module_w
        texts.append(f'<text x="{tx}" y="{y_text}" text-anchor="middle" font-size="{_FONT_SIZE}" font-family="monospace">{d}</text>')

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{total_h}" '
        f'viewBox="0 0 {total_w} {total_h}" role="img" aria-label="EAN-13 barcode {code}">'
        f'<rect width="{total_w}" height="{total_h}" fill="#fff"/>'
        + "".join(rects)
        + "".join(texts)
        + "</svg>"
    )

    if path:
        Path(path).write_text(svg, encoding="utf-8")
    return svg


def render_png(code: str, path: str, scale: int = 2) -> None:
    """
    Render an EAN-13 code as a PNG barcode.

    Args:
        code:  A valid 13-digit EAN-13 code.
        path:  File path to save the PNG (e.g. 'barcode.png').
        scale: Module width in pixels (default 2).

    Raises:
        ImportError: If Pillow is not installed.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as e:
        raise ImportError(
            "Pillow is required for PNG rendering. "
            "Install it with: pip install Pillow"
        ) from e

    validate_ean13(code, raise_on_error=True)
    bits = _encode(code)

    module_w = scale
    total_w  = (_QUIET_ZONE * 2 + len(bits)) * module_w
    total_h  = _BAR_HEIGHT + 24

    img  = Image.new("RGB", (total_w, total_h), "white")
    draw = ImageDraw.Draw(img)

    x = _QUIET_ZONE * module_w
    for bit in bits:
        if bit == "1":
            draw.rectangle([x, 0, x + module_w - 1, _BAR_HEIGHT], fill="black")
        x += module_w

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 11)
    except Exception:
        font = ImageFont.load_default()

    left_x  = _QUIET_ZONE * module_w
    center_x = left_x + (3 + 6 * 7) * module_w
    right_x  = center_x + 5 * module_w
    y_text   = _BAR_HEIGHT + 4

    draw.text((left_x - module_w * 2, y_text), code[0], fill="black", font=font)
    for i, d in enumerate(code[1:7]):
        tx = left_x + (3 + i * 7 + 3) * module_w - 3
        draw.text((tx, y_text), d, fill="black", font=font)
    for i, d in enumerate(code[7:]):
        tx = right_x + (i * 7 + 3) * module_w - 3
        draw.text((tx, y_text), d, fill="black", font=font)

    img.save(path)
