"""Round-trip mission model for the reusable electric cargo tug.

Model (all stated in TUG-MDN-001 §5.2 and §6):

* One round trip = outbound leg (GTO-class to NRHO, with cargo) + return leg
  (NRHO to GTO-class, with return cargo) + fixed time at the two ends.
* Each leg needs the same delta-v (A-07), including a margin (A-06).
* The tug leaves the staging orbit carrying the propellant for *both* legs;
  it is refuelled only in Earth orbit (MO-3).
* Constant thrust and Isp, so thrusting time = propellant / mass flow.
  Thrusting is paused for eclipses etc., captured by a duty cycle (A-17).
* Delta-v does not depend on thrust level. This is the main simplification;
  in reality low-thrust delta-v rises slightly with lower thrust-to-weight.

Dry mass is supplied by a :class:`DryMassModel`, so that Step 4 can make it
grow with power without changing this module.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from typing import Protocol

from . import physics
from .constants import DAYS_PER_YEAR, SECONDS_PER_DAY
from .parameters import ParameterSet


# --------------------------------------------------------------- dry mass models
class DryMassModel(Protocol):
    """Returns tug dry mass [kg] for a given electric propulsion power [W]."""

    def __call__(self, power_w: float) -> float: ...


@dataclass(frozen=True)
class ConstantDryMass:
    """Dry mass independent of power (Issue 2 baseline, A-10 placeholder)."""

    dry_mass_kg: float

    def __call__(self, power_w: float) -> float:
        return self.dry_mass_kg


@dataclass(frozen=True)
class LinearPowerDryMass:
    """Dry mass that grows linearly with power above a reference point.

    ``m_dry = m_ref + alpha * (P - P_ref)``, with ``alpha`` the specific mass
    of the power and propulsion chain [kg/W]. Intended for the Step 4 trade;
    ``alpha`` must come from a cited source or a stated assumption.
    """

    reference_dry_mass_kg: float
    reference_power_w: float
    specific_mass_kg_per_w: float

    def __call__(self, power_w: float) -> float:
        dry = self.reference_dry_mass_kg + self.specific_mass_kg_per_w * (power_w - self.reference_power_w)
        if dry <= 0.0:
            raise ValueError(f"Dry mass model returned a non-positive mass ({dry:.1f} kg).")
        return dry


# --------------------------------------------------------------- inputs
@dataclass(frozen=True)
class MissionInputs:
    """Typed view of the parameters the round-trip model needs."""

    cargo_outbound_kg: float
    cargo_return_kg: float
    dv_outbound_m_s: float
    dv_return_m_s: float
    thrust_n: float
    isp_s: float
    thruster_efficiency: float
    duty_cycle: float
    end_time_days: float
    design_life_years: float
    dry_mass_model: DryMassModel

    @classmethod
    def from_parameters(
        cls,
        params: ParameterSet,
        dv_per_leg_base_m_s: float | None = None,
        dry_mass_model: DryMassModel | None = None,
    ) -> MissionInputs:
        """Build inputs from a parameter set.

        Args:
            params: Validated parameters.
            dv_per_leg_base_m_s: Optional delta-v *before* margin; defaults to
                ``dv_per_leg_base``. The margin (A-06) is always applied.
            dry_mass_model: Optional model; defaults to constant ``dry_mass``.
        """
        base = params.value("dv_per_leg_base") if dv_per_leg_base_m_s is None else dv_per_leg_base_m_s
        dv_out = design_dv(base, params.value("dv_margin"))
        return cls(
            cargo_outbound_kg=params.value("cargo_outbound"),
            cargo_return_kg=params.value("cargo_return"),
            dv_outbound_m_s=dv_out,
            dv_return_m_s=dv_out * params.value("return_dv_ratio"),
            thrust_n=params.value("thrust"),
            isp_s=params.value("isp"),
            thruster_efficiency=params.value("thruster_efficiency"),
            duty_cycle=params.value("duty_cycle"),
            end_time_days=params.value("end_time_per_round_trip"),
            design_life_years=params.value("design_life"),
            dry_mass_model=dry_mass_model or ConstantDryMass(params.value("dry_mass")),
        )

    def with_changes(self, **changes: float) -> MissionInputs:
        """Return a copy with some fields changed (used by trade sweeps)."""
        return replace(self, **changes)


def design_dv(base_dv_m_s: float, margin: float) -> float:
    """Design delta-v per leg: ``dv = dv_base * (1 + margin)`` [m/s]."""
    return base_dv_m_s * (1.0 + margin)


# --------------------------------------------------------------- results
@dataclass(frozen=True)
class RoundTripResult:
    """Outputs of one round trip. Masses in kg, times in days unless noted."""

    cargo_outbound_kg: float
    power_w: float
    dry_mass_kg: float
    propellant_return_kg: float
    propellant_outbound_kg: float
    initial_mass_kg: float
    thrusting_outbound_days: float
    thrusting_return_days: float
    transfer_outbound_days: float
    transfer_return_days: float
    round_trip_days: float
    trips_in_life: int

    @property
    def propellant_total_kg(self) -> float:
        return self.propellant_outbound_kg + self.propellant_return_kg

    @property
    def round_trip_years(self) -> float:
        return self.round_trip_days / DAYS_PER_YEAR

    @property
    def launch_mass_per_trip_kg(self) -> float:
        """Mass one launch must bring up per trip: cargo + round-trip propellant (A-09)."""
        return self.cargo_outbound_kg + self.propellant_total_kg


# --------------------------------------------------------------- model
def simulate_round_trip(inputs: MissionInputs) -> RoundTripResult:
    """Compute propellant, durations and trip count for one round trip.

    Mass bookkeeping, working backwards from the end of the return leg:

    1. Return leg final mass   = dry + return cargo
    2. Return propellant       = m_f,ret * (exp(dv_ret / v_e) - 1)
    3. Outbound final mass     = dry + outbound cargo + return propellant
       (the outbound cargo is still on board on arrival at NRHO)
    4. Outbound propellant     = m_f,out * (exp(dv_out / v_e) - 1)
    5. Initial mass            = outbound final mass + outbound propellant
    """
    power_w = physics.jet_power(inputs.thrust_n, inputs.isp_s, inputs.thruster_efficiency)
    dry_kg = inputs.dry_mass_model(power_w)

    final_return_kg = dry_kg + inputs.cargo_return_kg
    prop_return_kg = physics.propellant_for_dv_from_final(final_return_kg, inputs.dv_return_m_s, inputs.isp_s)
    final_outbound_kg = dry_kg + inputs.cargo_outbound_kg + prop_return_kg
    prop_outbound_kg = physics.propellant_for_dv_from_final(
        final_outbound_kg, inputs.dv_outbound_m_s, inputs.isp_s
    )

    thrust_out_days = physics.burn_time(prop_outbound_kg, inputs.thrust_n, inputs.isp_s) / SECONDS_PER_DAY
    thrust_ret_days = physics.burn_time(prop_return_kg, inputs.thrust_n, inputs.isp_s) / SECONDS_PER_DAY
    transfer_out_days = thrust_out_days / inputs.duty_cycle
    transfer_ret_days = thrust_ret_days / inputs.duty_cycle
    round_trip_days = transfer_out_days + transfer_ret_days + inputs.end_time_days

    return RoundTripResult(
        cargo_outbound_kg=inputs.cargo_outbound_kg,
        power_w=power_w,
        dry_mass_kg=dry_kg,
        propellant_return_kg=prop_return_kg,
        propellant_outbound_kg=prop_outbound_kg,
        initial_mass_kg=final_outbound_kg + prop_outbound_kg,
        thrusting_outbound_days=thrust_out_days,
        thrusting_return_days=thrust_ret_days,
        transfer_outbound_days=transfer_out_days,
        transfer_return_days=transfer_ret_days,
        round_trip_days=round_trip_days,
        trips_in_life=trips_in_life(round_trip_days, inputs.design_life_years),
    )


def trips_in_life(round_trip_days: float, design_life_years: float) -> int:
    """Whole round trips that fit in the design life: ``floor(L / t_rt)``.

    Conservative: the last trip is counted only if its return leg also fits,
    and commissioning time after launch is not deducted. A tiny relative
    tolerance stops floating-point noise at an exact fit (e.g. from
    :func:`thrust_for_trips`) from losing a trip.
    """
    ratio = design_life_years * DAYS_PER_YEAR / round_trip_days
    return math.floor(ratio * (1.0 + _FIT_TOLERANCE))


_FIT_TOLERANCE = 1e-9


def max_cargo_per_launch(inputs: MissionInputs, launch_capacity_kg: float) -> float:
    """Largest outbound cargo such that cargo + round-trip propellant fits one launch [kg].

    Implements A-09 (one launch per round trip brings cargo and propellant).
    Solved numerically because propellant depends on cargo.
    """

    def excess(cargo_kg: float) -> float:
        trip = simulate_round_trip(inputs.with_changes(cargo_outbound_kg=cargo_kg))
        return cargo_kg + trip.propellant_total_kg - launch_capacity_kg

    return physics.bisect(excess, 0.0, launch_capacity_kg)


def thrust_for_trips(
    inputs: MissionInputs,
    trips: int,
    within_years: float,
    thrust_bounds_n: tuple[float, float] = (0.05, 20.0),
) -> float:
    """Minimum thrust that achieves ``trips`` round trips within ``within_years`` [N].

    Solves ``round_trip_days(T) = within_years * 365.25 / trips``. Works with
    any dry mass model (e.g. mass growing with power).
    """
    target_days = within_years * DAYS_PER_YEAR / trips
    if target_days <= inputs.end_time_days:
        raise ValueError("Target trip time is shorter than the fixed end time.")

    def gap(thrust_n: float) -> float:
        return simulate_round_trip(inputs.with_changes(thrust_n=thrust_n)).round_trip_days - target_days

    return physics.bisect(gap, *thrust_bounds_n)
