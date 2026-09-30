# cislunar-tug: calculation model

Python model behind the numbers in the Mission Definition Note (TUG-MDN-001 Issue 2) and the base for the Step 4 trade-offs.

Every study assumption lives in one parameter file with a reference to the note. Every result is logged with its formula, inputs and a check against the value the note states. If the note and the model disagree, the run says so and exits with an error code.

## Quick start

Requires Python 3.11 or later. No dependencies for calculations; matplotlib for charts.

```bash
pip install -e ".[plot,dev]"
cislunar-tug run --plots            # baseline -> results/baseline/
cislunar-tug run --set thrust=1.5 --out results/thrust-1p5
pytest                              # 35 tests, including reproduction of the note
```

Exit codes: `0` model and note agree; `1` at least one value differs (expected for variant runs); `2` bad input.

## Layout

```
config/baseline.toml        all study parameters: value, unit, ref (A-xx / C-x / D-xx / §), source
src/cislunar_tug/
  constants.py              physical constants (g0, lunar mu and radius)
  parameters.py             load and validate parameters; overrides are marked in outputs
  physics.py                rocket equation, EP power and mass flow, lunar orbits, bisection solver
  mission.py                round-trip model, max cargo per launch, thrust needed for N trips
  baseline.py               CALC-01..28 and VAL-01..03: every number in the note, with its MDN reference
  trades.py                 one-at-a-time sweeps (thrust, cargo, delta-v); Step 4 builds on this
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

Outputs per run: `calculation_log.md` (read this first), `calculation_log.json`/`.csv`, `parameters_used.md`, one CSV per sweep, `run_metadata.json`, and `thrust_sweep.png` with `--plots`.

## Model and its limits

- Round trip = outbound leg (5 t cargo) + return leg (0.5 t) + 60 days at the ends. The tug carries its return propellant outbound and is refuelled only in Earth orbit.
- Tsiolkovsky rocket equation per leg; constant thrust and Isp, so thrusting time = propellant / mass flow; an 85% duty cycle converts thrusting time to elapsed time.
- **Delta-v does not depend on thrust.** Real low-thrust delta-v rises slightly at low thrust-to-weight; the published 2.4 km/s (+10%) is used at all thrust levels.
- **Dry mass is constant (5.9 t) in the baseline.** `LinearPowerDryMass` is ready for Step 4 to make array and thruster mass grow with power; the coefficient must come from a cited source.
- Trips in life = floor(life / round-trip time); commissioning time is not deducted.
- LLO extra delta-v is approximated by the local circular speed (own estimate).
- Validation: VAL-01 reproduces the Rimani et al. transfer, VAL-02 the Gateway PPE duty cycle, VAL-03 SMART-1's flown xenon (79.7 kg predicted vs 82 kg flown).

## Adding the Step 4 trade

- Power levels: edit `[trades].thrust_levels_n` or call `trades.thrust_sweep`.
- Mass growth with power: pass `dry_mass_model=LinearPowerDryMass(...)` to `MissionInputs.from_parameters`; `thrust_for_trips` and `max_cargo_per_launch` work unchanged.
- New results: add a `Calculation` with a new `CALC-xx` ID in `baseline.py` (or a new module), so it appears in the log with its inputs.
