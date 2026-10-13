"""End-to-end test: a run writes all traceability outputs."""

import json
from pathlib import Path

from cislunar_tug.parameters import load_parameters
from cislunar_tug.run import run

CONFIG = Path(__file__).resolve().parents[1] / "config" / "baseline.toml"


def test_run_writes_outputs(params, tmp_path):
    result = run(params.with_overrides(thrust=1.5), tmp_path)
    for name in (
        "calculation_log.md",
        "calculation_log.json",
        "calculation_log.csv",
        "parameters_used.md",
        "run_metadata.json",
        "thrust_sweep.csv",
    ):
        assert (tmp_path / name).exists(), name
    meta = json.loads((tmp_path / "run_metadata.json").read_text())
    assert meta["overridden_parameters"] == ["thrust"]
    assert len(meta["parameter_file_sha256"]) == 64
    # With a different thrust the document values no longer hold, and the log says so.
    assert result.log.discrepancies()


def test_validation_cases_do_not_depend_on_tug_design(params, tmp_path):
    """VAL-xx check published missions, so changing the tug must not move them."""
    base = run(params, tmp_path / "a").log
    variant = run(params.with_overrides(thrust=3.0, isp=2600.0, dv_per_leg_base=3100.0), tmp_path / "b").log
    for calc_id in ("VAL-01", "VAL-02", "VAL-03"):
        assert variant[calc_id].value == base[calc_id].value


def test_cli_saves_chart_by_default(tmp_path, capsys):
    """A variant run from the command line writes the chart without extra flags."""
    import pytest

    pytest.importorskip("matplotlib")
    from cislunar_tug.cli import main

    main(["run", "--set", "ep_specific_mass=40", "--out", str(tmp_path)])
    assert (tmp_path / "power_trade.png").exists()
    assert not (tmp_path / "thrust_sweep.png").exists()
    assert "Charts: power_trade.png" in capsys.readouterr().out


def test_cli_no_plots_skips_charts(tmp_path):
    from cislunar_tug.cli import main

    main(["run", "--no-plots", "--out", str(tmp_path)])
    assert not list(tmp_path.glob("*.png"))


def test_run_from_another_directory_keeps_every_output(tmp_path, monkeypatch):
    """The companion config files are found next to the parameter file, whatever the working directory."""
    monkeypatch.chdir(tmp_path)
    log = run(load_parameters(CONFIG), tmp_path / "out").log
    assert len(log.calculations) == 53
    for name in ("power_budget.csv", "mass_budget.csv", "launch_campaign.csv", "refuelling_trade_scores.csv"):
        assert (tmp_path / "out" / name).exists(), name
