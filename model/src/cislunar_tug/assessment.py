"""TRL and cost assessment: bottom-up dry mass, thruster life strategies, launch campaign.

Three questions the earlier phases left open, answered with numbers that can be
rerun and challenged:

* How heavy is the tug bottom-up, with ESA maturity and system margins, and how
  does that compare with the published parametric placeholder (A-10, A-23)?
* How is the thruster wear-out (D-18) handled: how many thruster strings and
  propulsion-module exchanges does each rated life imply over 15 years?
* Per launch, does the tug deliver more cargo to NRHO than a direct Ariane 64
  launch with an expendable carrier (D-09)?

The mass lines are engineering estimates, so they live in
``config/mass_budget.toml`` next to their basis and maturity category.
"""

from __future__ import annotations

import math
import tomllib
from dataclasses import dataclass
from pathlib import Path

from . import physics
from .budgets import design_point_trip
from .constants import G0
from .mission import ConstantDryMass, LinearPowerDryMass, MissionInputs, simulate_round_trip
from .traceability import Calculation, CalculationLog
from .trades import units_for_power

Row = dict[str, float | int | str]


class MassBudgetError(ValueError):
    """Raised when the mass budget file is incomplete or inconsistent."""


@dataclass(frozen=True)
class MassItem:
    """One line of the bottom-up mass budget."""

    lc: str
    item: str
    mass_kg: float
    category: str
    basis: str
    in_string_module: bool

    def margin_kg(self, categories: dict[str, float]) -> float:
        return self.mass_kg * categories[self.category]


@dataclass(frozen=True)
class MassBudget:
    """Bottom-up dry mass with ESA maturity margins."""

    items: tuple[MassItem, ...]
    categories: dict[str, float]

    def nominal_kg(self) -> float:
        return sum(i.mass_kg for i in self.items)

    def with_maturity_kg(self) -> float:
        return sum(i.mass_kg + i.margin_kg(self.categories) for i in self.items)

    def string_module_kg(self) -> float:
        """Mass of one exchangeable propulsion module (strings, mechanisms, its structure), with maturity margin."""
        return sum(i.mass_kg + i.margin_kg(self.categories) for i in self.items if i.in_string_module)

    def rows(self, system_margin: float) -> list[Row]:
        """One row per logical component, then totals."""
        total_mat = self.with_maturity_kg()
        rows: list[Row] = []
        for lc in sorted({i.lc for i in self.items}, key=lambda s: int(s.split("-")[1])):
            items = [i for i in self.items if i.lc == lc]
            nominal = sum(i.mass_kg for i in items)
            margin = sum(i.margin_kg(self.categories) for i in items)
            rows.append(
                {
                    "lc": lc,
                    "nominal_kg": round(nominal),
                    "maturity_margin_kg": round(margin),
                    "with_margin_kg": round(nominal + margin),
                    "share_pct": round(100.0 * (nominal + margin) / total_mat, 1),
                }
            )
        rows.append(
            {
                "lc": "Total",
                "nominal_kg": round(self.nominal_kg()),
                "maturity_margin_kg": round(total_mat - self.nominal_kg()),
                "with_margin_kg": round(total_mat),
                "share_pct": 100.0,
            }
        )
        rows.append(
            {
                "lc": f"Total with {system_margin:.0%} system margin",
                "nominal_kg": "",
                "maturity_margin_kg": "",
                "with_margin_kg": round(total_mat * (1.0 + system_margin)),
                "share_pct": "",
            }
        )
        return rows

    def item_rows(self) -> list[Row]:
        return [
            {
                "lc": i.lc,
                "item": i.item,
                "nominal_kg": i.mass_kg,
                "category": i.category,
                "margin_pct": round(100 * self.categories[i.category]),
                "with_margin_kg": round(i.mass_kg + i.margin_kg(self.categories), 1),
                "basis": i.basis,
            }
            for i in self.items
        ]


