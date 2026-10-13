"""Tests for the trade-offs: power level, thruster configuration and refuelling concept."""

from __future__ import annotations

from pathlib import Path

import pytest

from cislunar_tug.mission import MissionInputs
from cislunar_tug.parameters import load_parameters
from cislunar_tug.refuelling import ScoringError, load_scoring, sensitivity_rows
from cislunar_tug.trades import ThrusterUnit, power_trade, power_trade_from_parameters, units_for_power

CONFIG = Path(__file__).resolve().parents[1] / "config"


@pytest.fixture(scope="module")
def params():
    return load_parameters(CONFIG / "baseline.toml")


def test_power_trade_reproduces_baseline_at_18_kw(params):
    """At the reference power the trade must give back the mission definition baseline (CALC-07, CALC-12)."""
    (row,) = power_trade_from_parameters(params, [18.0])
    assert row["dry_mass_t"] == pytest.approx(5.9, abs=0.01)
    assert row["propellant_per_trip_t"] == pytest.approx(2.486, abs=0.002)
    assert row["trips_in_life"] == 7


def test_more_power_never_loses_trips(params):
    rows = power_trade_from_parameters(params, [12, 18, 25, 30, 36, 48])
    trips = [r["trips_in_life"] for r in rows]
    assert trips == sorted(trips)


def test_dry_mass_grows_with_specific_mass(params):
    low = power_trade_from_parameters(params, [48.0], 15.0)[0]
    high = power_trade_from_parameters(params, [48.0], 40.0)[0]
    assert high["dry_mass_t"] > low["dry_mass_t"]
    assert high["dry_mass_t"] == pytest.approx(5.9 + 0.040 * 30.0, abs=0.01)


def test_recommended_point_has_power_margin_for_nine_trips(params):
    """D-16: 25 kW must still give 9 trips with 10 % less power."""
    assert power_trade_from_parameters(params, [25.0 * 0.9])[0]["trips_in_life"] == 9


def test_thruster_wear_does_not_go_away_with_power(params):
    """Trade 1 finding: life used per operating thruster stays far above 100 %."""
    rows = power_trade_from_parameters(params, [12, 25, 48])
    assert all(r["thruster_5kw_eu_life_used_pct"] > 300 for r in rows)


def test_thruster_configurations_d20(params):
    """D-20: 25 kW = 5+1 x 5 kW class at nominal; 24 kW = 2+1 x 12 kW class at nominal; both 9 trips."""
    row24, row25 = power_trade_from_parameters(params, [24.0, 25.0])
    assert row25["thrusters_5kw_eu_operating"] == 5
    assert row25["thrusters_5kw_eu_installed"] == 6
    assert row25["thruster_5kw_eu_load_pct"] == 100
    assert row24["thrusters_12kw_operating"] == 2
    assert row24["thrusters_12kw_installed"] == 3
    assert row24["thruster_12kw_load_pct"] == 100
    assert row24["trips_in_life"] == row25["trips_in_life"] == 9


@pytest.mark.parametrize(
    ("power_kw", "unit_kw", "expected"),
    [(25, 5, 5), (24, 12, 2), (30, 12, 3), (42, 12, 4), (12, 5, 2), (2, 12, 1)],
)
def test_units_for_power_rounds_halves_up(power_kw, unit_kw, expected):
    """Nearest whole number of units, halves up: 2.5 -> 3 and 3.5 -> 4 (not Python's half-to-even)."""
    assert units_for_power(power_kw * 1_000.0, unit_kw * 1_000.0) == expected


def test_thirty_kw_uses_three_twelve_kw_units(params):
    """At 30 kW, 3 x 12 kW units at 83 % are closer to nominal than 2 at 125 %."""
    (row,) = power_trade_from_parameters(params, [30.0])
    assert row["thrusters_12kw_operating"] == 3
    assert row["thruster_12kw_load_pct"] == 83


def test_rotation_spreads_wear_but_not_lifetimes_needed(params):
    """A-27: rotation cuts hours per unit by N/(N+1); the lifetimes the mission consumes do not change."""
    inputs = MissionInputs.from_parameters(params)
    unit = ThrusterUnit("u5", 5_000.0, 2_100.0, 0.6, 15_000.0)
    common = (inputs, [25_000.0], 0.025, 18_019.7, params.value("dry_mass"), [unit], 11_500.0)
    (rot,) = power_trade(*common, spare_policy="rotation")
    (cold,) = power_trade(*common, spare_policy="cold")
    assert rot["thruster_u5_hours_per_unit_kh"] == pytest.approx(
        cold["thruster_u5_hours_per_unit_kh"] * 5 / 6, abs=0.1
    )
    assert rot["thruster_u5_lifetimes_needed"] == cold["thruster_u5_lifetimes_needed"]
    assert rot["thruster_u5_life_used_pct"] > 100  # rotation alone does not close the gap


def test_refuelling_scoring_ranks_r1_first_and_robust():
    table = load_scoring(CONFIG / "refuelling_trade.toml")
    assert table.ranking("baseline")[0] == "R1"
    # R1 is never worse than second in any weight set (ties count as second).
    for row in sensitivity_rows(table):
        totals = {k: v for k, v in row.items() if k.startswith("R")}
        better = [k for k, v in totals.items() if v > totals["R1"] + 1e-9]
        assert len(better) <= 1, row


def test_scoring_rejects_bad_weights(tmp_path):
    text = (
        (CONFIG / "refuelling_trade.toml")
        .read_text(encoding="utf-8")
        .replace("weight = 20", "weight = 25", 1)
    )
    bad = tmp_path / "bad.toml"
    bad.write_text(text, encoding="utf-8")
    with pytest.raises(ScoringError):
        load_scoring(bad)
