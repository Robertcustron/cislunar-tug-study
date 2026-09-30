"""End-to-end test: a run writes all traceability outputs."""

import json

from cislunar_tug.run import run


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