def load_mass_budget(path: str | Path) -> MassBudget:
    """Load and check the mass budget: every line has a mass, a known category and a basis."""
    data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    categories = {k: float(v) for k, v in data["categories"].items()}
    items = []
    for raw in data["items"]:
        for field in ("lc", "item", "mass", "category", "basis"):
            if field not in raw or (isinstance(raw[field], str) and not raw[field].strip()):
                raise MassBudgetError(f"Mass item {raw.get('item', '?')} has no {field}.")
        if raw["category"] not in categories:
            raise MassBudgetError(f"Mass item {raw['item']}: unknown category {raw['category']!r}.")
        if float(raw["mass"]) <= 0.0:
            raise MassBudgetError(f"Mass item {raw['item']}: mass must be > 0.")
        items.append(
            MassItem(
                raw["lc"],
                raw["item"],
                float(raw["mass"]),
                raw["category"],
                raw["basis"],
                bool(raw.get("string", False)),
            )
        )
    return MassBudget(tuple(items), categories)


# ------------------------------------------------------------------ thruster life
def thrusting_hours_per_trip(params) -> float:
    """Thrusting hours of one round trip at the design point [h]."""
    trip = design_point_trip(params)
    return (trip.thrusting_outbound_days + trip.thrusting_return_days) * 24.0


def module_plan(hours_per_unit_per_trip: float, rated_life_h: float, trips: int) -> tuple[int, int]:
    """Trips one set of strings lasts, and the number of exchanges over the life.

    A set is replaced before any unit would pass its rated life, so it lasts
    ``floor(rated / hours per trip)`` whole trips (at least one).
    """
    life_trips = max(1, math.floor(rated_life_h / hours_per_unit_per_trip))
    sets = math.ceil(trips / life_trips)
    return life_trips, sets - 1


def life_strategy_rows(params, budget: MassBudget | None = None) -> list[Row]:
    """Thruster life strategies: strings and propulsion-module exchanges over the design life.

    The 5 kW class is evaluated at the 25 kW baseline (5+1 strings); the 12 kW
    class at its own design point, 24 kW with 2+1 strings (D-20).
    """
    module_kg = round(budget.string_module_kg()) if budget else ""
    rows: list[Row] = []
    classes = [
        (
            "5 kW European class",
            params,
            params.value("european_thruster_unit_power"),
            list(params.trades.get("life_options_h", [])),
        ),
        (
            "12 kW class (24 kW option)",
            params.with_overrides(design_ep_power=2 * params.value("thruster_unit_power")),
            params.value("thruster_unit_power"),
            [params.value("thruster_rated_life")],
        ),
    ]
    for name, case, unit_w, lives in classes:
        trips = design_point_trip(case).trips_in_life
        h_trip = thrusting_hours_per_trip(case)
        n = units_for_power(case.value("design_ep_power"), unit_w)
        per_unit = h_trip * n / (n + 1)  # rotation, A-27
        for life in lives:
            life_trips, exchanges = module_plan(per_unit, life, trips)
            rows.append(
                {
                    "unit_class": name,
                    "strings_installed": n + 1,
                    "rated_life_kh": round(life / 1000.0, 1),
                    "hours_per_unit_per_trip_kh": round(per_unit / 1000.0, 2),
                    "set_lasts_trips": life_trips,
                    "module_exchanges": exchanges,
                    "strings_over_life": (exchanges + 1) * (n + 1),
                    "lifetimes_needed": round(n * h_trip * trips / life, 1),
                    "module_mass_kg": module_kg if name.startswith("5 kW") else "",
                }
            )
    return rows


# ------------------------------------------------------------------ launch campaign
def direct_cargo_per_launch(params) -> float:
    """Cargo an Ariane 64 delivers to NRHO directly, on a ballistic lunar transfer with an expendable carrier [kg]."""
    ve = params.value("direct_carrier_isp") * G0
    after_burn = params.value("launcher_lto_capacity") * math.exp(-params.value("direct_transfer_dv") / ve)
    return after_burn - params.value("direct_carrier_dry_mass")


