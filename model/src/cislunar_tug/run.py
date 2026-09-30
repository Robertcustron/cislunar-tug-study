"""Run the model and save every output with provenance.

A run writes to ``<out_dir>/``:

* ``calculation_log.md|json|csv``  every result with formula, inputs and MDN check
* ``parameters_used.md``           the parameter register of this run
* ``<sweep>.csv``                  one file per trade sweep
* ``run_metadata.json``            timestamp, versions, config hash, git commit
* ``*.png``                        charts, if matplotlib is installed and requested
"""

from __future__ import annotations

import csv
import json
import logging
import platform
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from . import __version__
from .baseline import build_baseline_log
from .mission import MissionInputs
from .parameters import ParameterSet
from .trades import Row, SweepSpec, standard_sweeps, thrust_sweep
from .traceability import CalculationLog

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RunOutput:
    """Everything produced by one run, kept in memory for tests and notebooks."""

    log: CalculationLog
    sweeps: dict[str, tuple[SweepSpec, list[Row]]]
    out_dir: Path


def run(params: ParameterSet, out_dir: str | Path, make_plots: bool = False) -> RunOutput:
    """Compute the baseline and trade sweeps, then save all outputs."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    log = build_baseline_log(params)
    sweeps = standard_sweeps(
        MissionInputs.from_parameters(params), dict(params.trades), params.value("dv_margin")
    )

    log.to_markdown(out / "calculation_log.md")
    log.to_json(out / "calculation_log.json")
    log.to_csv(out / "calculation_log.csv")
    log.parameters_to_markdown(out / "parameters_used.md")
    for name, (spec, rows) in sweeps.items():
        _write_rows(out / f"{name}.csv", rows)
        logger.info("Saved sweep %s (%s over %s %s)", name, spec.field, len(spec.values), spec.unit)

    _write_metadata(out / "run_metadata.json", params, log, sweeps)

    if make_plots:
        from .plots import plot_thrust_sweep  # optional dependency

        if "thrust_sweep" in sweeps:
            spec, table_rows = sweeps["thrust_sweep"]
            low, high = min(spec.values), max(spec.values)
            steps = 200
            dense = thrust_sweep(
                MissionInputs.from_parameters(params),
                [low + (high - low) * i / steps for i in range(steps + 1)],
            )
            plot_thrust_sweep(table_rows, dense, out / "thrust_sweep.png")

    for calc in log.discrepancies():
        logger.warning(
            "%s %s: model %.4g %s vs MDN %.4g (%s)",
            calc.calc_id,
            calc.title,
            calc.value,
            calc.unit,
            calc.mdn_value,
            calc.mdn_ref,
        )
    return RunOutput(log=log, sweeps=sweeps, out_dir=out)


def _write_rows(path: Path, rows: list[Row]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _git_commit() -> str:
    """Current git commit of the working tree, or 'unknown' outside a repo."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )
        dirty = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True, timeout=5
        ).stdout.strip()
        return result.stdout.strip() + ("-dirty" if dirty else "")
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def _write_metadata(path: Path, params: ParameterSet, log: CalculationLog, sweeps: dict) -> None:
    status_counts: dict[str, int] = {}
    for calc in log.calculations:
        status_counts[calc.status.value] = status_counts.get(calc.status.value, 0) + 1
    overridden = [p.name for p in params.parameters.values() if p.ref.endswith("(override)")]
    metadata = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model_version": __version__,
        "git_commit": _git_commit(),
        "python": platform.python_version(),
        "parameter_file": params.source_file,
        "parameter_file_sha256": params.source_sha256,
        "document": params.meta.get("document", ""),
        "overridden_parameters": overridden,
        "calculation_status_counts": status_counts,
        "sweeps": list(sweeps.keys()),
    }
    path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
