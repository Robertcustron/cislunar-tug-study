# Calculation Model: Physics, Code and How to Run It

**Issue:** 1 (13 October 2026) · Model version `cislunar-tug` 1.0.0

This document explains the Python model behind every number in the study: the physics and formulas it uses, how the code is organised, and how to run it step by step. The model reproduces the mission definition note, runs the trade-offs (power level vs transfer time, thruster configuration, refuelling concept) sizes the power chain of the logical architecture, and runs the TRL and cost assessment (mass budget, thruster life strategy, launch campaign). Code: [`model/`](../model/). Results of the committed baseline run: [`model/results/baseline/`](../model/results/baseline/).

## 1. What the model answers

For a reusable electric tug that carries 5 t of cargo from a GTO-class staging orbit to NRHO and comes back to be refuelled:

1. How much xenon does one round trip need?
2. How long does a round trip take, and how many fit in a 15-year life?
3. How do these change with electric propulsion power, given that more power means a heavier tug?
4. How many thrusters does each power level need, and how far beyond their rated life do they run?
5. Which refuelling concept scores best, and does the answer survive different weightings?
6. How large must the solar array, battery and heat rejection be at the design point?
7. How heavy is the tug bottom-up, how often must its thrusters be replaced, and how many launches does it need compared with launching the cargo directly?

Questions 1 to 4, 6 and 7 are physics or bookkeeping. Question 5 is a structured judgement, so the code only does the arithmetic and checks the scoring file.

## 2. Physics and formulas

All formulas are in [`physics.py`](../model/src/cislunar_tug/physics.py) and [`mission.py`](../model/src/cislunar_tug/mission.py). Symbols and baseline values:

| Symbol | Meaning | Baseline | Ref |
| --- | --- | --- | --- |
| g₀ | Standard gravity | 9.80665 m/s² | constant |
| I_sp | Specific impulse | 2,100 s | A-17 |
| η | Thruster total efficiency (jet power / electrical power) | 0.60 | A-19 |
| P | Electric power to the thrusters | 25 kW (design point, D-16) | D-16 |
| Δv | Delta-v per leg, including margin | 2.4 km/s × 1.10 = 2.64 km/s | A-06 |
| m_c | Cargo out / back | 5,000 kg / 500 kg | A-01, A-02 |
| m_dry | Tug dry mass | 5.9 t at 18 kW, grows with power | A-10, A-23 |
| δ | Thrusting duty cycle | 0.85 | A-17 |
| t_end | Fixed time at the two ends per round trip | 60 days | A-18 |
| L | Design life | 15 years | A-03 |

### 2.1 Electric propulsion

Exhaust velocity:

$$v_e = I_{sp}\, g_0 \qquad (2{,}100 \text{ s} \rightarrow 20{,}594 \text{ m/s})$$

Power, thrust and mass flow. The jet carries kinetic power ½ṁv_e² = ½Tv_e; the thruster turns a fraction η of the electrical power into it:

$$P = \frac{T\, v_e}{2\eta} \quad\Longleftrightarrow\quad T = \frac{2\eta P}{v_e}, \qquad \dot m = \frac{T}{v_e}$$

At 25 kW: T = 1.46 N and ṁ = 70.7 mg/s. Thrust is proportional to power at fixed I_sp and η. That is why the power chart can show an equivalent-thrust axis.

The trade-off this hides: for the same power, a higher I_sp gives less thrust but uses less propellant. The model keeps I_sp fixed at 2,100 s and treats 1,800 s as a sensitivity case.

### 2.2 Rocket equation

Tsiolkovsky, written from the **final** mass, because the end state of each leg is known:

$$m_p = m_f \left(e^{\Delta v / v_e} - 1\right)$$

### 2.3 Round-trip mass bookkeeping

The tug leaves the staging orbit with the propellant for both legs, because it is only refuelled in Earth orbit (MO-3). So the model works **backwards** from the end of the trip:

1. Return leg final mass: m_f,ret = m_dry + m_c,ret
2. Return propellant: m_p,ret = m_f,ret (e^(Δv/v_e) − 1)
3. Outbound final mass: m_f,out = m_dry + m_c,out + m_p,ret (the return propellant is still on board on arrival at NRHO)
4. Outbound propellant: m_p,out = m_f,out (e^(Δv/v_e) − 1)
5. Departure mass: m_0 = m_f,out + m_p,out

At 25 kW: m_dry = 6.07 t, m_p,ret = 0.90 t, m_p,out = 1.64 t, **2.54 t of xenon per trip**, and the departure mass is 13.6 t.

### 2.4 Time

Constant thrust and I_sp give a constant mass flow, so thrusting time is exact:

$$t_{thrust} = \frac{m_p}{\dot m}, \qquad t_{leg} = \frac{t_{thrust}}{\delta}$$

The duty cycle δ = 0.85 accounts for eclipses, navigation and other pauses. It is taken from Gateway PPE, which planned 319 thrusting days in 383 (VAL-02).

$$t_{rt} = t_{out} + t_{ret} + t_{end}, \qquad N_{trips} = \left\lfloor \frac{L}{t_{rt}} \right\rfloor$$

At 25 kW: outbound 315 days, return 173 days, round trip 548 days (1.50 years), **9 trips**. The floor function is why the trip count moves in steps. A trip counts only if it fits completely in the life.

### 2.5 Dry mass growing with power (power trade-off only)

More power needs larger arrays, more power processing units, more thrusters and more radiators. The model makes dry mass grow linearly above the 18 kW reference point:

$$m_{dry}(P) = 5.9 \text{ t} + \alpha\,(P - 18 \text{ kW}), \qquad \alpha = 25 \text{ kg/kW (A-23, swept 15–40)}$$

The mission definition baseline log (CALC-01 to CALC-28) keeps dry mass constant at 5.9 t, as in the note. Only the power trade-off uses this growth model.

### 2.6 Inverse questions (bisection)

Some questions run backwards, such as "what power gives 10 trips in 15 years?" or "how much cargo fits one launch with its propellant?" The model answers them by bisection: it repeatedly halves an interval until round-trip time, or launch mass, hits the target. A closed form would break once dry mass depends on power. Bisection does not. Used in CALC-15, CALC-20, CALC-24 and CALC-25.

### 2.7 Thruster count and wear (D-20, A-27)

For each thruster class (12 kW class, 23,000 h rated; 5 kW European class, 15,000 h rated):

| Quantity | Formula | 25 kW, 5 kW class |
| --- | --- | --- |
| Units firing together, N | P / unit power, nearest whole unit, halves up | 5 |
| Units installed | N + 1 | 6 |
| Load | P / (N × unit power) | 100 % |
| Thrusting hours in life, H | trips × (thrusting days out + back) × 24 | ≈ 89,700 h |
| Hours per unit (rotation) | H × N / (N + 1) | 74.7 kh (498 % of rated) |
| Lifetimes needed | N × H / rated life | 29.9 |

Rotation spreads the wear over all N + 1 units, but it does not change the total number of lifetimes needed. Trip count is set by thrust, and so by power, not by thruster life. Thruster life is a ceiling the design must stay under. That gap is the main finding of the trade-offs (D-18), and it leads into the TRL and cost assessment.

### 2.8 Lunar orbit checks (excluded LLO case)

These are only used to show why the tug stops at NRHO (D-10):

$$v_{circ} = \sqrt{\mu_{Moon}/r}, \qquad T_{orb} = 2\pi\sqrt{r^3/\mu_{Moon}}, \qquad f_{eclipse,max} = \frac{\arcsin(R_{Moon}/r)}{\pi}$$

The extra Δv to spiral down to a 100 km LLO is approximated by the local circular speed, about 1.6 km/s per leg. That is an own estimate.

### 2.9 Refuelling scoring