def _design_inputs(params) -> MissionInputs:
    inputs = MissionInputs.from_parameters(params)
    reference_power_w = simulate_round_trip(inputs).power_w
    mass_model = LinearPowerDryMass(
        params.value("dry_mass"), reference_power_w, params.value("ep_specific_mass") / 1_000.0
    )
    thrust = physics.thrust_from_power(
        params.value("design_ep_power"), inputs.isp_s, inputs.thruster_efficiency
    )
    return inputs.with_changes(thrust_n=thrust, dry_mass_model=mass_model)


def campaign_rows(params) -> list[Row]:
    """Launches needed over the life: tug (one launch + one resupply per trip) vs direct launches for the same cargo."""
    base = _design_inputs(params)
    direct = direct_cargo_per_launch(params)
    rows: list[Row] = []
    for cargo in params.trades.get("campaign_cargo_kg", []):
        trip = simulate_round_trip(base.with_changes(cargo_outbound_kg=cargo))
        total_t = trip.trips_in_life * cargo / 1000.0
        payload = cargo + trip.propellant_total_kg + params.value("propellant_module_dry_mass")
        tug_launches = trip.trips_in_life + 1
        direct_launches = math.ceil(total_t * 1000.0 / direct)
        rows.append(
            {
                "cargo_per_trip_t": round(cargo / 1000.0, 2),
                "trips_in_life": trip.trips_in_life,
                "round_trip_years": round(trip.round_trip_years, 3),
                "cargo_over_life_t": round(total_t, 1),
                "resupply_launch_payload_t": round(payload / 1000.0, 2),
                "spare_capacity_t": round((params.value("launcher_gto_capacity") - payload) / 1000.0, 2),
                "tug_launches": tug_launches,
                "tug_cargo_per_launch_t": round(total_t / tug_launches, 2),
                "direct_cargo_per_launch_t": round(direct / 1000.0, 2),
                "direct_launches_same_cargo": direct_launches,
                "extra_launches_with_tug": tug_launches - direct_launches,
            }
        )
    return rows


def max_cargo_for_trips(params, trips: int) -> float:
    """Largest cargo per trip that still gives ``trips`` round trips in the design life [kg]."""
    base = _design_inputs(params)
    target = params.value("design_life") * 365.25 / trips

    def gap(cargo: float) -> float:
        return simulate_round_trip(base.with_changes(cargo_outbound_kg=cargo)).round_trip_days - target

    return physics.bisect(gap, 1000.0, params.value("launcher_gto_capacity"))


