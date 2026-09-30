# Calculation log

Parameters: `config/baseline.toml` (sha256 `358554a397db`)

Status: **MATCH** = agrees with TUG-MDN-001 within tolerance; **DIFFERS** = document and model disagree; **NEW** = not in the document.

## Summary

| ID | Result | Value | Unit | MDN ref | MDN value | Status |
|---|---|---|---|---|---|---|
| CALC-01 | Exhaust velocity | 20,594 | m/s |  |  | NEW |
| CALC-02 | Design delta-v per leg | 2.640 | km/s | A-06, §5.2, §6.2 | 2.640 | MATCH |
| CALC-03 | EP input power at reference thrust | 18.0 | kW | §1.2, §5.2, A-17 (~18 kW) | 18.0 | MATCH |
| CALC-04 | Propellant mass flow | 51.0 | mg/s |  |  | NEW |
| CALC-05 | Return-leg propellant | 0.8753 | t |  |  | NEW |
| CALC-06 | Outbound-leg propellant | 1.611 | t |  |  | NEW |
| CALC-07 | Propellant per round trip | 2.486 | t | A-10, §5.2, SYS-REQ-004 (~2.5 t) | 2.500 | MATCH |
| CALC-08 | Tug mass at departure from staging orbit | 13.4 | t |  |  | NEW |
| CALC-09 | Outbound transfer time | 430.1 | days | §5.2, §6.2, §6.3 (~430 d) | 430.0 | MATCH |
| CALC-10 | Return transfer time | 233.8 | days | §5.2, §6.2, §6.3 (~234 d) | 234.0 | MATCH |
| CALC-11 | Round-trip duration | 1.982 | years | §1.2, §5.2, §6.3 (~2.0 yr) | 2.000 | MATCH |
| CALC-12 | Round trips in design life | 7.000 | trips | §1.2, A-03, §6.3 (7) | 7.000 | MATCH |
| CALC-13 | Launch mass needed per round trip | 7.486 | t | C-1, A-10 (~7.5 t) | 7.500 | MATCH |
| CALC-14 | Unused Ariane 64 GTO capacity per trip | 4.014 | t | C-1 (~4.0 t) | 4.000 | MATCH |
| CALC-15 | Max cargo per Ariane 64 (GTO, NRHO destination) | 8.531 | t | A-01, A-10, D-10 (~8.5 t) | 8.500 | MATCH |
| CALC-16 | Ariane 64 direct capacity to lunar transfer orbit | 8.600 | t | D-09 (~8.6 t) | 8.600 | MATCH |
| CALC-17 | Propellant per round trip, delta-v sensitivity case | 3.323 | t | A-10 (3.3 t) | 3.300 | MATCH |
| CALC-18 | Round trips in life, delta-v sensitivity case | 5.000 | trips |  |  | NEW |
| CALC-19 | Extra delta-v per leg NRHO to LLO (estimate) | 1.634 | km/s | §6.1 item 5, D-10 (~1.6 km/s) | 1.600 | MATCH |
| CALC-20 | Max cargo per Ariane 64 if the destination were LLO | 6.589 | t | §6.1 item 5, D-10 (6.6 t) | 6.600 | MATCH |
| CALC-21 | LLO orbital period | 117.8 | min | §5.1 item 3 (~118 min) | 118.0 | MATCH |
| CALC-22 | LLO worst-case eclipse per orbit | 46.5 | min | §5.1 item 3 (~46 min) | 46.0 | MATCH |
| CALC-23 | LEO-to-GEO delta-v relative to GTO-to-NRHO | 2.500 | - | D-02, §6.1 item 4 (more than twice) |  | NEW |
| CALC-24 | EP power for 10 round trips in 15 years | 24.5 | kW | §1.2, A-03, §6.3 | 25.0 | MATCH |
| CALC-25 | EP power for 8 round trips in 10 years | 30.2 | kW | §1.2, A-03, §6.3 | 30.0 | MATCH |
| CALC-26 | Xenon throughput of one 12 kW-class thruster over rated life | 1.926 | t | §5.2 (~2,000 kg, own estimate) | 2.000 | MATCH |
| CALC-27 | Xenon processed over the design life | 17.4 | t |  |  | NEW |
| CALC-28 | Thruster lifetimes consumed over the design life | 9.036 | - |  |  | NEW |
| VAL-01 | Rimani et al. tug: thrusting time at 1.05 N | 339.6 | days | §6.1 item 1 (340 d own check; paper: 364 d elapsed) | 340.0 | MATCH |
| VAL-02 | Gateway PPE thrusting duty cycle | 0.8329 | - | A-17 (85%) | 0.85 | MATCH |
| VAL-03 | SMART-1 xenon predicted by the rocket equation | 79.7 | kg | §6.1 item 3 (82 kg flown) | 82.0 | MATCH |

