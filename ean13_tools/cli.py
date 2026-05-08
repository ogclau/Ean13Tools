"""
cli.py — Command-line interface for ean13_tools.

Usage examples:
    ean13 generate 590123412345
    ean13 validate 5901234123457
    ean13 ascii 5901234123457
    ean13 svg 5901234123457 output.svg
    ean13 png 5901234123457 output.png
"""

import argparse
import sys

from .generator import generate_ean13
from .validator import validate_ean13
from .ascii_renderer import render_ascii
from .image_renderer import render_svg, render_png
from .exceptions import EAN13Error


def _cmd_generate(args):
    print(generate_ean13(args.prefix))


def _cmd_validate(args):
    ok = validate_ean13(args.code)
    symbol = "✓" if ok else "✗"
    status = "valid" if ok else "INVALID"
    print(f"{symbol}  {args.code}  →  {status}")
    sys.exit(0 if ok else 1)


def _cmd_ascii(args):
    height = getattr(args, "height", 8)
    print(render_ascii(args.code, height=height))


def _cmd_svg(args):
    render_svg(args.code, path=args.output)
    print(f"SVG saved to {args.output}")


def _cmd_png(args):
    render_png(args.code, path=args.output)
    print(f"PNG saved to {args.output}")


def main():
    parser = argparse.ArgumentParser(
        prog="ean13",
        description="EAN-13 barcode tools — generate, validate, and render.",
    )
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    sub.required = True

    # generate
    p_gen = sub.add_parser("generate", help="Generate EAN-13 from 12-digit prefix")
    p_gen.add_argument("prefix", help="12-digit numeric prefix")
    p_gen.set_defaults(func=_cmd_generate)

    # validate
    p_val = sub.add_parser("validate", help="Validate a 13-digit EAN-13 code")
    p_val.add_argument("code", help="13-digit EAN-13 code")
    p_val.set_defaults(func=_cmd_validate)

    # ascii
    p_asc = sub.add_parser("ascii", help="Render EAN-13 as ASCII barcode")
    p_asc.add_argument("code", help="13-digit EAN-13 code")
    p_asc.add_argument("--height", type=int, default=8, help="Bar height in rows (default 8)")
    p_asc.set_defaults(func=_cmd_ascii)

    # svg
    p_svg = sub.add_parser("svg", help="Render EAN-13 as SVG file")
    p_svg.add_argument("code", help="13-digit EAN-13 code")
    p_svg.add_argument("output", help="Output .svg path")
    p_svg.set_defaults(func=_cmd_svg)

    # png
    p_png = sub.add_parser("png", help="Render EAN-13 as PNG file")
    p_png.add_argument("code", help="13-digit EAN-13 code")
    p_png.add_argument("output", help="Output .png path")
    p_png.set_defaults(func=_cmd_png)

    args = parser.parse_args()
    try:
        args.func(args)
    except EAN13Error as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
