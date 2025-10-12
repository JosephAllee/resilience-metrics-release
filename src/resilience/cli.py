from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from . import __version__ as VERSION
from .core import analyze


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="resiliencectl",
        description="Resilience-Metrics CLI",
        epilog=(
            "Examples:\n"
            "  resiliencectl analyze --csv examples/synth.csv --out examples/analysis.json\n"
            "  resiliencectl analyze --csv examples/synth.csv --stdout --columns value\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {VERSION}")
    sub = parser.add_subparsers(dest="cmd", required=True)

    an = sub.add_parser("analyze", help="Analyze a CSV and generate a JSON report")
    an.add_argument("--csv", required=True, help="Path to CSV (with headers)")
    an.add_argument("--out", help="Output JSON path")
    an.add_argument("--stdout", action="store_true", help="Also print report to stdout")
    an.add_argument("--columns", default=None, help="Comma-separated list of columns to analyze")

    args = parser.parse_args()

    if args.cmd == "analyze":
        path = Path(args.csv)
        if not path.exists():
            print(f"CSV not found: {path}", file=sys.stderr)
            sys.exit(2)
        columns = None
        if args.columns:
            columns = [col.strip() for col in args.columns.split(",") if col.strip()]
            if not columns:
                print("No valid column provided via --columns", file=sys.stderr)
                sys.exit(2)

        if not args.stdout and not args.out:
            print("Specify --out or --stdout (at least one)", file=sys.stderr)
            sys.exit(2)

        try:
            res = analyze(str(path), columns=columns)
        except ValueError as e:
            print(str(e), file=sys.stderr)
            sys.exit(2)
        payload = json.dumps(res, indent=2)

        if args.stdout:
            print(payload)

        if args.out:
            out = Path(args.out)
            out.write_text(payload)
            print(f"OK: report written to {out}")


if __name__ == "__main__":
    main()