## Details

### CALC-01: Exhaust velocity

- **Result:** 20,594 m/s (NEW)
- **Formula:** `v_e = Isp * g0`
- **Inputs:**
  - isp = 2,100 s [A-17]
  - g0 = 9.807 m/s^2 [constant]

### CALC-02: Design delta-v per leg

- **Result:** 2.640 km/s (MATCH)
- **Formula:** `dv = dv_base * (1 + margin)`
- **In MDN:** A-06, §5.2, §6.2
- **Inputs:**
  - dv_per_leg_base = 2,400 m/s [A-06]
  - dv_margin = 0.1 - [A-06]

### CALC-03: EP input power at reference thrust

- **Result:** 18.0 kW (MATCH)
- **Formula:** `P = T * v_e / (2 * eta)`
- **In MDN:** §1.2, §5.2, A-17 (~18 kW)
- **Inputs:**
  - thrust = 1.050 N [A-17]
  - Exhaust velocity = 20,594 m/s [CALC-01]
  - thruster_efficiency = 0.6 - [§6.3]

### CALC-04: Propellant mass flow

- **Result:** 51.0 mg/s (NEW)
- **Formula:** `mdot = T / v_e`
- **Inputs:**
  - thrust = 1.050 N [A-17]
  - Exhaust velocity = 20,594 m/s [CALC-01]

### CALC-05: Return-leg propellant

- **Result:** 0.8753 t (NEW)
- **Formula:** `m_p,ret = (m_dry + m_cargo,ret) * (exp(dv / v_e) - 1)`
- **Inputs:**
  - cargo_outbound = 5,000 kg [A-01]
  - cargo_return = 500.0 kg [A-02]
  - dry_mass = 5,900 kg [A-10]
  - isp = 2,100 s [A-17]
  - thrust = 1.050 N [A-17]
  - duty_cycle = 0.85 - [A-17]
  - Design delta-v per leg = 2.640 km/s [CALC-02]

### CALC-06: Outbound-leg propellant

- **Result:** 1.611 t (NEW)
- **Formula:** `m_p,out = (m_dry + m_cargo,out + m_p,ret) * (exp(dv / v_e) - 1)`
- **Note:** The tug carries its return propellant on the outbound leg (refuelled only in Earth orbit).
- **Inputs:**
  - cargo_outbound = 5,000 kg [A-01]
  - cargo_return = 500.0 kg [A-02]
  - dry_mass = 5,900 kg [A-10]
  - isp = 2,100 s [A-17]
  - thrust = 1.050 N [A-17]
  - duty_cycle = 0.85 - [A-17]
  - Design delta-v per leg = 2.640 km/s [CALC-02]
  - Return-leg propellant = 0.8753 t [CALC-05]

### CALC-07: Propellant per round trip

- **Result:** 2.486 t (MATCH)
- **Formula:** `m_p = m_p,out + m_p,ret`
- **In MDN:** A-10, §5.2, SYS-REQ-004 (~2.5 t)
- **Inputs:**
  - Outbound-leg propellant = 1.611 t [CALC-06]
  - Return-leg propellant = 0.8753 t [CALC-05]

### CALC-08: Tug mass at departure from staging orbit

- **Result:** 13.4 t (NEW)
- **Formula:** `m_0 = m_dry + m_cargo,out + m_p`
- **Inputs:**
  - cargo_outbound = 5,000 kg [A-01]
  - cargo_return = 500.0 kg [A-02]
  - dry_mass = 5,900 kg [A-10]
  - isp = 2,100 s [A-17]
  - thrust = 1.050 N [A-17]
  - duty_cycle = 0.85 - [A-17]
  - Propellant per round trip = 2.486 t [CALC-07]

