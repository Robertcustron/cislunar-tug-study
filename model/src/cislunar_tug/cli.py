"""Command-line entry point.

Examples::

    python -m cislunar_tug run
    python -m cislunar_tug run --plots
    python -m cislunar_tug run --set thrust=1.5 --out results/thrust-1p5
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from .parameters import ParameterError, load_parameters
from .run import run

DEFAULT_CONFIG = Path(__file__).resolve().parents[2] / "config" / "baseline.toml"
DEFAULT_OUT = Path("results") / "baseline"


def _parse_overrides(pairs: list[str]) -> dict[str, float]:
    overrides: dict[str, float] = {}
    for pair in pairs:
        name, sep, value = pair.partition("=")
        if not sep:
            raise argparse.ArgumentTypeError(f"--set expects name=value, got '{pair}'")
        overrides[name.strip()] = float(value)
    return overrides


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="cislunar_tug", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    run_cmd = sub.add_parser("run", help="Run baseline calculations and trade sweeps")
    run_cmd.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Parameter TOML file")
    run_cmd.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Output directory")
    run_cmd.add_argument(
        "--set",
        action="append",
        default=[],
        metavar="NAME=VALUE",
        help="Override a parameter (repeatable); marked '(override)' in outputs",
    )
    run_cmd.add_argument("--plots", action="store_true", help="Also save charts (needs matplotlib)")
    run_cmd.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING, format="%(levelname)s %(message)s"
    )

    try:
        params = load_parameters(args.config)
        overrides = _parse_overrides(args.set)
        if overrides:
            params = params.with_overrides(**overrides)
    except (ParameterError, argparse.ArgumentTypeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    result = run(params, args.out, make_plots=args.plots)

    counts: dict[str, int] = {}
    for calc in result.log.calculations:
        counts[calc.status.value] = counts.get(calc.status.value, 0) + 1
    print(
        f"{len(result.log.calculations)} calculations: "
        + ", ".join(f"{k} {v}" for k, v in sorted(counts.items()))
    )
    print(f"Outputs written to {result.out_dir}")
    return 1 if result.log.discrepancies() else 0


if __name__ == "__main__":
    raise SystemExit(main())