$$S_{option} = \frac{1}{100}\sum_{c} w_c \, s_{option,c}$$

Each score s is an integer from 1 to 5 with a one-line rationale. Each weight set sums to 100. The same scores are re-ranked under 6 weight sets to see whether the winner changes.

### 2.10 Power budget and sizing (logical architecture)

The platform loads of the eight logical components in each mode are own estimates in `config/power_budget.toml`, each with its basis. [`budgets.py`](../model/src/cislunar_tug/budgets.py) adds them up and sizes the power chain at the design point (CALC-29 to CALC-39). Sizing uses the 2 kW platform allocation P_pl (A-21), not the estimate.

Longest eclipse in the staging orbit (cylindrical shadow, apogee on the anti-Sun line), with the apogee speed from the vis-viva equation:

$$v_a = \sqrt{\mu_E\left(\frac{2}{r_a} - \frac{1}{a}\right)}, \qquad t_{ecl} \approx \frac{2R_E}{v_a} \qquad (250 \times 35{,}786 \text{ km} \rightarrow 1.60 \text{ km/s}, 2.2 \text{ h})$$

Battery, recharge, array and heat, with design eclipse t_d = 2.5 h, battery efficiency η_b, depth of discharge DoD, orbit period T and distribution efficiency η_d:

$$E_{bat} = \frac{P_{pl}\, t_d}{\eta_b \, DoD}, \qquad P_{rech} = \frac{P_{pl}\, t_d}{\eta_b^2\,(T - t_d)}, \qquad P_{EOL} = \frac{P_{EP} + P_{pl} + P_{rech}}{\eta_d}, \qquad P_{BOL} = \frac{P_{EOL}}{EOL/BOL}$$

$$Q_{PPU} = P_{EP}\,(1 - \eta_{PPU}), \qquad Q_{Transfer} = Q_{PPU} + P_{pl}$$

At the design point: 8.8 kWh, 0.69 kW, 29.1 kW at end of life, 38.9 kW at beginning of life, 1.25 kW of PPU heat and 3.25 kW in total. CALC-31 checks that the PPU and thruster efficiencies (0.95 × 0.63) give back the 60 % used everywhere else (D-22).

### 2.11 Mass budget, thruster life and launch campaign (TRL and cost assessment)

[`assessment.py`](../model/src/cislunar_tug/assessment.py) reads `config/mass_budget.toml`, where every line has a mass, an ESA maturity category c (5, 10 or 20 %) and a basis:

$$m_{dry} = (1 + s)\sum_i m_i (1 + c_i), \qquad s = 20\,\% \ \text{system margin}$$

A set of N + 1 thruster strings in rotation fires h = H_trip × N / (N + 1) hours per string per trip, so with rated life L a set lasts floor(L / h) trips, and over n trips

$$\text{exchanges} = \left\lceil \frac{n}{\lfloor L/h \rfloor} \right\rceil - 1$$

A direct Ariane 64 launch to lunar transfer orbit (m_LTO = 8.6 t) with an expendable carrier of dry mass m_c on a ballistic transfer of Δv delivers

$$m_{cargo} = m_{LTO}\, e^{-\Delta v / (I_{sp} g_0)} - m_c \qquad (100 \text{ m/s},\ 300 \text{ s},\ 1.2 \text{ t} \rightarrow 7.1 \text{ t})$$

The tug needs one launch for itself plus one resupply launch per trip. CALC-40 to CALC-50 log the results; CALC-50 finds by bisection the largest cargo per trip that keeps 9 trips (7.29 t).

### 2.12 Main simplifications

- **Delta-v does not depend on thrust.** Real low-thrust transfers need slightly more Δv at lower thrust-to-weight. The published 2.4 km/s plus 10 % is used at every power level.
- Constant I_sp and η: no throttling, no degradation over life.
- Commissioning time is not deducted from the 15-year life.
- Dry mass growth is linear, with one own-estimate coefficient that is swept.

### 2.13 Validation against flown and published missions

