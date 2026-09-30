"""Trade-study sweeps built on the round-trip model.

Step 4 (power level vs transfer time) extends these functions. Every sweep
returns plain rows (list of dicts) so results can be saved to CSV, plotted,
or compared across runs without depending on this code.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from .mission import MissionInputs, RoundTripResult, simulate_round_trip

Row = dict[str, float | int | str]


@dataclass(frozen=True)
class SweepSpec:
    """Describes a one-parameter sweep for provenance in saved outputs."""

    name: str
    field: str
    unit: str
    values: tuple[float, ...]
    ref: str


def _row(label_field: str, label_value: float, trip: RoundTripResult, design_life_years: float) -> Row:
    """Flatten one round-trip result into a report row."""
    cargo_over_life_t = trip.trips_in_life * trip.cargo_outbound_kg / 1_000.0
    return {
        label_field: label_value,
        "power_kw": round(trip.power_w / 1_000.0, 2),
        "dry_mass_t": round(trip.dry_mass_kg / 1_000.0, 3),
        "propellant_per_trip_t": round(trip.propellant_total_kg / 1_000.0, 3),
        "launch_mass_per_trip_t": round(trip.launch_mass_per_trip_kg / 1_000.0, 3),
        "outbound_days": round(trip.transfer_outbound_days, 1),
        "return_days": round(trip.transfer_return_days, 1),
        "round_trip_years": round(trip.round_trip_years, 3),
        "trips_in_life": trip.trips_in_life,
        "cargo_over_life_t": round(cargo_over_life_t, 1),
        "cargo_per_year_t": round(cargo_over_life_t / design_life_years, 3),
    }


def sweep(inputs: MissionInputs, spec: SweepSpec) -> list[Row]:
    """One-at-a-time sweep of a :class:`MissionInputs` field.

    Args:
        inputs: Baseline inputs.
        spec: Which field to vary and over which values.

    Returns:
        One row per value.
    """
    rows = []
    for value in spec.values:
        trip = simulate_round_trip(inputs.with_changes(**{spec.field: value}))
        rows.append(_row(spec.name, value, trip, inputs.design_life_years))
    return rows


def thrust_sweep(inputs: MissionInputs, thrust_levels_n: Iterable[float]) -> list[Row]:
    """Power level vs transfer time table (MDN §6.3; basis of the Step 4 trade)."""
    spec = SweepSpec("thrust_n", "thrust_n", "N", tuple(thrust_levels_n), "A-17 / Step 4")
    return sweep(inputs, spec)


def standard_sweeps(
    inputs: MissionInputs, trades: dict, dv_margin: float
) -> dict[str, tuple[SweepSpec, list[Row]]]:
    """Run the sweeps configured in the ``[trades]`` table of the parameter file."""
    results: dict[str, tuple[SweepSpec, list[Row]]] = {}

    thrusts: Sequence[float] = trades.get("thrust_levels_n", [])
    if thrusts:
        spec = SweepSpec("thrust_n", "thrust_n", "N", tuple(thrusts), "A-17 / MDN §6.3")
        results["thrust_sweep"] = (spec, sweep(inputs, spec))

    cargos: Sequence[float] = trades.get("cargo_outbound_kg", [])
    if cargos:
        spec = SweepSpec("cargo_outbound_kg", "cargo_outbound_kg", "kg", tuple(cargos), "A-01 sensitivity")
        results["cargo_sensitivity"] = (spec, sweep(inputs, spec))

    dvs: Sequence[float] = trades.get("dv_per_leg_base_m_s", [])
    if dvs:
        spec = SweepSpec("dv_per_leg_base_m_s", "dv_outbound_m_s", "m/s", tuple(dvs), "A-06 sensitivity")
        return_ratio = inputs.dv_return_m_s / inputs.dv_outbound_m_s  # A-07
        rows = []
        for base in dvs:
            dv = base * (1.0 + dv_margin)
            trip = simulate_round_trip(
                inputs.with_changes(dv_outbound_m_s=dv, dv_return_m_s=dv * return_ratio)
            )
            rows.append(_row(spec.name, base, trip, inputs.design_life_years))
        results["dv_sensitivity"] = (spec, rows)

    return results
