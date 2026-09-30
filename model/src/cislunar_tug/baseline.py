"""Reproduce every number in TUG-MDN-001 Issue 2 as a traceable calculation.

``build_baseline_log`` is the single place that maps model outputs onto the
document. When the document changes, update the ``mdn_ref``/``mdn_value``
here; when an assumption changes, update the TOML file and rerun.
"""

from __future__ import annotations

from . import physics
from .constants import SECONDS_PER_DAY, SECONDS_PER_HOUR
from .mission import (
    MissionInputs,
    design_dv,
    max_cargo_per_launch,
    simulate_round_trip,
    thrust_for_trips,
)
from .parameters import ParameterSet
from .traceability import Calculation, CalculationLog, InputRef

KG_PER_T = 1_000.0
W_PER_KW = 1_000.0
M_S_PER_KM_S = 1_000.0


def build_baseline_log(params: ParameterSet) -> CalculationLog:
    """Run the baseline and return the full calculation log."""
    log = CalculationLog(params)
    _propulsion_and_trip(log)
    _launch(log)
    _sensitivity_dv(log)
    _excluded_llo(log)
    _staging_orbit(log)
    _power_for_trip_targets(log)
    _thruster_life(log)
    _validation(log)
    return log


# ------------------------------------------------------------------ helpers
def _inputs(log: CalculationLog, **kwargs) -> MissionInputs:
    return MissionInputs.from_parameters(log.params, **kwargs)


def _trip_inputs(log: CalculationLog) -> tuple[InputRef, ...]:
    """Inputs common to every round-trip calculation."""
    names = ("cargo_outbound", "cargo_return", "dry_mass", "isp", "thrust", "duty_cycle")
    return tuple(log.param(n) for n in names)


# ------------------------------------------------------------------ sections
def _propulsion_and_trip(log: CalculationLog) -> None:
    p = log.params
    ve = log.add(
        Calculation(
            "CALC-01",
            "Exhaust velocity",
            physics.exhaust_velocity(p.value("isp")),
            "m/s",
            "v_e = Isp * g0",
            (log.param("isp"), InputRef("g0", 9.80665, "m/s^2", "constant")),
        )
    )
    dv = log.add(
        Calculation(
            "CALC-02",
            "Design delta-v per leg",
            design_dv(p.value("dv_per_leg_base"), p.value("dv_margin")) / M_S_PER_KM_S,
            "km/s",
            "dv = dv_base * (1 + margin)",
            (log.param("dv_per_leg_base"), log.param("dv_margin")),
            mdn_ref="A-06, §5.2, §6.2",
            mdn_value=2.64,
            rel_tolerance=0.001,
        )
    )
    log.add(
        Calculation(
            "CALC-03",
            "EP input power at reference thrust",
            physics.jet_power(p.value("thrust"), p.value("isp"), p.value("thruster_efficiency")) / W_PER_KW,
            "kW",
            "P = T * v_e / (2 * eta)",
            (log.param("thrust"), ve.as_input(), log.param("thruster_efficiency")),
            mdn_ref="§1.2, §5.2, A-17 (~18 kW)",
            mdn_value=18.0,
        )
    )
    log.add(
        Calculation(
            "CALC-04",
            "Propellant mass flow",
            physics.mass_flow_rate(p.value("thrust"), p.value("isp")) * 1e6,
            "mg/s",
            "mdot = T / v_e",
            (log.param("thrust"), ve.as_input()),
        )
    )

    trip = simulate_round_trip(_inputs(log))
    common = _trip_inputs(log)
    ret = log.add(
        Calculation(
            "CALC-05",
            "Return-leg propellant",
            trip.propellant_return_kg / KG_PER_T,
            "t",
            "m_p,ret = (m_dry + m_cargo,ret) * (exp(dv / v_e) - 1)",
            common + (dv.as_input(),),
        )
    )
    out = log.add(
        Calculation(
            "CALC-06",
            "Outbound-leg propellant",
            trip.propellant_outbound_kg / KG_PER_T,
            "t",
            "m_p,out = (m_dry + m_cargo,out + m_p,ret) * (exp(dv / v_e) - 1)",
            common + (dv.as_input(), ret.as_input()),
            note="The tug carries its return propellant on the outbound leg (refuelled only in Earth orbit).",
        )
    )
    total = log.add(
        Calculation(
            "CALC-07",
            "Propellant per round trip",
            trip.propellant_total_kg / KG_PER_T,
            "t",
            "m_p = m_p,out + m_p,ret",
            (out.as_input(), ret.as_input()),
            mdn_ref="A-10, §5.2, SYS-REQ-004 (~2.5 t)",
            mdn_value=2.5,
        )
    )
    log.add(
        Calculation(
            "CALC-08",
            "Tug mass at departure from staging orbit",
            trip.initial_mass_kg / KG_PER_T,
            "t",
            "m_0 = m_dry + m_cargo,out + m_p",
            common + (total.as_input(),),
        )
    )
    t_out = log.add(
        Calculation(
            "CALC-09",
            "Outbound transfer time",
            trip.transfer_outbound_days,
            "days",
            "t_out = m_p,out / mdot / duty_cycle",
            common + (out.as_input(),),
            mdn_ref="§5.2, §6.2, §6.3 (~430 d)",
            mdn_value=430.0,
            rel_tolerance=0.005,
        )
    )
    t_ret = log.add(
        Calculation(
            "CALC-10",
            "Return transfer time",
            trip.transfer_return_days,
            "days",
            "t_ret = m_p,ret / mdot / duty_cycle",
            common + (ret.as_input(),),
            mdn_ref="§5.2, §6.2, §6.3 (~234 d)",
            mdn_value=234.0,
            rel_tolerance=0.005,
        )
    )
    rt = log.add(
        Calculation(
            "CALC-11",
            "Round-trip duration",
            trip.round_trip_years,
            "years",
            "t_rt = (t_out + t_ret + t_ends) / 365.25",
            (t_out.as_input(), t_ret.as_input(), log.param("end_time_per_round_trip")),
            mdn_ref="§1.2, §5.2, §6.3 (~2.0 yr)",
            mdn_value=2.0,
        )
    )
    log.add(
        Calculation(
            "CALC-12",
            "Round trips in design life",
            float(trip.trips_in_life),
            "trips",
            "N = floor(L / t_rt)",
            (rt.as_input(), log.param("design_life")),
            mdn_ref="§1.2, A-03, §6.3 (7)",
            mdn_value=7.0,
            rel_tolerance=0.0,
            note="Commissioning time after launch is not deducted; last return leg must fit.",
        )
    )


