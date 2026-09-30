# Mission Definition Note: Reusable, Refuellable Electric Cargo Tug (Earth Orbit to Moon)

| | |
| --- | --- |
| **Document** | TUG-MDN-001, Issue 2 |
| **Date** | 30 September 2026 |
| **Phase** | Phase 0 / A-style portfolio study, step 1 of 7 |
| **Author** | Robert |
| **Information basis** | Public sources only; every assumption carries an ID |

**Summary.** A reusable, refuellable solar-electric tug collects 5 t of cargo that Ariane 64 places in a GTO-class orbit, delivers it to a near-rectilinear halo orbit (NRHO) around the Moon, brings back up to 0.5 t, and is refuelled in Earth orbit for repeated round trips over a 15-year life from the late 2030s. At the reference thrust that is about seven round trips; the power trade (step 4) decides whether more power buys more.

---

## 1. Why a reusable electric tug

ESA's 2040 strategy documents already call for this vehicle, so the concept is the premise of the study, not a trade. The trades (step 4) decide how to build it.

| Premise | What ESA says | Source |
| --- | --- | --- |
| Tugs are part of Europe's logistics network | "Develop a scalable 'Hub-and-Spoke' network approach for space logistics through new launchers and space tugs." | Strategy 2040, Obj. 3.1, action 3c, p. 45 |
| Electric propulsion is the route for cargo | "Very high thrust chemical, high-power electric and nuclear propulsion will enable large payload crewed or cargo deep space missions." Also: "very high-power electric propulsion to support large cargo missions" | Strategy 2040, Obj. 3.1, p. 45; Obj. 4.1, p. 55; Technology Vision 2040, p. 50 |
| Electric tugs lower cost and raise cadence | "next-generation electric propulsion space tugs [...] will help lower the costs, leading to more frequent missions carrying ever larger payloads between Mars, the Moon and Earth." | Explore2040, p. 16 |
| Refuelling and reuse | "high-efficiency refillable propulsion systems" are "critical for long-distance travel and creating durable spacecraft"; "rendezvous, docking and refueling [...] including fuel depots" | Strategy 2040, Obj. 2.2, p. 40; Explore2040, p. 19 |
| Circular economy in orbit | "Develop key technological enablers for the future growth markets of in-orbit servicing, in-orbit assembly, in-orbit manufacturing and in-orbit recycling" | Strategy 2040, Obj. 1.2, p. 29 |
| Lunar resupply and return cargo | Orion "has limited return mass capabilities"; a European vehicle to and from the Gateway, "with synergies with [...] electric tugs", would carry Gateway resupply and returned lunar samples (written before NASA paused Gateway in March 2026) | Explore2040, p. 14 |
| Non-dependence | "European non-dependence from launch to landing" | Explore2040, p. 19 |
| Timing | The Moon roadmap places tugs in the late 2030s to 2040s; "Incremental deployment of space transportation solutions from 2030 onwards" | Explore2040, Fig. 5, p. 14; Strategy 2040, Obj. 3.1, p. 45 |

European heritage to build on: SMART-1 flew a Hall thruster from GTO to the Moon in 2003–04; OHB was contracted in 2021 for the xenon refuelling system of Gateway's electric propulsion (ESPRIT, now Lunar View), which ESA slowed down in June 2026 after NASA paused Gateway; the Earth Return Orbiter uses an electric propulsion tug (Explore2040, p. 16).

Page numbers are the printed page numbers of each document.

## 2. Objectives

The study's figure of merit is cargo delivered to NRHO per year for a given cost; the step 4 power trade is judged on it.

| ID | Objective | Traces to |
| --- | --- | --- |
| MO-1 | Deliver 5 t of cargo per trip from the Earth staging orbit to NRHO | Hub-and-Spoke; lunar resupply |
| MO-2 | Return up to 0.5 t per trip from NRHO to the Earth staging orbit (samples, waste) | Explore2040 p. 14 return need |
| MO-3 | Be refuelled in orbit and reused over a 15-year design life; the number of round trips comes from the step 4 power trade | Refillable propulsion; circular economy |
| MO-4 | Use a European launcher and European-sourced critical technologies | Non-dependence |
| MO-5 | Leave no debris: controlled disposal at end of life | Zero Debris |

## 3. Stakeholders

