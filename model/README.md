# cislunar-tug: calculation model

Python model behind the numbers in the Mission Definition Note (TUG-MDN-001 Issue 2) and the trade-offs (power level vs transfer time, thruster configuration, refuelling concept).

Every study assumption lives in one parameter file with a reference to the note. Every result is logged with its formula, inputs and a check against the value the note states. If the note and the model disagree, the run says so and exits with an error code.

For the physics, formulas and a step-by-step run guide, see [`docs/calculation-model.md`](../docs/calculation-model.md).

## Quick start

Requires Python 3.11 or later. No dependencies for calculations; matplotlib for charts. `constraints.txt` pins the exact package versions last verified (`pip install -e ".[plot,dev]" -c constraints.txt`).

```bash
pip install -e ".[plot,dev]"
cislunar-tug run                    # baseline -> results/baseline/ (tables and charts)
cislunar-tug run --set ep_specific_mass=40 --out results/alpha-40   # variant, marked on the charts
cislunar-tug run --no-plots         # tables only
pytest                              # 73 tests, including reproduction of the note and the trade-off conclusions
ruff check . && ruff format --check .   # lint and format
```

Exit codes: `0` model and note agree; `1` at least one value differs (expected for variant runs); `2` bad input.

## Layout

```
config/baseline.toml        all study parameters: value, unit, ref (A-xx / C-x / D-xx / §), source
config/refuelling_trade.toml  Trade 2: options, criteria, weights, scores with a reason for each
config/power_budget.toml    logical architecture: platform load per component and mode, with a basis for each
config/mass_budget.toml     TRL and cost: dry mass lines per component, ESA maturity category and basis
src/cislunar_tug/
  constants.py              physical constants (g0, Earth and Moon mu and radius, time units)
  parameters.py             load and validate parameters; overrides are marked in outputs
  physics.py                rocket equation, EP power and mass flow, lunar orbits, bisection solver
  mission.py                round-trip model, max cargo per launch, thrust needed for N trips
  baseline.py               CALC-01..28 and VAL-01..03: every number in the note, with its MDN reference
  trades.py                 one-at-a-time sweeps and the power trade (mass growth, thruster count and wear)
  refuelling.py             Trade 2: load and check the scoring file, weighted totals, sensitivity
  budgets.py                logical architecture: power budget per mode, eclipse, battery, array, heat (CALC-29..39)
  assessment.py             TRL and cost: mass budget, thruster life strategies, launch campaign (CALC-40..50)
  traceability.py           calculation log and its Markdown/JSON/CSV export
  run.py, cli.py, plots.py  orchestration, command line, charts
tests/                      unit tests, behaviour tests, reproduction of the note (incl. table 6.3)
results/baseline/           outputs of the committed baseline run
```

## How traceability works

1. **Input:** `thrust = 1.05 N [A-17] - Rimani et al. (2020) operating point`
2. **Calculation:** `CALC-09 Outbound transfer time = m_p,out / mdot / duty_cycle`, with every input listed with its ref (`A-xx` for parameters, `CALC-xx` for earlier results).
3. **Check:** CALC-09 = 430.1 days; the note says ~430 days in §5.2, §6.2, §6.3 → `MATCH`.
4. **Provenance:** `run_metadata.json` records the time, model version, git commit, and SHA-256 of the parameter file. Overridden parameters are listed and tagged `(override)`.

Outputs per run: `calculation_log.md` (read this first), `calculation_log.json`/`.csv`, `parameters_used.md`, one CSV per sweep, `power_trade.csv` and `power_trade_sensitivity.csv`, `refuelling_trade_scores.csv` and `refuelling_trade_sensitivity.csv`, `power_budget.csv`, `mass_budget.csv` and `mass_budget_items.csv`, `thruster_life_strategies.csv`, `launch_campaign.csv`, `run_metadata.json`, and the chart `power_trade.png` (power, equivalent thrust, round trips and round-trip time) (skipped with `--no-plots` or if matplotlib is not installed). A variant run names its overridden parameters under the chart title.

