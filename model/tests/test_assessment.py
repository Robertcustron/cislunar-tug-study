"""Tests for the TRL and cost assessment: mass budget, thruster life strategies, launch campaign."""

from __future__ import annotations

from pathlib import Path

import pytest

from cislunar_tug.assessment import (
    MassBudgetError,
    add_assessment_calculations,
    campaign_rows,
    direct_cargo_per_launch,
    life_strategy_rows,
    load_mass_budget,
    max_cargo_for_trips,
    module_plan,
)
from cislunar_tug.traceability import CalculationLog

CONFIG = Path(__file__).resolve().parents[1] / "config"


@pytest.fixture(scope="module")
def budget():
    return load_mass_budget(CONFIG / "mass_budget.toml")


@pytest.fixture(scope="module")
def log(params, budget):
    log = CalculationLog(params)
    add_assessment_calculations(log, budget)
    return log


def test_every_logical_component_has_mass(budget):
    assert {i.lc for i in budget.items} == {f"LC-{i}" for i in range(1, 9)}


def test_esa_margins_are_applied(budget, log):
    """Maturity margins between 5 and 20 % overall, then 20 % system margin (A-35)."""
    ratio = budget.with_maturity_kg() / budget.nominal_kg()
    assert 1.05 < ratio < 1.20
    assert log["CALC-42"].value == pytest.approx(log["CALC-41"].value * 1.2)


def test_bottom_up_is_lighter_than_parametric_and_trips_are_a_floor(log):
    """D-32: the baseline uses the heavier parametric mass, so 9 trips is a floor."""
    assert log["CALC-42"].value < log["CALC-43"].value
    assert log["CALC-44"].value >= 9


def test_module_plan_counts_exchanges():
    assert module_plan(8300.0, 15000.0, 9) == (1, 8)
    assert module_plan(8300.0, 20000.0, 9) == (2, 4)
    assert module_plan(8300.0, 75000.0, 9) == (9, 0)


def test_life_strategies_match_the_trade_offs(params, budget):
    """Lifetimes needed reproduce the trade-offs: 29.9 (5 kW class at 15 kh) and 8.1 (12 kW class, 24 kW)."""
    rows = life_strategy_rows(params, budget)
    five = next(r for r in rows if r["unit_class"].startswith("5 kW") and r["rated_life_kh"] == 15.0)
    twelve = next(r for r in rows if r["unit_class"].startswith("12 kW"))
    assert five["lifetimes_needed"] == pytest.approx(29.9, abs=0.1)
    assert twelve["lifetimes_needed"] == pytest.approx(8.1, abs=0.1)
    assert five["module_exchanges"] == 8


def test_replacement_module_fits_a_resupply_launch(log):
    assert log["CALC-45"].value / 1000.0 < log["CALC-46"].value


def test_direct_launch_beats_the_baseline_tug_per_launch(params):
    """D-09 answered: about 7.1 t per direct launch vs 5 t per tug resupply launch."""
    assert direct_cargo_per_launch(params) == pytest.approx(7113.0, abs=5.0)
    base = campaign_rows(params)[0]
    assert base["cargo_per_trip_t"] == 5.0 and base["extra_launches_with_tug"] == 3


def test_fuller_loads_keep_nine_trips(params):
    """D-30: up to about 7.3 t per trip still gives 9 trips."""
    assert max_cargo_for_trips(params, 9) == pytest.approx(7294.0, abs=5.0)
    seven = next(r for r in campaign_rows(params) if r["cargo_per_trip_t"] == 7.0)
    assert seven["trips_in_life"] == 9 and seven["spare_capacity_t"] > 0


def test_mass_budget_rejects_unknown_category(tmp_path):
    bad = tmp_path / "mass_budget.toml"
    bad.write_text(
        '[categories]\nAB = 0.05\n[[items]]\nlc = "LC-1"\nitem = "x"\nmass = 10\ncategory = "Z"\nbasis = "b"\n',
        encoding="utf-8",
    )
    with pytest.raises(MassBudgetError):
        load_mass_budget(bad)