def _launch(log: CalculationLog) -> None:
    p = log.params
    trip = simulate_round_trip(_inputs(log))
    need = log.add(
        Calculation(
            "CALC-13",
            "Launch mass needed per round trip",
            trip.launch_mass_per_trip_kg / KG_PER_T,
            "t",
            "m_launch = m_cargo,out + m_p",
            (log.param("cargo_outbound"), log["CALC-07"].as_input()),
            mdn_ref="C-1, A-10 (~7.5 t)",
            mdn_value=7.5,
        )
    )
    log.add(
        Calculation(
            "CALC-14",
            "Unused Ariane 64 GTO capacity per trip",
            (p.value("launcher_gto_capacity") - trip.launch_mass_per_trip_kg) / KG_PER_T,
            "t",
            "margin = C_GTO - m_launch",
            (log.param("launcher_gto_capacity"), need.as_input()),
            mdn_ref="C-1 (~4.0 t)",
            mdn_value=4.0,
        )
    )
    cargo_max = max_cargo_per_launch(_inputs(log), p.value("launcher_gto_capacity"))
    log.add(
        Calculation(
            "CALC-15",
            "Max cargo per Ariane 64 (GTO, NRHO destination)",
            cargo_max / KG_PER_T,
            "t",
            "solve m_cargo + m_p(m_cargo) = C_GTO",
            _trip_inputs(log) + (log.param("launcher_gto_capacity"),),
            mdn_ref="A-01, A-10, D-10 (~8.5 t)",
            mdn_value=8.5,
        )
    )
    log.add(
        Calculation(
            "CALC-16",
            "Ariane 64 direct capacity to lunar transfer orbit",
            p.value("launcher_lto_capacity") / KG_PER_T,
            "t",
            "input (direct-launch baseline for Step 4)",
            (log.param("launcher_lto_capacity"),),
            mdn_ref="D-09 (~8.6 t)",
            mdn_value=8.6,
            note="Includes any lunar insertion hardware; not directly comparable with CALC-15 (cargo delivered into NRHO).",
        )
    )