| Check | Model | Reference |
| --- | --- | --- |
| VAL-01 Rimani et al. tug, thrusting time at 1.05 N | 340 days | 364 days elapsed (paper) |
| VAL-02 Gateway PPE duty cycle | 0.833 | 0.85 used (A-17) |
| VAL-03 SMART-1 xenon from the rocket equation | 79.7 kg | 82 kg flown |

## 3. Code structure

```
model/
├── config/
│   ├── baseline.toml            every parameter: value, unit, ref (A-xx, C-x, D-xx, §), source
│   ├── refuelling_trade.toml    refuelling options, criteria, weights, scores with rationale
│   ├── power_budget.toml        platform load of each logical component in each mode, with basis
│   └── mass_budget.toml         dry mass lines per component, ESA maturity category, basis
├── src/cislunar_tug/
│   ├── constants.py             g0, Earth and lunar mu and radius, time conversions
│   ├── parameters.py            load and validate parameters; overrides
│   ├── physics.py               formulas of section 2.1, 2.2, 2.4, 2.6, 2.8 and the eclipse of 2.10
│   ├── mission.py               round-trip model (section 2.3–2.5) and inverse solvers
│   ├── baseline.py              CALC-01..28 and VAL-01..03: every number in the mission note
│   ├── trades.py                sweeps and the power trade (mass growth, thruster count and wear)
│   ├── refuelling.py            scoring arithmetic and sensitivity (section 2.9)
│   ├── budgets.py               power budget per mode and power-chain sizing, CALC-29..39 (section 2.10)
│   ├── assessment.py            mass budget, thruster life strategies, launch campaign, CALC-40..50 (section 2.11)
│   ├── traceability.py          calculation log and its Markdown/JSON/CSV export
│   ├── run.py                   runs everything and writes the outputs
│   ├── plots.py                 the power trade chart
│   └── cli.py                   the `cislunar-tug` command
├── tests/                       73 tests (unit, behaviour, reproduction of the note and trade results)
└── results/baseline/            committed outputs of the baseline run
```

### 3.1 How the pieces connect

```
baseline.toml ──► parameters.load_parameters ──► ParameterSet
                                                   │
                     ┌─────────────────────────────┼──────────────────────────────┐
                     ▼                             ▼                              ▼
         baseline.build_baseline_log     trades.power_trade_from_parameters   refuelling.load_scoring
         (CALC/VAL entries, each         (one round trip per power level,     (weighted totals per
          checked against the note)        thruster count and wear)             weight set)
         budgets.add_budget_calculations          assessment.add_assessment_calculations
         (CALC-29..39 from power_budget.toml)    (CALC-40..50 from mass_budget.toml)
                     │                             │                              │
                     └──────────────► run.run ◄────┴──────────────────────────────┘
                                         │
                       CSV, Markdown, JSON, PNG in results/<name>/
```

### 3.2 Main functions