# ------------------------------------------------------------------ logged calculations
def add_assessment_calculations(log: CalculationLog, budget: MassBudget) -> None:
    """CALC-40 to CALC-50: dry mass, life strategy, launch campaign."""
    p = log.params
    sys_margin = p.value("mass_system_margin")
    nominal = log.add(
        Calculation(
            "CALC-40",
            "Bottom-up dry mass, nominal",
            budget.nominal_kg() / 1000.0,
            "t",
            "sum of the lines in config/mass_budget.toml",
            (),
            note="Own estimates and public sources per line (A-34).",
        )
    )
    with_maturity = log.add(
        Calculation(
            "CALC-41",
            "Bottom-up dry mass with maturity margins",
            budget.with_maturity_kg() / 1000.0,
            "t",
            "sum of mass * (1 + 5 / 10 / 20 % by maturity category)",
            (nominal.as_input(),),
            note="ESA margin philosophy SRE-PA/2011.097 (A-35).",
        )
    )
    bottom_up = log.add(
        Calculation(
            "CALC-42",
            "Bottom-up dry mass with system margin",
            with_maturity.value * (1.0 + sys_margin),
            "t",
            "m = m_maturity * (1 + system margin)",
            (with_maturity.as_input(), log.param("mass_system_margin")),
        )
    )
    trip = design_point_trip(p)
    parametric = log.add(
        Calculation(
            "CALC-43",
            "Parametric dry mass at the design point (baseline)",
            trip.dry_mass_kg / 1000.0,
            "t",
            "m = 5.9 t + alpha * (P - 18 kW)",
            (log.param("dry_mass"), log.param("ep_specific_mass"), log.param("design_ep_power")),
            note=f"The bottom-up estimate is {100 * (bottom_up.value / (trip.dry_mass_kg / 1000.0) - 1):+.0f} % of this value (D-32).",
        )
    )
    inputs = _design_inputs(p)
    light = simulate_round_trip(inputs.with_changes(dry_mass_model=ConstantDryMass(bottom_up.value * 1000.0)))
    log.add(
        Calculation(
            "CALC-44",
            "Round trips in life at the bottom-up dry mass",
            float(light.trips_in_life),
            "trips",
            "as CALC-12 at 25 kW with dry mass = CALC-42",
            (bottom_up.as_input(), parametric.as_input()),
            note="The baseline (9 trips) uses the heavier parametric value, so 9 is a floor.",
        )
    )
    module = log.add(
        Calculation(
            "CALC-45",
            "Exchangeable propulsion module mass with maturity margin",
            budget.string_module_kg(),
            "kg",
            "sum of the string lines (thrusters, PPUs, mechanisms, module structure)",
            (),
        )
    )
    payload = p.value("cargo_outbound") + trip.propellant_total_kg + p.value("propellant_module_dry_mass")
    log.add(
        Calculation(
            "CALC-46",
            "Spare capacity on each resupply launch",
            (p.value("launcher_gto_capacity") - payload) / 1000.0,
            "t",
            "capacity - (cargo + xenon per trip + propellant module)",
            (
                log.param("launcher_gto_capacity"),
                log.param("cargo_outbound"),
                log.param("propellant_module_dry_mass"),
            ),
            note=f"Room for a replacement propulsion module ({module.value:.0f} kg) on any resupply launch.",
        )
    )
    n = units_for_power(p.value("design_ep_power"), p.value("european_thruster_unit_power"))
    per_unit_h = thrusting_hours_per_trip(p) * n / (n + 1)
    per_unit = log.add(
        Calculation(
            "CALC-47",
            "Firing hours per thruster string per trip (5+1, rotation)",
            per_unit_h / 1000.0,
            "kh",
            "h = thrusting h per trip * N / (N + 1)",
            (log.param("design_ep_power"), log.param("european_thruster_unit_power")),
        )
    )
    _, exchanges = module_plan(per_unit_h, p.value("european_thruster_rated_life"), trip.trips_in_life)
    log.add(
        Calculation(
            "CALC-48",
            "Propulsion-module exchanges over life at 15,000 h rated life",
            float(exchanges),
            "exchanges",
            "sets = ceil(trips / floor(rated life / CALC-47)); exchanges = sets - 1",
            (per_unit.as_input(), log.param("european_thruster_rated_life")),
            note="See thruster_life_strategies.csv for 20, 50 and 75 kh and for the 12 kW class.",
        )
    )
    log.add(
        Calculation(
            "CALC-49",
            "Cargo to NRHO per direct Ariane 64 launch",
            direct_cargo_per_launch(p) / 1000.0,
            "t",
            "m = m_LTO * exp(-dv / (Isp g0)) - m_carrier",
            (
                log.param("launcher_lto_capacity"),
                log.param("direct_transfer_dv"),
                log.param("direct_carrier_isp"),
                log.param("direct_carrier_dry_mass"),
            ),
            note="The D-09 comparison: the tug carries 5 t per resupply launch.",
        )
    )
    log.add(
        Calculation(
            "CALC-50",
            "Largest cargo per trip that keeps 9 round trips",
            max_cargo_for_trips(p, trip.trips_in_life) / 1000.0,
            "t",
            "solve t_rt(cargo) = 15 years / 9 at 25 kW",
            (log.param("design_ep_power"), log.param("design_life")),
            note="Zero margin on the trip time at this value; about 7 t keeps a small margin (D-30).",
        )
    )