def _sensitivity_dv(log: CalculationLog) -> None:
    p = log.params
    base = p.value("dv_per_leg_sensitivity_base")
    trip = simulate_round_trip(_inputs(log, dv_per_leg_base_m_s=base))
    log.add(
        Calculation(
            "CALC-17",
            "Propellant per round trip, delta-v sensitivity case",
            trip.propellant_total_kg / KG_PER_T,
            "t",
            "as CALC-07 with dv = dv_sens * (1 + margin)",
            _trip_inputs(log) + (log.param("dv_per_leg_sensitivity_base"), log.param("dv_margin")),
            mdn_ref="A-10 (3.3 t)",
            mdn_value=3.3,
            note="The MDN value applies the 10% margin to 3.1 km/s (3.41 km/s per leg). "
            "The MDN should say so explicitly.",
        )
    )
    log.add(
        Calculation(
            "CALC-18",
            "Round trips in life, delta-v sensitivity case",
            float(trip.trips_in_life),
            "trips",
            "as CALC-12 with dv = dv_sens * (1 + margin)",
            (log.param("dv_per_leg_sensitivity_base"),),
        )
    )


def _excluded_llo(log: CalculationLog) -> None:
    p = log.params
    alt = p.value("llo_altitude")
    v_circ = physics.circular_speed_moon(alt)
    extra = log.add(
        Calculation(
            "CALC-19",
            "Extra delta-v per leg NRHO to LLO (estimate)",
            v_circ / M_S_PER_KM_S,
            "km/s",
            "dv_extra ~ v_circ(LLO) = sqrt(mu_moon / (R_moon + h))",
            (log.param("llo_altitude"),),
            mdn_ref="§6.1 item 5, D-10 (~1.6 km/s)",
            mdn_value=1.6,
            note="Low-thrust spiral delta-v is approximated by the local circular speed (own estimate).",
        )
    )
    llo_inputs = _inputs(log, dv_per_leg_base_m_s=p.value("dv_per_leg_base") + v_circ)
    cargo_llo = max_cargo_per_launch(llo_inputs, p.value("launcher_gto_capacity"))
    log.add(
        Calculation(
            "CALC-20",
            "Max cargo per Ariane 64 if the destination were LLO",
            cargo_llo / KG_PER_T,
            "t",
            "as CALC-15 with dv = (dv_base + dv_extra) * (1 + margin)",
            (log["CALC-15"].as_input(), extra.as_input(), log.param("dv_margin")),
            mdn_ref="§6.1 item 5, D-10 (6.6 t)",
            mdn_value=6.6,
        )
    )
    period = log.add(
        Calculation(
            "CALC-21",
            "LLO orbital period",
            physics.orbital_period_moon(alt) / 60.0,
            "min",
            "T = 2 pi sqrt(r^3 / mu_moon)",
            (log.param("llo_altitude"),),
            mdn_ref="§5.1 item 3 (~118 min)",
            mdn_value=118.0,
        )
    )
    log.add(
        Calculation(
            "CALC-22",
            "LLO worst-case eclipse per orbit",
            physics.max_eclipse_fraction_moon(alt) * period.value,
            "min",
            "t_ecl = T * asin(R_moon / r) / pi  (beta = 0, cylindrical shadow)",
            (log.param("llo_altitude"), period.as_input()),
            mdn_ref="§5.1 item 3 (~46 min)",
            mdn_value=46.0,
        )
    )


def _staging_orbit(log: CalculationLog) -> None:
    p = log.params
    log.add(
        Calculation(
            "CALC-23",
            "LEO-to-GEO delta-v relative to GTO-to-NRHO",
            p.value("leo_to_geo_dv") / p.value("dv_per_leg_base"),
            "-",
            "ratio = dv(LEO->GEO) / dv(GTO->NRHO)",
            (log.param("leo_to_geo_dv"), log.param("dv_per_leg_base")),
            mdn_ref="D-02, §6.1 item 4 (more than twice)",
            mdn_value=None,
            note="Supports D-02: > 2 means a LEO start needs more than twice the delta-v.",
        )
    )


def _power_for_trip_targets(log: CalculationLog) -> None:
    p = log.params
    inputs = _inputs(log)
    targets = log.params.trades.get("trip_targets", [])
    mdn_values = {(10, 15.0): 25.0, (8, 10.0): 30.0}
    for index, (trips, years) in enumerate(targets, start=24):
        thrust = thrust_for_trips(inputs, int(trips), float(years))
        power_kw = physics.jet_power(thrust, p.value("isp"), p.value("thruster_efficiency")) / W_PER_KW
        log.add(
            Calculation(
                f"CALC-{index}",
                f"EP power for {int(trips)} round trips in {years:g} years",
                power_kw,
                "kW",
                "solve t_rt(T) = years * 365.25 / trips, then P = T * v_e / (2 * eta)",
                _trip_inputs(log) + (log.param("thruster_efficiency"), log.param("end_time_per_round_trip")),
                mdn_ref="§1.2, A-03, §6.3",
                mdn_value=mdn_values.get((int(trips), float(years))),
                rel_tolerance=0.05,
                note=f"Required thrust {thrust:.3f} N. Dry mass held constant (Step 4 adds growth with power).",
            )
        )