| Module | Function / class | What it does |
| --- | --- | --- |
| `parameters` | `load_parameters(path)` | Reads the TOML file. Rejects any parameter without a unit, a reference or a source |
| | `ParameterSet.with_overrides(**kw)` | Returns a copy with some values changed, tagged `(override)` in every output |
| `physics` | `exhaust_velocity`, `jet_power`, `thrust_from_power`, `mass_flow_rate` | Section 2.1 |
| | `propellant_for_dv_from_final` / `_from_initial` | Rocket equation, section 2.2 |
| | `burn_time` | m_p / ṁ |
| | `circular_speed_moon`, `orbital_period_moon`, `max_eclipse_fraction_moon` | Section 2.8 |
| | `apoapsis_speed_earth`, `orbital_period_earth`, `max_eclipse_at_apogee_earth` | Section 2.10 |
| | `bisect(f, lo, hi)` | Root finder for the inverse questions |
| `mission` | `MissionInputs.from_parameters(params)` | Collects the inputs one round trip needs, with margin applied to Δv |
| | `ConstantDryMass`, `LinearPowerDryMass` | The two dry mass models (section 2.5) |
| | `simulate_round_trip(inputs)` → `RoundTripResult` | Section 2.3 and 2.4: propellant, leg times, round-trip time, trips in life |
| | `max_cargo_per_launch(inputs, capacity)` | Largest cargo whose cargo + propellant fits one Ariane 64 |
| | `thrust_for_trips(inputs, trips, years)` | Minimum thrust for N trips in a given time |
| `baseline` | `build_baseline_log(params)` | Rebuilds every number of the mission note as a logged calculation |
| `trades` | `sweep(inputs, spec)` | One-at-a-time sweep of any input (cargo, Δv, thrust) |
| | `power_trade(...)`, `power_trade_from_parameters(params, levels)` | The power trade-off, including thruster columns (section 2.7) |
| | `ThrusterUnit` | Power, I_sp, efficiency and rated life of one thruster class |
| `refuelling` | `load_scoring(path)` → `ScoringTable` | Reads and checks the scoring file |
| | `ScoringTable.totals(weight_set)`, `.ranking(...)` | Weighted totals and ranking |
| `budgets` | `load_power_budget(path)` → `PowerBudget` | Reads and checks the power budget file (every component, every mode, a basis for each) |
| | `PowerBudget.platform_load(mode)`, `.worst_mode()`, `.rows(margin)` | Totals per mode, with and without margin |
| | `add_budget_calculations(log, budget)` | CALC-29 to CALC-39: eclipse, efficiency check, battery, array, heat, xenon transfer rate |
| `assessment` | `load_mass_budget(path)` → `MassBudget` | Reads and checks the mass budget (category, basis for every line); totals with maturity and system margins |
| | `life_strategy_rows(params, budget)`, `module_plan(h, L, n)` | Strings and propulsion-module exchanges for each rated life |
| | `campaign_rows(params)`, `direct_cargo_per_launch(params)`, `max_cargo_for_trips(params, n)` | Tug vs direct launches for the same cargo; largest cargo per trip for n trips |
| `traceability` | `Calculation`, `CalculationLog` | Value, formula, inputs with their refs, value in the note, MATCH / DIFFERS / NEW |
| `run` | `run(params, out_dir, make_plots)` | Runs everything and writes all outputs |
| `cli` | `main()` | Command-line options `--config`, `--out`, `--set`, `--no-plots`, `-v` |

### 3.3 Traceability, in one example

Each logged result carries its own provenance:

```
CALC-09  Outbound transfer time = 430.1 days
         formula:  m_p,out / mdot / duty_cycle
         inputs:   CALC-06 (outbound propellant), CALC-04 (mass flow), duty_cycle = 0.85 [A-17]
         note says ~430 days (§5.2, §6.2, §6.3)  →  MATCH
```

If a parameter change makes the model disagree with the note, the run lists the difference and exits with code 1. `run_metadata.json` records the time, model version, git commit and a SHA-256 hash of the parameter file, so every result can be traced to the exact inputs.

## 4. How to run it, step by step

These steps use Windows PowerShell. Linux and macOS differences are noted in brackets.

**1. Install Python 3.11 or later.** Download it from python.org and tick "Add python.exe to PATH" during setup. Check it in a new terminal:

```powershell
python --version        # must show 3.11 or later   [macOS/Linux: python3 --version]
```

**2. Get the code.** Clone the repository, or pull the latest version if you already have it:

```powershell
git clone https://github.com/Robertcustron/cislunar-tug-study.git
cd cislunar-tug-study\model
# already cloned:  git pull
```