Five stakeholders interact with the tug in operation and become Capella operational entities in step 2, alongside the space safety authority; the rest shape requirements without an operational interface.

| Stakeholder | Main need | Capella entity (step 2) |
| --- | --- | --- |
| Cargo customer (ESA programmes, international partners, commercial lunar payload providers) | Reliable, affordable delivery; standard cargo interface | Cargo Customer |
| Launch service (Ariane 6) | Clear cargo and propellant delivery orbit and mass | Launch Service Provider |
| Ground operations (control centre, ground stations) | Autonomous tug, low operator workload | Ground Operations |
| Lunar orbit customer (lander or future logistics node) | Safe approach and docking; cargo hand-over | Lunar Orbit Destination |
| Refuelling provider (depot or tanker, per step 4) | Standard refuelling interface | Propellant Supplier |
| ESA (Exploration and Space Transportation directorates) | Strategic autonomy; low cost per kg delivered | — (sponsor) |
| European industry (electric propulsion, solar arrays, docking) | Technology roadmap and production volume | — |
| Space safety and licensing authorities | Debris-free operations and disposal | Space Safety Authority |

## 4. Constraints

Constraints are imposed from outside the study and are not traded.

| ID | Constraint | Source |
| --- | --- | --- |
| C-1 | Launch on Ariane 6: Ariane 64 carries 11.5 t to GTO or 21.6 t to LEO; Ariane 62 carries 4.5 t to GTO | ArianeGroup |
| C-2 | Critical technologies sourced in Europe | Explore2040, p. 19 |
| C-3 | Comply with ESA's Zero Debris approach, including disposal | Strategy 2040, Obj. 1.2, p. 28–29 |
| C-4 | Solar electric power only; nuclear electric is a later evolution | Explore2040, p. 16 |
| C-5 | Programme decisions follow ESA ministerial councils (2025, 2028); a December 2026 ministerial meeting will reset the exploration roadmap after NASA's Gateway pause | Explore2040, p. 3; European Spaceflight, June 2026 |
| C-6 | Study uses public information only | Study rule |

## 5. Assumptions

One Ariane 64 launch per round trip can carry the cargo and the next trip's propellant with about 4 t to spare (A-10); that unused capacity is one reason step 4 compares against launching direct (D-09). The other values are baselines that later steps may revise.

| ID | Assumption | Value | Basis |
| --- | --- | --- | --- |
| A-01 | Cargo per outbound trip | 5 t (sensitivity 3–8.5 t) | Close to the 5.4 t of Rimani et al. (2020); fits A-10 |
| A-02 | Return cargo per trip | Up to 0.5 t | Study assumption; return need in Explore2040, p. 14 |
| A-03 | Reuse and life | 15-year design life; about 7 round trips at the reference thrust (A-17); 10 need about 25 kW | Study assumption; timing check in section 8 |
| A-04 | Earth staging orbit (cargo pick-up and refuelling) | GTO-class orbit | SMART-1, Rimani et al. and Gateway PPE all start from GTO-class orbits; Ariane 64 GTO performance (C-1) |
| A-05 | Lunar destination | NRHO, the orbit planned for Gateway (period about 6.6 days); low lunar orbit excluded (D-10) | Rimani et al.; McGuire et al. (2021) |
| A-06 | Delta-v per leg | 2.4 km/s + 10% margin = 2.64 km/s; sensitivity case 3.1 km/s | Rimani et al. (GTO to NRHO); Gateway PPE (McGuire et al., 2024); margin is a study assumption |
| A-07 | Return-leg delta-v | Equal to outbound | Study assumption |
| A-08 | Propulsion baseline | Hall-effect thrusters on xenon, specific impulse 2,000–2,700 s | SMART-1, Rimani et al. (2,100 s), Gateway PPE (2,458–2,670 s) |
| A-09 | Supply per round trip | One Ariane 64 to GTO carries the cargo and the next trip's propellant; how it is transferred is the step 4 refuelling trade | Study assumption |
| A-10 | Propellant per round trip | About 2.5 t xenon (3.3 t in the 3.1 km/s case), so cargo plus propellant is about 7.5 t (8.3 t) against 11.5 t; a full launch would carry about 8.5 t of cargo | Rocket equation with A-01, A-02, A-06, specific impulse 2,100 s and Rimani et al.'s 5.9 t dry mass as a placeholder until step 4 |
| A-11 | Schedule | Phase B1 about 2029–2030 after the 2028 ministerial; operations from about 2036–2038 | Explore2040, p. 3 and Fig. 5 |
| A-12 | Disposal | Heliocentric disposal after a lunar flyby, or controlled lunar impact; chosen in step 3 | Zero Debris (C-3) |
| A-13 | Cost treatment | Relative cost drivers only; no absolute costs | Public information limit (C-6) |
| A-14 | Returned cargo from Earth staging orbit to the ground | Out of scope | Step 2; Explore2040, p. 14 points to Earth return vehicles |
| A-15 | Propellant delivery route | Same Ariane 64 as the cargo, via the Propellant Supplier | Step 2; follows A-09 |
| A-16 | Ground segment in the operational model | One Ground Operations entity for planning and control | Step 2; split in step 3 if needed |
| A-17 | Reference thrust for timing | 1.05 N at 2,100 s (about 18 kW of electric propulsion), thrusting 85% of transfer time | Rimani et al. operating point, which reproduces their 364-day transfer; duty cycle from Gateway PPE (319 of 383 days thrusting) |
| A-18 | Time at the ends of each round trip | 60 days in total for rendezvous, refuelling, cargo capture and hand-over | Study assumption |