def _thruster_life(log: CalculationLog) -> None:
    p = log.params
    thrust_unit = physics.thrust_from_power(
        p.value("thruster_unit_power"), p.value("thruster_unit_isp"), p.value("thruster_unit_efficiency")
    )
    throughput_kg = (
        physics.mass_flow_rate(thrust_unit, p.value("thruster_unit_isp"))
        * p.value("thruster_rated_life")
        * SECONDS_PER_HOUR
    )
    unit = log.add(
        Calculation(
            "CALC-26",
            "Xenon throughput of one 12 kW-class thruster over rated life",
            throughput_kg / KG_PER_T,
            "t",
            "m_xe = (2 * eta * P / v_e) / v_e * life",
            (
                log.param("thruster_unit_power"),
                log.param("thruster_unit_isp"),
                log.param("thruster_unit_efficiency"),
                log.param("thruster_rated_life"),
            ),
            mdn_ref="§5.2 (~2,000 kg, own estimate)",
            mdn_value=2.0,
            rel_tolerance=0.10,
        )
    )
    trip = simulate_round_trip(_inputs(log))
    life_xenon_t = trip.propellant_total_kg * trip.trips_in_life / KG_PER_T
    life = log.add(
        Calculation(
            "CALC-27",
            "Xenon processed over the design life",
            life_xenon_t,
            "t",
            "m_life = m_p * N",
            (log["CALC-07"].as_input(), log["CALC-12"].as_input()),
            note="Input to the Step 6 thruster-life assessment.",
        )
    )
    log.add(
        Calculation(
            "CALC-28",
            "Thruster lifetimes consumed over the design life",
            life.value / unit.value,
            "-",
            "n = m_life / m_xe,unit",
            (life.as_input(), unit.as_input()),
            note="How many 12 kW-class thruster lifetimes the mission uses; drives spares/replacement (Step 6).",
        )
    )


def _validation(log: CalculationLog) -> None:
    p = log.params
    rimani_prop = physics.propellant_for_dv_from_initial(
        p.value("rimani_initial_mass"), p.value("rimani_dv"), p.value("rimani_isp")
    )
    rimani_days = (
        physics.burn_time(rimani_prop, p.value("rimani_thrust"), p.value("rimani_isp")) / SECONDS_PER_DAY
    )
    log.add(
        Calculation(
            "VAL-01",
            "Rimani et al. tug: thrusting time at 1.05 N",
            rimani_days,
            "days",
            "t = m_0 * (1 - exp(-dv / v_e)) / mdot",
            (
                log.param("rimani_initial_mass"),
                log.param("rimani_dv"),
                log.param("rimani_isp"),
                log.param("rimani_thrust"),
            ),
            mdn_ref="§6.1 item 1 (340 d own check; paper: 364 d elapsed)",
            mdn_value=340.0,
            rel_tolerance=0.01,
            note="340 d thrusting inside a 364 d transfer (93%) supports the 1.05 N reference thrust.",
        )
    )
    log.add(
        Calculation(
            "VAL-02",
            "Gateway PPE thrusting duty cycle",
            p.value("ppe_thrusting_time") / p.value("ppe_transfer_time"),
            "-",
            "duty = t_thrust / t_transfer",
            (log.param("ppe_thrusting_time"), log.param("ppe_transfer_time")),
            mdn_ref="A-17 (85%)",
            mdn_value=0.85,
            rel_tolerance=0.03,
        )
    )
    smart1_prop = physics.propellant_for_dv_from_initial(
        p.value("smart1_launch_mass"), p.value("smart1_dv"), p.value("smart1_isp")
    )
    log.add(
        Calculation(
            "VAL-03",
            "SMART-1 xenon predicted by the rocket equation",
            smart1_prop,
            "kg",
            "m_p = m_0 * (1 - exp(-dv / v_e))",
            (log.param("smart1_launch_mass"), log.param("smart1_dv"), log.param("smart1_isp")),
            mdn_ref="§6.1 item 3 (82 kg flown)",
            mdn_value=p.value("smart1_xenon_used"),
            rel_tolerance=0.05,
            note="Checks that the rocket-equation approach matches a flown European EP mission.",
        )
    )


__all__ = ["build_baseline_log"]