### CALC-09: Outbound transfer time

- **Result:** 430.1 days (MATCH)
- **Formula:** `t_out = m_p,out / mdot / duty_cycle`
- **In MDN:** §5.2, §6.2, §6.3 (~430 d)
- **Inputs:**
  - cargo_outbound = 5,000 kg [A-01]
  - cargo_return = 500.0 kg [A-02]
  - dry_mass = 5,900 kg [A-10]
  - isp = 2,100 s [A-17]
  - thrust = 1.050 N [A-17]
  - duty_cycle = 0.85 - [A-17]
  - Outbound-leg propellant = 1.611 t [CALC-06]

### CALC-10: Return transfer time

- **Result:** 233.8 days (MATCH)
- **Formula:** `t_ret = m_p,ret / mdot / duty_cycle`
- **In MDN:** §5.2, §6.2, §6.3 (~234 d)
- **Inputs:**
  - cargo_outbound = 5,000 kg [A-01]
  - cargo_return = 500.0 kg [A-02]
  - dry_mass = 5,900 kg [A-10]
  - isp = 2,100 s [A-17]
  - thrust = 1.050 N [A-17]
  - duty_cycle = 0.85 - [A-17]
  - Return-leg propellant = 0.8753 t [CALC-05]

### CALC-11: Round-trip duration

- **Result:** 1.982 years (MATCH)
- **Formula:** `t_rt = (t_out + t_ret + t_ends) / 365.25`
- **In MDN:** §1.2, §5.2, §6.3 (~2.0 yr)
- **Inputs:**
  - Outbound transfer time = 430.1 days [CALC-09]
  - Return transfer time = 233.8 days [CALC-10]
  - end_time_per_round_trip = 60.0 days [A-18]

### CALC-12: Round trips in design life

- **Result:** 7.000 trips (MATCH)
- **Formula:** `N = floor(L / t_rt)`
- **In MDN:** §1.2, A-03, §6.3 (7)
- **Note:** Commissioning time after launch is not deducted; last return leg must fit.
- **Inputs:**
  - Round-trip duration = 1.982 years [CALC-11]
  - design_life = 15.0 years [A-03]

### CALC-13: Launch mass needed per round trip

- **Result:** 7.486 t (MATCH)
- **Formula:** `m_launch = m_cargo,out + m_p`
- **In MDN:** C-1, A-10 (~7.5 t)
- **Inputs:**
  - cargo_outbound = 5,000 kg [A-01]
  - Propellant per round trip = 2.486 t [CALC-07]

### CALC-14: Unused Ariane 64 GTO capacity per trip

- **Result:** 4.014 t (MATCH)
- **Formula:** `margin = C_GTO - m_launch`
- **In MDN:** C-1 (~4.0 t)
- **Inputs:**
  - launcher_gto_capacity = 11,500 kg [C-1]
  - Launch mass needed per round trip = 7.486 t [CALC-13]

### CALC-15: Max cargo per Ariane 64 (GTO, NRHO destination)

- **Result:** 8.531 t (MATCH)
- **Formula:** `solve m_cargo + m_p(m_cargo) = C_GTO`
- **In MDN:** A-01, A-10, D-10 (~8.5 t)
- **Inputs:**
  - cargo_outbound = 5,000 kg [A-01]
  - cargo_return = 500.0 kg [A-02]
  - dry_mass = 5,900 kg [A-10]
  - isp = 2,100 s [A-17]
  - thrust = 1.050 N [A-17]
  - duty_cycle = 0.85 - [A-17]
  - launcher_gto_capacity = 11,500 kg [C-1]

### CALC-16: Ariane 64 direct capacity to lunar transfer orbit

- **Result:** 8.600 t (MATCH)
- **Formula:** `input (direct-launch baseline for Step 4)`
- **In MDN:** D-09 (~8.6 t)
- **Note:** Includes any lunar insertion hardware; not directly comparable with CALC-15 (cargo delivered into NRHO).
- **Inputs:**
  - launcher_lto_capacity = 8,600 kg [D-09]

