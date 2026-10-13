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
from .assessment import add_assessment_calculations, campaign_rows, life_strategy_rows, load_mass_budget
from .baseline import build_baseline_log
from .budgets import add_budget_calculations, load_power_budget
from .mission import MissionInputs
from .parameters import ParameterSet
from .refuelling import load_scoring, score_rows, sensitivity_rows
from .traceability import CalculationLog
from .trades import Row, SweepSpec, power_trade_from_parameters, standard_sweeps

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RunOutput:
    """Everything produced by one run, kept in memory for tests and notebooks."""

    log: CalculationLog
    sweeps: dict[str, tuple[SweepSpec, list[Row]]]
    out_dir: Path
    plots: list[Path]


def run(params: ParameterSet, out_dir: str | Path, make_plots: bool = False) -> RunOutput:
    """Compute the baseline and trade sweeps, then save all outputs."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    # Read the git state before writing anything: rewriting committed result files
    # would otherwise mark every rerun of the reference results as "-dirty".
    commit = _git_commit()

    log = build_baseline_log(params)
    _power_budget(params, log, out)
    _assessment(params, log, out)
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

    power_rows, _ = _power_trade(params, out)
    _refuelling_trade(params, out)

    _write_metadata(out / "run_metadata.json", params, log, sweeps, commit)

    plots: list[Path] = []
    if make_plots:
        plots = _make_plots(params, out, sweeps, power_rows)

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
    return RunOutput(log=log, sweeps=sweeps, out_dir=out, plots=plots)


def _make_plots(
    params: ParameterSet,
    out: Path,
    sweeps: dict[str, tuple[SweepSpec, list[Row]]],
    power_rows: list[Row],
) -> list[Path]:
    """Save the charts; skip them with a warning if matplotlib is missing."""
    try:
        from .plots import plot_power_trade  # optional dependency
    except ImportError:
        logger.warning('matplotlib not installed: charts skipped (pip install -e ".[plot]")')
        return []

    overridden = [p for p in params.parameters.values() if p.ref.endswith("(override)")]
    note = ", ".join(f"{p.name} = {p.value:g} {p.unit} (override)" for p in overridden)
    written: list[Path] = []
    if power_rows:
        levels = [float(r["power_kw"]) for r in power_rows]
        low, high = min(levels), max(levels)
        dense_power = power_trade_from_parameters(params, [low + (high - low) * i / 300 for i in range(301)])
        path = out / "power_trade.png"
        plot_power_trade(power_rows, dense_power, path, note)
        written.append(path)
    return written


def _power_budget(params: ParameterSet, log: CalculationLog, out: Path):
    """Logical architecture: power budget per mode and the sizing calculations, if the file exists."""
    path = _companion_file(params, "power_budget.toml")
    if not path.exists():
        logger.info("No power budget file at %s; logical architecture budgets skipped.", path)
        return None
    budget = load_power_budget(path)
    add_budget_calculations(log, budget)
    _write_rows(out / "power_budget.csv", budget.rows(params.value("power_margin")))
    return budget


def _assessment(params: ParameterSet, log: CalculationLog, out: Path):
    """TRL and cost assessment: mass budget, thruster life strategies, launch campaign, if the file exists."""
    path = _companion_file(params, "mass_budget.toml")
    if not path.exists():
        logger.info("No mass budget file at %s; TRL and cost assessment skipped.", path)
        return None
    budget = load_mass_budget(path)
    add_assessment_calculations(log, budget)
    _write_rows(out / "mass_budget.csv", budget.rows(params.value("mass_system_margin")))
    _write_rows(out / "mass_budget_items.csv", budget.item_rows())
    _write_rows(out / "thruster_life_strategies.csv", life_strategy_rows(params, budget))
    _write_rows(out / "launch_campaign.csv", campaign_rows(params))
    return budget


def _power_trade(params: ParameterSet, out: Path) -> tuple[list[Row], list[Row]]:
    """Trade 1: power level vs transfer time, plus specific-mass sensitivity."""
    levels = params.trades.get("power_levels_kw", [])
    if not levels:
        return [], []
    rows = power_trade_from_parameters(params, levels)
    _write_rows(out / "power_trade.csv", rows)
    sens: list[Row] = []
    for alpha in params.trades.get("ep_specific_mass_kg_per_kw", []):
        for row in power_trade_from_parameters(params, levels, alpha):
            sens.append({"ep_specific_mass_kg_per_kw": alpha, **row})
    _write_rows(out / "power_trade_sensitivity.csv", sens)
    return rows, sens


def _refuelling_trade(params: ParameterSet, out: Path):
    """Trade 2: refuelling concept scoring, if the scoring file exists."""
    path = _companion_file(params, "refuelling_trade.toml")
    if not path.exists():
        logger.info("No refuelling scoring file at %s; Trade 2 skipped.", path)
        return None
    table = load_scoring(path)
    _write_rows(out / "refuelling_trade_scores.csv", score_rows(table))
    _write_rows(out / "refuelling_trade_sensitivity.csv", sensitivity_rows(table))
    return table


def _companion_file(params: ParameterSet, name: str) -> Path:
    """A config file that sits next to the parameter file (power budget, mass budget, scoring).

    Uses the absolute path of the parameter file, so the result does not depend on the
    working directory. ``source_file`` is only the relative path shown in outputs.
    """
    return Path(params.source_path or params.source_file).with_name(name)


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


def _write_metadata(
    path: Path, params: ParameterSet, log: CalculationLog, sweeps: dict, git_commit: str
) -> None:
    status_counts: dict[str, int] = {}
    for calc in log.calculations:
        status_counts[calc.status.value] = status_counts.get(calc.status.value, 0) + 1
    overridden = [p.name for p in params.parameters.values() if p.ref.endswith("(override)")]
    metadata = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model_version": __version__,
        "git_commit": git_commit,
        "python": platform.python_version(),
        "parameter_file": params.source_file,
        "parameter_file_sha256": params.source_sha256,
        "document": params.meta.get("document", ""),
        "overridden_parameters": overridden,
        "calculation_status_counts": status_counts,
        "sweeps": list(sweeps.keys()),
    }
    path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
