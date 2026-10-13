"""Logical architecture budgets: power per mode, eclipse, battery, array, heat.

The platform loads per logical component and mode are engineering estimates,
so they live in ``config/power_budget.toml`` next to their basis. This module
checks that file, adds up the loads, and sizes the power chain at the design
point (D-16) as logged calculations CALC-29 to CALC-39.

Sizing uses the platform power *allocation* (A-21, 2 kW), not the current
estimate: the allocation is what PWR-01 promises, and the estimate plus its
margin must stay inside it (checked by CALC-32 and the tests).
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from . import physics
from .constants import SECONDS_PER_HOUR
from .mission import LinearPowerDryMass, MissionInputs, RoundTripResult, simulate_round_trip
from .traceability import Calculation, CalculationLog

Row = dict[str, float | int | str]


class BudgetError(ValueError):
    """Raised when the power budget file is incomplete or inconsistent."""


@dataclass(frozen=True)
class ComponentLoads:
    """Nominal platform load of one logical component in every mode [W]."""

    key: str
    lc_id: str
    name: str
    basis: str
    loads: Mapping[str, float]


@dataclass(frozen=True)
class PowerBudget:
    """Platform power budget: components x modes."""

    modes: tuple[str, ...]
    components: tuple[ComponentLoads, ...]

    def platform_load(self, mode: str) -> float:
        """Sum of the nominal platform loads in one mode [W]."""
        if mode not in self.modes:
            raise BudgetError(f"Unknown mode '{mode}'. Modes: {list(self.modes)}")
        return sum(c.loads[mode] for c in self.components)

    def worst_mode(self) -> str:
        """Mode with the highest platform load."""
        return max(self.modes, key=self.platform_load)

    def rows(self, margin: float) -> list[Row]:
        """One row per component plus total and margined total rows."""
        rows: list[Row] = []
        for c in self.components:
            row: Row = {"id": c.lc_id, "component": c.name}
            row.update({m: round(c.loads[m]) for m in self.modes})
            rows.append(row)
        total: Row = {"id": "", "component": "Total (nominal)"}
        total.update({m: round(self.platform_load(m)) for m in self.modes})
        with_margin: Row = {"id": "", "component": f"Total with {margin:.0%} margin"}
        with_margin.update({m: round(self.platform_load(m) * (1.0 + margin)) for m in self.modes})
        return rows + [total, with_margin]


def load_power_budget(path: str | Path) -> PowerBudget:
    """Load and check the power budget file.

    Checks: every component has an ID, a name, a basis and a non-negative
    load for every mode, and no load for an unknown mode.
    """
    data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    modes = tuple(data["meta"]["modes"])
    if not modes:
        raise BudgetError("No modes listed in [meta].")
    components = []
    for key, c in data["components"].items():
        for field in ("id", "name", "basis", "loads"):
            if field not in c or (isinstance(c[field], str) and not c[field].strip()):
                raise BudgetError(f"Component {key} has no {field}.")
        loads = {m: float(v) for m, v in c["loads"].items()}
        if set(loads) != set(modes):
            raise BudgetError(f"Component {key} must give a load for exactly the modes {list(modes)}.")
        if any(v < 0.0 for v in loads.values()):
            raise BudgetError(f"Component {key} has a negative load.")
        components.append(ComponentLoads(key, c["id"], c["name"], c["basis"], loads))
    return PowerBudget(modes, tuple(components))


def design_point_trip(params) -> RoundTripResult:
    """Round trip at the design-point power (D-16), with dry mass growing with power (A-23)."""
    inputs = MissionInputs.from_parameters(params)
    reference_power_w = simulate_round_trip(inputs).power_w
    mass_model = LinearPowerDryMass(
        params.value("dry_mass"), reference_power_w, params.value("ep_specific_mass") / 1_000.0
    )
    thrust = physics.thrust_from_power(
        params.value("design_ep_power"), inputs.isp_s, inputs.thruster_efficiency
    )
    return simulate_round_trip(inputs.with_changes(thrust_n=thrust, dry_mass_model=mass_model))


def add_budget_calculations(log: CalculationLog, budget: PowerBudget) -> None:
    """Add CALC-29 to CALC-39: eclipse, efficiency split, power, battery, array, heat, xenon rate."""
    p = log.params
    hp, ha = p.value("staging_perigee_altitude"), p.value("staging_apogee_altitude")
    orbit_inputs = (log.param("staging_perigee_altitude"), log.param("staging_apogee_altitude"))

    log.add(
        Calculation(
            "CALC-29",
            "Longest eclipse in the GTO-class staging orbit",
            physics.max_eclipse_at_apogee_earth(hp, ha) / SECONDS_PER_HOUR,
            "h",
            "t = 2 R_E / v_apogee (cylindrical shadow, apogee on the anti-Sun line)",
            orbit_inputs,
            note="Basis of the design eclipse A-28 (2.5 h) and of SR-12.",
        )
    )
    period = log.add(
        Calculation(
            "CALC-30",
            "Orbital period of the staging orbit",
            physics.orbital_period_earth(hp, ha) / SECONDS_PER_HOUR,
            "h",
            "T = 2 pi sqrt(a^3 / mu_E)",
            orbit_inputs,
        )
    )
    log.add(
        Calculation(
            "CALC-31",
            "Thruster total efficiency from PPU and thruster efficiencies",
            p.value("ppu_efficiency") * p.value("thruster_anode_efficiency"),
            "-",
            "eta = eta_PPU * eta_thruster",
            (log.param("ppu_efficiency"), log.param("thruster_anode_efficiency")),
            mdn_ref="A-19 (60 %)",
            mdn_value=p.value("thruster_efficiency"),
            note="D-22: EP power is defined at the PPU input, so A-19 is read as PPU x thruster.",
        )
    )

    worst = budget.worst_mode()
    margin = p.value("power_margin")
    log.add(
        Calculation(
            "CALC-32",
            f"Highest platform load with margin ({worst.capitalize()} mode)",
            budget.platform_load(worst) * (1.0 + margin),
            "W",
            "P = sum of component loads in the worst mode * (1 + margin)",
            (log.param("power_margin"),),
            mdn_ref="A-21 allocation",
            note=(
                f"Nominal {budget.platform_load(worst):.0f} W from config/power_budget.toml (A-33). "
                f"Must stay inside the {p.value('platform_power'):.0f} W allocation (A-21)."
            ),
        )
    )

    platform_w = p.value("platform_power")
    t_ecl_h = p.value("design_eclipse")
    eta_bat = p.value("battery_efficiency")
    energy_out_wh = platform_w * t_ecl_h / eta_bat
    log.add(
        Calculation(
            "CALC-33",
            "Battery energy required",
            energy_out_wh / p.value("battery_dod") / 1_000.0,
            "kWh",
            "E = P_platform * t_eclipse / (eta_bat * DoD)",
            (
                log.param("platform_power"),
                log.param("design_eclipse"),
                log.param("battery_efficiency"),
                log.param("battery_dod"),
            ),
            note="Thrusters are off in eclipse (A-17), so the battery carries the platform only.",
        )
    )
    recharge = log.add(
        Calculation(
            "CALC-34",
            "Battery recharge power in Transfer",
            energy_out_wh / eta_bat / (period.value - t_ecl_h),
            "W",
            "P = (P_platform * t_eclipse / eta_bat) / eta_bat / (T_orbit - t_eclipse)",
            (log.param("platform_power"), log.param("design_eclipse"), period.as_input()),
            note="Recharge spread over the sunlit part of the staging orbit; could instead be taken from EP power after each eclipse.",
        )
    )
    p_ep = p.value("design_ep_power")
    array_eol = log.add(
        Calculation(
            "CALC-35",
            "Solar array power required at end of life",
            (p_ep + platform_w + recharge.value) / p.value("distribution_efficiency") / 1_000.0,
            "kW",
            "P_EOL = (P_EP + P_platform + P_recharge) / eta_distribution",
            (
                log.param("design_ep_power"),
                log.param("platform_power"),
                recharge.as_input(),
                log.param("distribution_efficiency"),
            ),
            note="The trade-offs counted about 27 kW (25 + 2); losses and recharge add the rest.",
        )
    )
    log.add(
        Calculation(
            "CALC-36",
            "Solar array power at beginning of life",
            array_eol.value / p.value("array_eol_bol_ratio"),
            "kW",
            "P_BOL = P_EOL / (EOL/BOL ratio)",
            (array_eol.as_input(), log.param("array_eol_bol_ratio")),
            note="Sets the array size, a cost driver for the TRL and cost assessment.",
        )
    )
    ppu_heat = log.add(
        Calculation(
            "CALC-37",
            "PPU waste heat at the design point",
            p_ep * (1.0 - p.value("ppu_efficiency")),
            "W",
            "Q = P_EP * (1 - eta_PPU)",
            (log.param("design_ep_power"), log.param("ppu_efficiency")),
            note="Heat the PROP-TCS interface must carry (IR-03). Thruster losses radiate from the thrusters themselves.",
        )
    )
    log.add(
        Calculation(
            "CALC-38",
            "Heat to reject in Transfer",
            ppu_heat.value + platform_w,
            "W",
            "Q = Q_PPU + P_platform (all platform power ends up as heat)",
            (ppu_heat.as_input(), log.param("platform_power")),
            note="Radiator sizing input for TCS.",
        )
    )
    trip = design_point_trip(p)
    log.add(
        Calculation(
            "CALC-39",
            "Average xenon transfer rate during refuelling",
            trip.propellant_total_kg / p.value("xenon_transfer_time"),
            "kg/day",
            "rate = m_p per trip (design point) / transfer time",
            (log.param("design_ep_power"), log.param("xenon_transfer_time")),
            note=f"Xenon per trip at the design point: {trip.propellant_total_kg:.0f} kg. SR-09 rounds it to 2,550 kg (IR-02).",
        )
    )