### CALC-17: Propellant per round trip, delta-v sensitivity case

- **Result:** 3.323 t (MATCH)
- **Formula:** `as CALC-07 with dv = dv_sens * (1 + margin)`
- **In MDN:** A-10 (3.3 t)
- **Note:** The MDN value applies the 10% margin to 3.1 km/s (3.41 km/s per leg). The MDN should say so explicitly.
- **Inputs:**
  - cargo_outbound = 5,000 kg [A-01]
  - cargo_return = 500.0 kg [A-02]
  - dry_mass = 5,900 kg [A-10]
  - isp = 2,100 s [A-17]
  - thrust = 1.050 N [A-17]
  - duty_cycle = 0.85 - [A-17]
  - dv_per_leg_sensitivity_base = 3,100 m/s [A-06]
  - dv_margin = 0.1 - [A-06]

### CALC-18: Round trips in life, delta-v sensitivity case

- **Result:** 5.000 trips (NEW)
- **Formula:** `as CALC-12 with dv = dv_sens * (1 + margin)`
- **Inputs:**
  - dv_per_leg_sensitivity_base = 3,100 m/s [A-06]

### CALC-19: Extra delta-v per leg NRHO to LLO (estimate)

- **Result:** 1.634 km/s (MATCH)
- **Formula:** `dv_extra ~ v_circ(LLO) = sqrt(mu_moon / (R_moon + h))`
- **In MDN:** §6.1 item 5, D-10 (~1.6 km/s)
- **Note:** Low-thrust spiral delta-v is approximated by the local circular speed (own estimate).
- **Inputs:**
  - llo_altitude = 100.0 km [D-10]

### CALC-20: Max cargo per Ariane 64 if the destination were LLO

- **Result:** 6.589 t (MATCH)
- **Formula:** `as CALC-15 with dv = (dv_base + dv_extra) * (1 + margin)`
- **In MDN:** §6.1 item 5, D-10 (6.6 t)
- **Inputs:**
  - Max cargo per Ariane 64 (GTO, NRHO destination) = 8.531 t [CALC-15]
  - Extra delta-v per leg NRHO to LLO (estimate) = 1.634 km/s [CALC-19]
  - dv_margin = 0.1 - [A-06]

### CALC-21: LLO orbital period

- **Result:** 117.8 min (MATCH)
- **Formula:** `T = 2 pi sqrt(r^3 / mu_moon)`
- **In MDN:** §5.1 item 3 (~118 min)
- **Inputs:**
  - llo_altitude = 100.0 km [D-10]

### CALC-22: LLO worst-case eclipse per orbit

- **Result:** 46.5 min (MATCH)
- **Formula:** `t_ecl = T * asin(R_moon / r) / pi  (beta = 0, cylindrical shadow)`
- **In MDN:** §5.1 item 3 (~46 min)
- **Inputs:**
  - llo_altitude = 100.0 km [D-10]
  - LLO orbital period = 117.8 min [CALC-21]

### CALC-23: LEO-to-GEO delta-v relative to GTO-to-NRHO

- **Result:** 2.500 - (NEW)
- **Formula:** `ratio = dv(LEO->GEO) / dv(GTO->NRHO)`
- **In MDN:** D-02, §6.1 item 4 (more than twice)
- **Note:** Supports D-02: > 2 means a LEO start needs more than twice the delta-v.
- **Inputs:**
  - leo_to_geo_dv = 6,000 m/s [D-02]
  - dv_per_leg_base = 2,400 m/s [A-06]

### CALC-24: EP power for 10 round trips in 15 years

- **Result:** 24.5 kW (MATCH)
- **Formula:** `solve t_rt(T) = years * 365.25 / trips, then P = T * v_e / (2 * eta)`
- **In MDN:** §1.2, A-03, §6.3
- **Note:** Required thrust 1.429 N. Dry mass held constant (Step 4 adds growth with power).
- **Inputs:**
  - cargo_outbound = 5,000 kg [A-01]
  - cargo_return = 500.0 kg [A-02]
  - dry_mass = 5,900 kg [A-10]
  - isp = 2,100 s [A-17]
  - thrust = 1.050 N [A-17]
  - duty_cycle = 0.85 - [A-17]
  - thruster_efficiency = 0.6 - [§6.3]
  - end_time_per_round_trip = 60.0 days [A-18]

