"""Tests for the logical architecture budgets (power per mode, battery, array, heat)."""

from __future__ import annotations

from pathlib import Path

import pytest

from cislunar_tug import physics
from cislunar_tug.budgets import BudgetError, add_budget_calculations, design_point_trip, load_power_budget
from cislunar_tug.traceability import CalculationLog

CONFIG = Path(__file__).resolve().parents[1] / "config"


@pytest.fixture(scope="module")
def budget():
    return load_power_budget(CONFIG / "power_budget.toml")


@pytest.fixture(scope="module")
def log(params, budget):
    log = CalculationLog(params)
    add_budget_calculations(log, budget)
    return log


def test_budget_covers_eight_logical_components_and_all_modes(budget):
    assert [c.lc_id for c in budget.components] == [f"LC-{i}" for i in range(1, 9)]
    assert "transfer" in budget.modes and "eclipse" in budget.modes


def test_platform_estimate_with_margin_fits_the_allocation(params, budget):
    """A-21: the 2 kW platform allocation must hold the current estimate plus its margin in every mode."""
    allocation = params.value("platform_power")
    margin = params.value("power_margin")
    for mode in budget.modes:
        assert budget.platform_load(mode) * (1.0 + margin) <= allocation, mode


def test_docking_is_the_worst_platform_mode(budget):
    assert budget.worst_mode() == "docking"


def test_gto_apogee_eclipse_is_about_two_hours():
    """CALC-29: 2 R_E crossed at about 1.6 km/s."""
    assert physics.apoapsis_speed_earth(250.0, 35786.0) == pytest.approx(1602.6, abs=0.5)
    assert physics.max_eclipse_at_apogee_earth(250.0, 35786.0) / 3600.0 == pytest.approx(2.21, abs=0.01)


def test_design_eclipse_covers_the_computed_eclipse(params, log):
    assert params.value("design_eclipse") >= log["CALC-29"].value


def test_ppu_and_thruster_efficiencies_reproduce_a19(log):
    """D-22: 0.95 x 0.63 must give back the 60 % used in every trade (CALC-31 MATCH)."""
    assert log["CALC-31"].status.value == "MATCH"


def test_array_and_battery_sizing(log):
    assert log["CALC-33"].value == pytest.approx(8.77, abs=0.01)  # kWh
    assert log["CALC-35"].value == pytest.approx(29.1, abs=0.1)  # kW EOL
    assert log["CALC-36"].value == pytest.approx(38.9, abs=0.1)  # kW BOL
    assert log["CALC-35"].value > 27.0  # more than the 25 + 2 kW of the trade-offs


def test_ppu_heat_and_xenon_rate(log):
    assert log["CALC-37"].value == pytest.approx(1250.0)
    assert log["CALC-39"].value == pytest.approx(120.8, abs=0.2)
    assert 2550.0 / 21.0 >= log["CALC-39"].value  # IR-02 rate covers the design point


def test_design_point_trip_matches_the_trade(params):
    trip = design_point_trip(params)
    assert trip.trips_in_life == 9
    assert trip.propellant_total_kg == pytest.approx(2537.0, abs=1.0)


def test_budget_file_rejects_a_missing_mode(tmp_path):
    bad = tmp_path / "power_budget.toml"
    bad.write_text(
        '[meta]\nmodes = ["transfer", "safe"]\n'
        '[components.X]\nid = "LC-9"\nname = "X"\nbasis = "b"\nloads = { transfer = 10 }\n',
        encoding="utf-8",
    )
    with pytest.raises(BudgetError):
        load_power_budget(bad)