**3. Create a virtual environment** (once). This keeps the model's packages separate from the rest of your system:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1      # [macOS/Linux: source .venv/bin/activate]
```

If PowerShell refuses to run the activation script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then try again. The prompt now starts with `(.venv)`.

**4. Install the model** (once):

```powershell
pip install -e ".[plot,dev]"
```

`-e` installs in editable mode, so changes to the code take effect without reinstalling. `plot` adds matplotlib for the chart and `dev` adds pytest and ruff. The calculations themselves need no external packages. To get exactly the package versions the model was last verified with, add `-c constraints.txt`. Keep the editable install: the command line finds `config/baseline.toml` relative to the source folder.

**5. Run the tests:**

```powershell
pytest
```

Expected: `73 passed`. The tests check the formulas, reproduce the mission note's numbers and confirm the trade-off conclusions (for example 9 trips at 25 kW).

**6. Run the baseline:**

```powershell
cislunar-tug run
```

Expected output:

```
53 calculations: MATCH 23, NEW 30
Outputs written to results\baseline
Charts: power_trade.png
```

`MATCH` means the model reproduces the value stated in the note. `NEW` means the note gives no value to check against. The exit code is 0.

**7. Read the outputs** in `results\baseline\`:

| File | What it contains |
| --- | --- |
| `calculation_log.md` | Start here: every CALC and VAL entry with its formula, inputs and check |
| `parameters_used.md` | Every input actually used, with its reference and source |
| `power_trade.csv`, `power_trade.png` | The power trade-off table and chart |
| `power_budget.csv` | Platform power of each logical component in each mode, with totals |
| `mass_budget.csv`, `mass_budget_items.csv` | Dry mass by component and by line, with ESA margins |
| `thruster_life_strategies.csv`, `launch_campaign.csv` | Propulsion-module exchanges per rated life; tug vs direct launches |
| `power_trade_sensitivity.csv` | The same trade at α = 15, 25 and 40 kg/kW |
| `refuelling_trade_scores.csv`, `refuelling_trade_sensitivity.csv` | Refuelling scores and ranking under each weight set |
| `thrust_sweep.csv`, `cargo_sensitivity.csv`, `dv_sensitivity.csv` | One-at-a-time sweeps |
| `calculation_log.json` / `.csv`, `run_metadata.json` | Machine-readable log and provenance |

**8. Run a variant.** Change any parameter without editing the file, and write to a separate folder so the baseline stays untouched:

```powershell
cislunar-tug run --set ep_specific_mass=40 --out results\alpha-40
cislunar-tug run --set isp=1800 --set thruster_efficiency=0.55 --out results\isp-1800
cislunar-tug run --set end_time_per_round_trip=120 --out results\end-120 --no-plots
```

Parameter names are the ones in `config\baseline.toml`. Overridden values are tagged `(override)` in every output and named under the chart title. A variant prints a `WARNING` line for each value that no longer matches the note, and exits with code 1. That is expected: it tells you exactly which numbers of the note the change moves.

**9. Change the study's settings.** To change the power levels, the α sweep or the spare policy (`"rotation"` or `"cold"`), edit the `[trades]` table in `config\baseline.toml`. To change a baseline assumption, edit its `[parameters.*]` entry and add the change to the assumption register in the mission note. Then rerun steps 5 and 6.

**10. Use it from Python** (optional), for example in a notebook:

```python
from cislunar_tug.parameters import load_parameters
from cislunar_tug.trades import power_trade_from_parameters

params = load_parameters("config/baseline.toml")
for row in power_trade_from_parameters(params, [20, 25, 30]):
    print(row["power_kw"], row["thrust_n"], row["round_trip_years"], row["trips_in_life"])
```

### Troubleshooting

| Symptom | Fix |
| --- | --- |
| `cislunar-tug` is not recognised | The virtual environment is not active (step 3), or step 4 was skipped |
| `Charts skipped: matplotlib is not installed` | `pip install -e ".[plot]"` |
| `error: Unknown parameter 'x'.` (exit code 2) | Misspelled name in `--set`; use the names in `config\baseline.toml` |
| Exit code 1 on a variant run | Expected: the variant differs from the note. Read the DIFFERS rows in `calculation_log.md` |
| `pytest` finds no tests | Run it from the `model` folder |