### CALC-25: EP power for 8 round trips in 10 years

- **Result:** 30.2 kW (MATCH)
- **Formula:** `solve t_rt(T) = years * 365.25 / trips, then P = T * v_e / (2 * eta)`
- **In MDN:** §1.2, A-03, §6.3
- **Note:** Required thrust 1.758 N. Dry mass held constant (Step 4 adds growth with power).
- **Inputs:**
  - cargo_outbound = 5,000 kg [A-01]
  - cargo_return = 500.0 kg [A-02]
  - dry_mass = 5,900 kg [A-10]
  - isp = 2,100 s [A-17]
  - thrust = 1.050 N [A-17]
  - duty_cycle = 0.85 - [A-17]
  - thruster_efficiency = 0.6 - [§6.3]
  - end_time_per_round_trip = 60.0 days [A-18]

### CALC-26: Xenon throughput of one 12 kW-class thruster over rated life

- **Result:** 1.926 t (MATCH)
- **Formula:** `m_xe = (2 * eta * P / v_e) / v_e * life`
- **In MDN:** §5.2 (~2,000 kg, own estimate)
- **Inputs:**
  - thruster_unit_power = 12,000 W [§5.2]
  - thruster_unit_isp = 2,600 s [§5.2]
  - thruster_unit_efficiency = 0.63 - [§5.2]
  - thruster_rated_life = 23,000 hours [§5.2]

### CALC-27: Xenon processed over the design life

- **Result:** 17.4 t (NEW)
- **Formula:** `m_life = m_p * N`
- **Note:** Input to the Step 6 thruster-life assessment.
- **Inputs:**
  - Propellant per round trip = 2.486 t [CALC-07]
  - Round trips in design life = 7.000 trips [CALC-12]

### CALC-28: Thruster lifetimes consumed over the design life

- **Result:** 9.036 - (NEW)
- **Formula:** `n = m_life / m_xe,unit`
- **Note:** How many 12 kW-class thruster lifetimes the mission uses; drives spares/replacement (Step 6).
- **Inputs:**
  - Xenon processed over the design life = 17.4 t [CALC-27]
  - Xenon throughput of one 12 kW-class thruster over rated life = 1.926 t [CALC-26]

### VAL-01: Rimani et al. tug: thrusting time at 1.05 N

- **Result:** 339.6 days (MATCH)
- **Formula:** `t = m_0 * (1 - exp(-dv / v_e)) / mdot`
- **In MDN:** §6.1 item 1 (340 d own check; paper: 364 d elapsed)
- **Note:** 340 d thrusting inside a 364 d transfer (93%) supports the 1.05 N reference thrust.
- **Inputs:**
  - rimani_initial_mass = 13,600 kg [§6.1]
  - rimani_dv = 2,400 m/s [§6.1]
  - rimani_isp = 2,100 s [§6.1]
  - rimani_thrust = 1.050 N [§6.1]

### VAL-02: Gateway PPE thrusting duty cycle

- **Result:** 0.8329 - (MATCH)
- **Formula:** `duty = t_thrust / t_transfer`
- **In MDN:** A-17 (85%)
- **Inputs:**
  - ppe_thrusting_time = 319.0 days [§6.1]
  - ppe_transfer_time = 383.0 days [§6.1]

### VAL-03: SMART-1 xenon predicted by the rocket equation

- **Result:** 79.7 kg (MATCH)
- **Formula:** `m_p = m_0 * (1 - exp(-dv / v_e))`
- **In MDN:** §6.1 item 3 (82 kg flown)
- **Note:** Checks that the rocket-equation approach matches a flown European EP mission.
- **Inputs:**
  - smart1_launch_mass = 367.0 kg [§6.1]
  - smart1_dv = 3,700 m/s [§6.1]
  - smart1_isp = 1,540 s [§6.1]
