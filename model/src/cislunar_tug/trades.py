"""Trade-study sweeps built on the round-trip model.

The power trade-off (power level vs transfer time) extends these functions. Every sweep
returns plain rows (list of dicts) so results can be saved to CSV, plotted,
or compared across runs without depending on this code.
"""

from __future__ import annotations

import math
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
    """Power level vs transfer time table (MDN §6.3; basis of the power trade-off)."""
    spec = SweepSpec("thrust_n", "thrust_n", "N", tuple(thrust_levels_n), "A-17 / trade-offs")
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


# ------------------------------------------------------------------ power trade-off
def units_for_power(power_w: float, unit_power_w: float) -> int:
    """Thruster units firing at once: the nearest whole number to ``P / unit power``, at least one.

    Halves round up, so the units run as close as possible to their nominal power
    (2.5 units -> 3 at 83 %, not 2 at 125 %). Python's ``round`` rounds halves to the
    even number, which would give 2.5 -> 2 but 3.5 -> 4.
    """
    return max(1, math.floor(power_w / unit_power_w + 0.5))


@dataclass(frozen=True)
class ThrusterUnit:
    """A thruster class used to count units and check wear in the power trade.

    Args:
        name: Short label used in column names (e.g. ``"12kw"``).
        power_w: Nominal input power of one unit [W].
        isp_s: Specific impulse of one unit [s].
        efficiency: Total efficiency of one unit [-].
        rated_life_h: Rated operating life [hours].
    """

    name: str
    power_w: float
    isp_s: float
    efficiency: float
    rated_life_h: float

    @property
    def throughput_kg(self) -> float:
        """Xenon one unit can process over its rated life: ``mdot * life`` [kg]."""
        from . import physics  # local import keeps the module header unchanged

        thrust = physics.thrust_from_power(self.power_w, self.isp_s, self.efficiency)
        return physics.mass_flow_rate(thrust, self.isp_s) * self.rated_life_h * 3_600.0


def power_trade(
    inputs: MissionInputs,
    power_levels_w: Iterable[float],
    specific_mass_kg_per_w: float,
    reference_power_w: float,
    reference_dry_mass_kg: float,
    units: Sequence[ThrusterUnit],
    launch_capacity_kg: float,
    spare_policy: str = "rotation",
) -> list[Row]:
    """Trade 1: EP power level vs transfer time, throughput, mass and thruster wear.

    Thrust follows from power at fixed Isp and efficiency (``T = 2 eta P / v_e``),
    and dry mass grows linearly with power (:class:`LinearPowerDryMass`, A-23).

    Thruster columns per unit class (A-27, D-20), counted in firing hours:

    * ``operating``: units firing at once, :func:`units_for_power` (nearest whole
      number, halves up), so each runs near its nominal point (``load_pct`` = share
      of nominal power);
    * ``installed``: operating units + 1 spare (N+1);
    * ``hours_per_unit_kh``: firing hours each unit accumulates over the life.
      All operating units fire together, so with a cold spare each one carries
      the full thrusting time; with rotation the N+1 units take turns and each
      carries N/(N+1) of it;
    * ``life_used_pct``: ``hours_per_unit / rated life``. Above 100 % the
      mission needs thruster replacement or a longer-life thruster;
    * ``lifetimes_needed``: rated unit lifetimes the mission consumes,
      ``N * thrusting hours / rated life``, whatever the spare policy.

    All units are assumed to run at the mission Isp and efficiency.
    """
    if spare_policy not in ("rotation", "cold"):
        raise ValueError(f"spare_policy must be 'rotation' or 'cold', not {spare_policy!r}")

    from . import physics
    from .mission import LinearPowerDryMass

    mass_model = LinearPowerDryMass(reference_dry_mass_kg, reference_power_w, specific_mass_kg_per_w)
    rows: list[Row] = []
    for power_w in power_levels_w:
        thrust = physics.thrust_from_power(power_w, inputs.isp_s, inputs.thruster_efficiency)
        trip = simulate_round_trip(inputs.with_changes(thrust_n=thrust, dry_mass_model=mass_model))
        row = _row("power_kw_in", round(power_w / 1_000.0, 2), trip, inputs.design_life_years)
        row.pop("power_kw_in")
        life_xenon_kg = trip.propellant_total_kg * trip.trips_in_life
        tug_launch_kg = trip.dry_mass_kg + trip.propellant_total_kg
        row.update(
            {
                "thrust_n": round(thrust, 3),
                "life_xenon_t": round(life_xenon_kg / 1_000.0, 1),
                "tug_launch_mass_t": round(tug_launch_kg / 1_000.0, 2),
                "thrusting_kh_life": round(
                    trip.trips_in_life
                    * (trip.thrusting_outbound_days + trip.thrusting_return_days)
                    * 24.0
                    / 1_000.0,
                    1,
                ),
                "fits_launcher": "yes"
                if max(tug_launch_kg, trip.launch_mass_per_trip_kg) <= launch_capacity_kg
                else "no",
            }
        )
        thrusting_h = trip.trips_in_life * (trip.thrusting_outbound_days + trip.thrusting_return_days) * 24.0
        for unit in units:
            operating = units_for_power(power_w, unit.power_w)
            share = operating / (operating + 1) if spare_policy == "rotation" else 1.0
            hours_per_unit = thrusting_h * share
            row[f"thrusters_{unit.name}_operating"] = operating
            row[f"thrusters_{unit.name}_installed"] = operating + 1
            row[f"thruster_{unit.name}_load_pct"] = round(100.0 * power_w / (operating * unit.power_w))
            row[f"thruster_{unit.name}_hours_per_unit_kh"] = round(hours_per_unit / 1_000.0, 1)
            row[f"thruster_{unit.name}_life_used_pct"] = round(100.0 * hours_per_unit / unit.rated_life_h)
            row[f"thruster_{unit.name}_lifetimes_needed"] = round(
                operating * thrusting_h / unit.rated_life_h, 1
            )
        rows.append(row)
    return rows


def power_trade_from_parameters(
    params, power_levels_kw: Iterable[float], specific_mass_kg_per_kw: float | None = None
) -> list[Row]:
    """Convenience wrapper: run :func:`power_trade` with the values in the parameter file."""
    inputs = MissionInputs.from_parameters(params)
    reference_power_w = simulate_round_trip(inputs).power_w  # 18 kW baseline point (CALC-03)
    alpha = params.value("ep_specific_mass") if specific_mass_kg_per_kw is None else specific_mass_kg_per_kw
    units = (
        ThrusterUnit(
            "12kw",
            params.value("thruster_unit_power"),
            params.value("thruster_unit_isp"),
            params.value("thruster_unit_efficiency"),
            params.value("thruster_rated_life"),
        ),
        ThrusterUnit(
            "5kw_eu",
            params.value("european_thruster_unit_power"),
            params.value("isp"),
            params.value("thruster_efficiency"),
            params.value("european_thruster_rated_life"),
        ),
    )
    return power_trade(
        inputs,
        [kw * 1_000.0 for kw in power_levels_kw],
        alpha / 1_000.0,
        reference_power_w,
        params.value("dry_mass"),
        units,
        params.value("launcher_gto_capacity"),
        params.trades.get("spare_policy", "rotation"),
    )