## Model and its limits

- Round trip = outbound leg (5 t cargo) + return leg (0.5 t) + 60 days at the ends. The tug carries its return propellant outbound and is refuelled only in Earth orbit.
- Tsiolkovsky rocket equation per leg; constant thrust and Isp, so thrusting time = propellant / mass flow; an 85% duty cycle converts thrusting time to elapsed time.
- **Delta-v does not depend on thrust.** Real low-thrust delta-v rises slightly at low thrust-to-weight; the published 2.4 km/s (+10%) is used at all thrust levels.
- **Dry mass is constant (5.9 t) in the mission definition baseline log.** The power trade makes it grow with power, `m_dry = 5.9 t + alpha (P - 18 kW)`, with alpha = 25 kg/kW (A-23, own estimate, swept 15-40 kg/kW).
- Trips in life = floor(life / round-trip time); commissioning time is not deducted.
- LLO extra delta-v is approximated by the local circular speed (own estimate).
- Validation: VAL-01 reproduces the Rimani et al. transfer, VAL-02 the Gateway PPE duty cycle, VAL-03 SMART-1's flown xenon (79.7 kg predicted vs 82 kg flown).

## Trade-offs

- **Trade 1, power vs transfer time:** `trades.power_trade` sweeps EP power (`[trades].power_levels_kw`). Thrust follows from power at fixed Isp and efficiency, dry mass grows with power, and each row also sizes the thruster set for a 12 kW class and a 5 kW European class (A-24): units firing at once (power / unit power, rounded to the nearest whole unit with halves up, so each runs near nominal), N+1 installed, firing hours per unit, share of rated life and rated lifetimes the mission consumes. Wear is counted in firing hours. With the default `spare_policy = "rotation"` (A-27) the N+1 units take turns, so each carries N/(N+1) of the thrusting time; `"cold"` keeps the spare idle until a failure. `[trades].ep_specific_mass_kg_per_kw` gives the mass sensitivity.
- **Trade 2, refuelling concept:** `refuelling.load_scoring` reads `config/refuelling_trade.toml` and refuses a score outside 1-5, a score without a reason, or weights that do not sum to 100. Totals are computed for six weight sets.
- **Tests that guard the conclusions:** 25 kW still gives 9 trips with 10 % less power; more power never loses trips; 25 kW maps onto 5+1 five-kW units and 24 kW onto 2+1 twelve-kW units, both at nominal power and 9 trips (D-20); rotation spreads wear but leaves the lifetimes needed unchanged and above 100 %; R1 is never below second.
- **Logical architecture budget:** `budgets.load_power_budget` reads `config/power_budget.toml` and refuses a component without a basis or without a load for every mode. `add_budget_calculations` sizes the battery, the array and the heat rejection at the design point (D-16) from the 2 kW platform allocation (A-21). Tests check that the estimate plus its 20 % margin stays inside the allocation in every mode, and that the PPU and thruster efficiencies give back the 60 % used in the trades (CALC-31).
- **TRL and cost assessment:** `assessment.load_mass_budget` reads `config/mass_budget.toml` and refuses a line without a basis or with an unknown maturity category; margins follow the ESA margin philosophy (5/10/20 % plus 20 % system). `life_strategy_rows` counts propulsion-module exchanges for each rated string life, and `campaign_rows` compares the launches the tug needs with direct Ariane 64 launches for the same cargo. Tests check that the bottom-up mass stays below the parametric baseline (so 9 trips is a floor), that a replacement module fits a resupply launch, and that about 7 t per trip still gives 9 trips.
- **Adding a trade:** put new inputs in the parameter file with a ref and source, add a function returning plain rows in `trades.py`, write it from `run.py`, and add a test that checks the conclusion you draw from it.