## 6. Reference transfer data

Published low-thrust transfers from GTO-class orbits to the Moon need 2.4–3.1 km/s and take about a year; this sets A-06 and the starting point for the step 4 power trade.

| Mission or study | From → to | Propulsion and power | Mass | Delta-v | Transfer time |
| --- | --- | --- | --- | --- | --- |
| [Gateway PPE + HALO](https://ntrs.nasa.gov/api/citations/20240007012/downloads/IEPC24_358_v2.pdf) (NASA, planned) | About 200 × 33,900 km, 28.5° → NRHO | 50 kW-class solar electric; about 2.3 N; 2,458–2,670 s | About 16 t average (implied: 50 MN·s impulse ÷ 3.1 km/s) | About 3.1 km/s; more than 2,000 kg xenon | [383 days, 319 of them thrusting](https://ntrs.nasa.gov/api/citations/20210019116/downloads/AAS_McGuire_LunarTransferTraj_v8.pdf) |
| [Reusable EP space tug](https://iris.polito.it/retrieve/handle/11583/2837701/379000) (Rimani et al., 2020, with ESA ESTEC) | GTO → NRHO | Four Hall thrusters, 2,100 s (1.05 N in total at about 18 kW; the 91 kW listed for the propulsion subsystem is unexplained) | 13.6 t, of which 5.4 t cargo; 5.9 t dry | 2.4 km/s | 364 days |
| [SMART-1](https://www.esa.int/esapub/bulletin/bulletin129/bul129e_estublier.pdf) (ESA, flown 2003–06) | GTO (622 × 35,781 km) → polar lunar orbit | One Hall thruster, up to 1.2 kW, 67 mN, 1,540 s | 370 kg | 3.7 km/s for the whole mission; 82 kg xenon | About 14 months to lunar capture (launched 27 Sep 2003, [captured 15 Nov 2004](https://www.eoportal.org/satellite-missions/smart-1)) |
| [High-power SEP study](https://ntrs.nasa.gov/api/citations/20180000689/downloads/20180000689.pdf) (Loghry et al., 2017) | LEO (28.5°) → GEO | 20–50 kW solar electric | — | About 6 km/s | — |

Two readings carry into later steps. A LEO start needs about 6 km/s just to reach GEO, against 2.4–3.1 km/s from GTO all the way to NRHO, which is why A-04 baselines GTO. The flown and planned transfers averaged about 0.8–2 × 10⁻⁴ m/s² of acceleration, so halving the trip time needs roughly twice the thrust, and power, per kilogram: the core of the step 4 trade.

Check on Rimani et al.: 1.05 N of total thrust on their 13.6 t tug needs 340 days of thrusting for 2.4 km/s, consistent with the 364 days they report. Their tug therefore runs at about 18 kW of electric propulsion, and that operating point is the reference thrust A-17 uses.

## 7. Decision log

| ID | Decision | Why | Left open |
| --- | --- | --- | --- |
| D-01 | Concept fixed: reusable, refuellable solar-electric tug | Called for by Strategy 2040 and Explore2040 (section 1) | How to build it (step 4) |
| D-02 | Earth staging orbit = GTO-class | Less than half the low-thrust delta-v of a LEO start; matches Ariane 64 GTO performance and all three reference missions | LEO or higher orbits as step 4 open point, including radiation-belt dose on the arrays at each crossing |
| D-03 | Lunar destination = NRHO | Reachable from GTO for 2.4–3.1 km/s with low thrust; designed to avoid eclipses; about 10 m/s per year to maintain; used by the reference studies | None for this study. NASA paused Gateway in March 2026, so NRHO is a staging orbit for landers or a future logistics node, not a Gateway commitment |
| D-04 | Propulsion baseline = Hall thrusters on xenon | Flight heritage (SMART-1), Gateway PPE, ESPRIT xenon refuelling | Krypton and gridded ion as step 4 open points; thruster life for step 6 (about 2.5 t of xenon per round trip against roughly 2 t per 12 kW-class thruster) |
| D-05 | Cargo 5 t out, 0.5 t back, repeated round trips over 15 years | Fits one Ariane 64 per round trip with margin (A-10); comparable to the reference tug | Cargo sensitivity 3–8.5 t and the number of round trips, both in step 4 |
| D-06 | Operational analysis is solution-neutral: the tug is replaced by the entity Cislunar Cargo Transport | Arcadia practice; keeps the need independent of the design | The entity becomes the System in step 3 |
| D-07 | "Be refuelled" becomes "Replenish transport propellant in orbit"; Propellant Supplier kept generic | Stakeholder need, not a design choice | Depot, tanker or tank swap (step 4) |
| D-08 | Returning cargo extends delivery (OC-2 extends OC-1) | Return cargo is optional per trip (A-02) | None |
| D-09 | Step 4 judges the tug against a direct Ariane 64 launch to the Moon | Ariane 64 already sends about 10 t towards the Moon (Argonaut's launch mass); a tug that uses one Ariane 64 to move 5 t in a year has to beat that on cost per kg | Where the tug's advantage comes from: fuller or cheaper launches to GTO, reuse, or return cargo |
| D-10 | Low lunar orbit excluded; the tug stops at NRHO | Spiralling down to a 100 km orbit adds about 1.6 km/s per leg (own estimate), cutting cargo per Ariane 64 from 8.5 t to 6.6 t; eclipses of up to 46 min every 2-hour orbit starve solar electric propulsion; lower orbits cost far more than 10 m/s per year to maintain | Descent below NRHO belongs to the lander |

## 8. Review, 30 September 2026

Issue 1 over-committed in four places: ten round trips did not fit the 15-year life, low lunar orbit was offered as an equal alternative, Gateway was treated as live, and the baseline was never compared with launching direct. The fixes are in the sections above and in D-09 and D-10.

| # | Finding | Fix |
| --- | --- | --- |
| R1 | At the reference thrust a round trip takes about 2 years, so 15 years allows about 7 trips, not 10 | MO-3 and A-03 no longer fix the count; A-17 and A-18 state the timing basis; step 4 sets the count through the power trade |
| R2 | Low lunar orbit was listed as an open alternative, as if it cost the same as NRHO | Excluded (D-10): about 1.6 km/s more per leg, 6.6 t instead of 8.5 t of cargo per Ariane 64, 46-minute eclipses |
| R3 | NASA paused Gateway on 24 March 2026; in June ESA slowed its refuelling module (formerly ESPRIT, now Lunar View) | NRHO kept as an orbit, not a customer (D-03); heritage line and C-5 updated |
| R4 | No comparison with launching cargo directly: Ariane 64 already sends about 10 t towards the Moon | Direct Ariane 64 launch becomes the step 4 reference (D-09) |
| R5 | Rimani et al.'s power figures were called irreconcilable | Resolved: 1.05 N in total at about 18 kW reproduces their transfer (section 6) |
| R6 | About 2.5 t of xenon per round trip, 17 t over 7 trips, against roughly 2 t per 12 kW-class thruster | Thruster life flagged for step 6 (D-04) |
| R7 | The stakeholder table still used step 1's actor names | Aligned with the step 2 entities |

**Round-trip time against thrust.** Outbound carries 5 t of cargo, return carries 0.5 t; each includes an 85% thrusting duty cycle, and every round trip adds 60 days at the two ends (A-17, A-18).

| Thrust (N) | Electric propulsion power (kW) | Outbound (days) | Return (days) | Round trip (years) | Round trips in 15 years |
| --- | --- | --- | --- | --- | --- |
| 1.05 (reference) | About 18 | 430 | 234 | 2.0 | 7 |
| 1.5 | About 26 | 301 | 164 | 1.4 | 10 |
| 2.0 | About 34 | 226 | 123 | 1.1 | 13 |
| 3.0 | About 51 | 151 | 82 | 0.8 | 18 |

Ten round trips in 15 years need about 25 kW; eight in 10 years need about 30 kW. Power assumes 2,100 s and 60% thruster efficiency (study assumption); step 4 adds the array and dry-mass growth that comes with more power, which these figures leave out.

## Sources

- ESA, *ESA Strategy 2040* (in-depth version)
- ESA, *Explore2040: The European Exploration Strategy*, 2024
- ESA, *Technology Vision 2040*
- J. Rimani, C.A. Paissoni, N. Viola, G. Saccoccia, J. Gonzalez del Amo, [Multidisciplinary mission and system design tool for a reusable electric propulsion space tug](https://iris.polito.it/retrieve/handle/11583/2837701/379000), Acta Astronautica 175 (2020) 387–395
- M. McGuire et al., [Application of Solar Electric Propulsion to the Low Thrust Lunar Transit of the Gateway Power and Propulsion Element](https://ntrs.nasa.gov/api/citations/20240007012/downloads/IEPC24_358_v2.pdf), IEPC 2024
- M. McGuire et al., [Overview of the Lunar Transfer Trajectory of the Co-Manifested First Elements of NASA's Gateway](https://ntrs.nasa.gov/api/citations/20210019116/downloads/AAS_McGuire_LunarTransferTraj_v8.pdf), AAS 21-697, 2021
- D. Estublier et al., [Electric Propulsion on SMART-1: A Technology Milestone](https://www.esa.int/esapub/bulletin/bulletin129/bul129e_estublier.pdf), ESA Bulletin 129
- eoPortal, [SMART-1 mission page](https://www.eoportal.org/satellite-missions/smart-1)
- C. Loghry et al., [LEO to GEO (and Beyond) Transfers using High Power Solar Electric Propulsion](https://ntrs.nasa.gov/api/citations/20180000689/downloads/20180000689.pdf), IEPC 2017
- ArianeGroup, [Number crunching: Ariane 62 and Ariane 64](https://www.ariane.group/en/news/number-crunching-ariane-6-ariane-62-and-ariane-64/)
- OHB, [OHB and Thales Alenia Space sign contract for refuelling system for Lunar Gateway](https://www.ohb.de/en/news/2021/ohb-and-thales-alenia-space-sign-contract-for-refuelling-system-for-lunar-gateway), 2021
- The Register, [NASA abandons Lunar Gateway plans for base on Lunar surface](https://www.theregister.com/2026/03/24/goodbye_lunar_gateway_nasa_ditches/), 24 March 2026
- European Spaceflight, [ESA Details Next Steps for Agency's Gateway Contributions](https://europeanspaceflight.com/esa-details-next-steps-for-agencys-gateway-contributions/), 23 June 2026
- NASA Architecture Concept Review 2022, [Why NRHO: The Artemis Orbit](https://www.lpi.usra.edu/lunar/artemis/resources/WhitePaper_2023_WhyNRHA-TheArtemisOrbit.pdf)
- Wikipedia, [Argonaut (lunar lander)](https://en.wikipedia.org/wiki/Argonaut_(lunar_lander)) — 10 t launch mass on Ariane 64
- R. Shastry et al., [12-kW AEPS Hall Current Thruster Qualification and Production Status](https://ntrs.nasa.gov/api/citations/20240006249/downloads/AEPS%20Status%20IEPC%202024%20v7.pdf), IEPC 2024 — 23,000 h life target; the xenon-per-thruster figure is an own estimate from it

## Revision history

| Issue | Date | Change |
| --- | --- | --- |
| 1 | 29 Sep 2026 | First release |
| 2 | 30 Sep 2026 | Self-review (section 8): round-trip count made an output of step 4; low lunar orbit excluded; Gateway pause reflected; direct-launch baseline added; unverifiable citations and trajectory figures removed |
