# Mission Definition Note: Reusable Refuellable Electric Cargo Tug (Earth Orbit to Moon)

**Document Reference:** TUG-MDN-001  
**Issue:** 2 (30 September 2026) — supersedes Issue 1 (29 September 2026)  
**Project Phase:** Phase 0 / Phase A Conceptual Architecture  
**Methodology:** Model-Based Systems Engineering (MBSE) Framing Baseline  
**Security / Proprietary Classification:** Public Domain Information Only  

---

## 1. Executive Summary & Mission Statement

### 1.1 Mission Statement
> **"Deploy an autonomous, reusable and refuellable Solar Electric Propulsion (SEP) space tug within a European 'Hub-and-Spoke' logistics architecture to transport 5,000 kg of cargo per trip from a GTO-class Earth staging orbit to a Near Rectilinear Halo Orbit (NRHO) around the Moon, repeatedly over a 15-year life, supporting sustained lunar exploration while contributing to European strategic autonomy."**

### 1.2 Core Mission Parameters
* **Primary Role:** Cislunar cargo freight carrier between an Earth staging orbit and lunar orbit, refuelled in Earth orbit between trips.
* **Launch Vehicle:** Ariane 64 (European heavy-lift launcher, CSG Kourou): 11,500 kg to GTO, 21,600 kg to LEO.
* **Earth Staging Orbit:** GTO-class orbit (cargo pick-up and refuelling). LEO is not baselined: it roughly doubles the low-thrust delta-v (see Section 6).
* **Target Delivery Orbit:** NRHO (southern $L_2$ Earth-Moon halo, period ~6.6 days), the orbit planned for Gateway. Low Lunar Orbit (LLO) is **excluded** (see D-10): descent below NRHO belongs to the lander.
* **Net Cargo Capacity:** **5,000 kg** outbound per trip (sensitivity 3,000–8,500 kg); up to **500 kg** return cargo per trip.
* **Reusability & Life Cycle:** **15-year** design life. At the reference thrust (~18 kW of electric propulsion) a round trip takes ~2 years, giving **~7 round trips**; 10 round trips need ~25 kW. The final number is an output of the Step 4 power trade.

---

## 2. Strategic Rationale & Premise: "Why a Reusable Electric Tug"

The decision to architect a reusable, refuellable electric cargo tug is not a local trade-off; it is the **mission premise**, drawn from ESA's 2040 strategy documents. The Step 4 trades decide *how* to build it, not *whether*.

```
                                  ESA POLICY BASIS
 ┌─────────────────────────────────────────┼────────────────────────────────────────┐
 │                                         │                                        │
 ▼                                         ▼                                        ▼
ESA Strategy 2040                    Explore 2040                             Technology 2040
• Objective 3.1 (Transport):         • Next-gen electric tugs:                • Very-High-Power EP
  "Hub-and-Spoke" logistics          lower costs, more frequent,              for large cargo missions (p.50).
  through launchers & tugs (p.45).   larger missions (p.16).                  • Circular Space Economy:
• Objective 3.1, Action 2a:          • Heritage synergy:                      modular, reusable systems
  in-orbit refuelling &              Earth Return Orbiter (ERO) (p.16)        beyond a single launch (p.45).
  servicing technologies (p.45).     and lunar resupply/return (p.14).        • Deep-Space Power:
• Objective 2.2:                     • Common capabilities:                   large solar arrays & power
  refillable propulsion,             rendezvous, docking, refuelling,         conditioning (p.59).
  cislunar infrastructure (p.38-41). fuel depots (p.19).
```

### 2.1 Alignment with ESA Strategy 2040 (In-Depth)
* **The "Hub-and-Spoke" Logistics Network (Objective 3.1, Action 3c, p. 45):**  
  Strategy 2040 calls for a *"scalable 'Hub-and-Spoke' network approach for space logistics through new launchers and space tugs."* In this study Ariane 64 serves the Earth-orbit "hub" (GTO-class staging orbit) and the electric tug provides the "spoke" to lunar orbit. The same objective states that *"Very high thrust chemical, high-power electric and nuclear propulsion will enable large payload crewed or cargo deep space missions."*
* **In-Orbit Servicing & Refuelling (Objective 3.1, Action 2a, p. 45):**  
  Under stimulating commercial in-orbit services in LEO, the strategy lists *"innovative technologies for in-orbit data storage, processing, manufacturing, refuelling, servicing, and debris removal."* The tug applies the refuelling element beyond LEO; reusability requires propellant replenishment as an operational routine.
* **Cislunar Infrastructure & Refillable Propulsion (Objective 2.2, p. 38–41):**  
  Directs ESA to *"provide essential infrastructure for the cislunar environment"*, fly the Argonaut lander for scientific and logistic deliveries, and names *"high-efficiency refillable propulsion systems"* as *"critical for long-distance travel and creating durable spacecraft."*
* **A Circular Space Economy (Objective 1.2, p. 29; Objective 4.1, Action 8, p. 56):**  
  Commits ESA to *"key technological enablers for the future growth markets of in-orbit servicing"* and to *"the four Rs of in-orbit servicing (remove, reuse, refurbish, recycle)."* A reusable tug replaces single-use transfer stages.

### 2.2 Alignment with ESA Explore 2040
* **Cost Reduction & Mission Cadence (Explore 2040, p. 16):**  
  *"For orbital and surface missions, the next-generation electric propulsion space tugs, with the potential to evolve towards nuclear propulsion, will help lower the costs, leading to more frequent missions carrying ever larger payloads between Mars, the Moon and Earth."*
* **Synergies with European Exploration Assets (Explore 2040, p. 14, 16):**  
  Explore 2040 notes that Orion *"has limited return mass capabilities"* and that a European vehicle flying to and from the Gateway, *"with synergies with LEO Earth return vehicles and electric tugs"*, would carry resupply and returned lunar samples (written before NASA paused Gateway in March 2026). Europe *"will fly the Earth Return Orbiter (ERO) using an electric propulsion space tug."* The Moon roadmap (Fig. 5, p. 14) places tugs in the late 2030s to 2040s.
* **Enabling Rendezvous, Docking, and Refuelling (Explore 2040, p. 19):**  
  *"Additional commonalities are for rendezvous, docking and refueling, especially for dual launches to increase the payload masses for Moon and Mars missions, including fuel depots,"* within the goal of *"European non-dependence from launch to landing."*

### 2.3 Alignment with ESA Technology Vision 2040
* **High-Power Electric Propulsion (p. 50):** Lists *"Very-High-Power Electric propulsion to enable large cargo missions"* as a key innovative-propulsion technology.
* **Circular Spacecraft Architecture (p. 45):** Calls for *"standardised interfaces and interoperability to enable in-orbit services"* and *"modular, repairable and reusable systems – no longer constrained by the need to fit everything on a single launch."*
* **Deep-Space Power (p. 59):** Lists large solar arrays and *"advanced power conditioning and distribution units"* as key technologies, and notes that solar cells are *"a pillar of European non-dependence."*

### 2.4 Existing European Heritage to Leverage
1. **SMART-1 (ESA, 2003–2006):** Flew a PPS-1350 Hall thruster from GTO to lunar orbit on ~1.2 kW, 82 kg of xenon and 3.7 km/s — the direct flight precedent for this mission profile.
2. **ESPRIT / Lunar View (Gateway):** Thales Alenia Space-led European Gateway element; OHB was contracted in 2021 for its xenon refuelling system. After NASA paused Gateway on 24 March 2026, ESA announced in June 2026 that it would slow the refuelling module while keeping its key technologies.
3. **Earth Return Orbiter (ERO):** European electric-propulsion spacecraft planned for the Mars Sample Return campaign (Explore 2040, p. 16).
4. **Electric Propulsion Industry:** European Hall-effect (e.g. Safran PPS family) and gridded-ion (e.g. QinetiQ T6 on BepiColombo) thruster lines.
5. **Automated Rendezvous & Docking (RVD):** Automated Transfer Vehicle (ATV) heritage and the European International Berthing and Docking Mechanism (IBDM).

---

## 3. Mission Objectives & Success Criteria

| ID | Objective Category | Description | Success Metric / Verification |
| :--- | :--- | :--- | :--- |
| **MO-1** | **Primary Transport** | Transport cargo from the GTO-class Earth staging orbit to NRHO. | Delivery of $5,000\text{ kg}$ net cargo to NRHO per outbound trip. |
| **MO-2** | **Return Cargo** | Return samples or waste from NRHO to the Earth staging orbit. | Up to $500\text{ kg}$ returned per trip; onward return to the ground out of scope (A-14). |
| **MO-3** | **Reusability & Refuelling** | Be refuelled in Earth orbit and reused over the design life. | 15-year design life; number of round trips set by the Step 4 power trade (~7 at the reference thrust). |
| **MO-4** | **Non-Dependence** | Use a European launcher and European-sourced critical technologies. | Ariane 6 launch; critical subsystems sourced in Europe. |
| **MO-5** | **Zero Debris Disposal** | Perform compliant end-of-life disposal at mission completion. | Heliocentric disposal after a lunar flyby, or controlled lunar impact (chosen in Step 3). |

**Figure of merit** for the study: cargo delivered to NRHO per year for a given cost, judged against a **direct Ariane 64 launch to the Moon** (D-09).

---

## 4. Stakeholder Analysis

```
                              ┌───────────────────────────────────┐
                              │       STAKEHOLDER ECOSYSTEM       │
                              └─────────────────┬─────────────────┘
                                                │
         ┌──────────────────────────────┼──────────────────────────────┐
         ▼                              ▼                              ▼
  Institutional Clients          Industrial Ecosystem            International / Commercial
  • ESA Exploration (HRE)        • Launch Provider:             • Lunar orbit customers:
    Owner of Terrae Novae,         Arianespace / ArianeGroup      landers or a future
    lunar logistics needs.         (Ariane 64 launcher).          logistics node in NRHO.
  • ESA STS (Transport):         • Spacecraft Primes:           • Commercial Cargo Owners:
    Sponsor of Hub-and-Spoke       Airbus DS, OHB SE, Thales      lunar payload providers.
    space tug network.             Alenia Space.                • In-Orbit Service Providers:
  • Space Safety Authorities:    • Subsystem Suppliers:           future propellant depot /
    Zero Debris, licensing.        EP thrusters, solar arrays,    tanker operators.
                                   refuelling & docking.
```

* **ESA Exploration Directorate (Terrae Novae):** Needs sustained, affordable lunar logistics; its lunar roadmap is being reset after NASA's Gateway pause (ministerial meeting December 2026).
* **ESA Space Transportation (STS):** Needs an in-space mobility layer that extends Ariane 6 and establishes the Hub-and-Spoke network.
* **Industrial Primes (Airbus, OHB, Thales Alenia Space):** Seek to grow in-space transportation and servicing portfolios.
* **Lunar Orbit Customers:** Landers or a future logistics node in NRHO that receive cargo; need safe approach, docking and hand-over.
* **Space Safety & Licensing Authorities:** Need debris-free operations and compliant disposal.

These map to seven Capella operational entities in Step 2: Cargo Customer, Launch Service Provider, Cislunar Cargo Transport, Ground Operations, Lunar Orbit Destination, Propellant Supplier and Space Safety Authority.

---

## 5. Mission Constraints & Baseline Assumptions

### 5.1 System Constraints
1. **Launcher Mass Envelope (C-1):**  
   * Launcher: Ariane 64 (Ariane 62 carries 4,500 kg to GTO).
   * Launch Capacity: up to **11,500 kg into GTO** or **21,600 kg into LEO**. Baseline: one Ariane 64 per round trip carries the cargo and the next trip's propellant (~7,500 kg), leaving ~4,000 kg unused — one reason the tug is judged against a direct launch (D-09).
2. **Radiation Environment (Van Allen Belts):**  
   * A GTO-class staging orbit means crossing the radiation belts on every round trip; the Gateway PPE transfer notes that its spiral phase spends the most cumulative time in the belts.
   * Array and avionics dose over the life are to be quantified in Step 3.
3. **Power Availability & Eclipses:**  
   * The thrusters cannot operate in eclipse; transfers assume an 85% thrusting duty cycle (A-17).
   * NRHO is designed to avoid eclipses; a 100 km LLO would impose up to ~46 min of eclipse per ~2-hour orbit (own calculation), one reason LLO is excluded.
4. **Docking & Interoperability Interfaces:**  
   * Standardised docking and fluid-transfer interfaces are required for cargo capture, NRHO hand-over and refuelling (Technology Vision 2040, p. 45); the specific standard is chosen in Step 3.
5. **Space Debris Mitigation (C-3):**  
   * Full compliance with ESA's Zero Debris approach; disposal delta-v reserve to be sized in Step 3.
6. **Programme & Information Constraints:**  
   * Programme decisions follow ESA ministerial councils (2025, 2028); a December 2026 ministerial meeting will reset the exploration roadmap (C-5).
   * Solar electric power only; nuclear electric is a later evolution (C-4). Public information only (C-6).

### 5.2 Baseline Mission Assumptions
* **Electric Propulsion System:** Hall-effect thrusters on xenon at $I_{sp} \approx 2,000 - 2,700\text{ s}$ (A-08). Krypton and gridded ion are Step 4 open points.
* **Reference Thrust Level:** 1.05 N at 2,100 s, **~18 kW** of electric propulsion (A-17), the operating point of the Rimani et al. reusable tug; higher power levels are traded in Step 4.
* **Propellant:** Xenon (heritage standard), ~2,500 kg per round trip (A-10). Thruster life is a flag: that is more than the ~2,000 kg one 12 kW-class thruster processes over its rated life (own estimate), so it goes to the Step 6 technology assessment.
* **Delta-V:** 2.4 km/s per leg + 10% margin = **2.64 km/s** (sensitivity 3.1 km/s); return leg equal to outbound (A-06, A-07).
* **Operational Cycle Time:** ~**2 years** per round trip at the reference thrust: ~430 days outbound, ~234 days return, ~60 days at the ends for rendezvous, refuelling, capture and hand-over (A-18).
* **Schedule:** Phase B1 ~2029–2030; operations from ~2036–2038 (A-11).

The full assumption register (A-01 to A-18) is in Appendix A.

---

## 6. Flight Mechanics: Delta-V Budget & Transfer Durations

Because electric propulsion imparts continuous, low thrust rather than impulsive burns, the tug spirals out from the GTO-class staging orbit, raising perigee first (SMART-1 strategy), before capture into the lunar three-body environment and insertion into NRHO.

```
                               CISLUNAR TRAJECTORY PHASES
  [GTO Staging] ──(Perigee Raising & Spiral-Out)──► [Lunar Capture] ──► [NRHO]
        ▲                  ΔV ≈ 2.4 km/s (+10% margin)                    │
        │                  ~430 days with 5 t cargo (reference thrust)    │
        │                                                                 │
        └──────────────(Return Spiral, ~234 days, 0.5 t)──────────────────┘

        [NRHO] ──✕──► [Low Lunar Orbit]   excluded: +~1.6 km/s per leg, eclipses
```

### 6.1 Published Literature Trajectory Data & Citations

1. **GTO to NRHO (Reusable Electric Propulsion Space Tug):**
   * **Trajectory Profile:** GTO start, SMART-1-like thrust strategy, capture into NRHO.
   * **Total $\Delta V$ Budget:** **2.4 km/s**.
   * **Transfer Duration:** **364 days** for a 13.6 t tug (5.4 t cargo, 5.9 t dry) with four Hall thrusters at 2,100 s. A 1.05 N total thrust (~18 kW) reproduces this: 340 days of thrusting (own check).
   * **Citation:** Rimani, J., Paissoni, C. A., Viola, N., Saccoccia, G., Gonzalez del Amo, J., *"Multidisciplinary mission and system design tool for a reusable electric propulsion space tug"*, Acta Astronautica 175 (2020) 387–395.

2. **Sub-GTO to NRHO (Gateway Power and Propulsion Element + HALO):**
   * **Trajectory Profile:** Start from ~200 × 33,900 km at 28.5°; 50 kW-class solar electric propulsion (~2.3 N, 2,458–2,670 s).
   * **Total $\Delta V$ Budget:** **~3.1 km/s**, more than 2,000 kg of xenon, ~50 MN·s total impulse.
   * **Transfer Duration:** **383 days**, of which 319 thrusting.
   * **Citations:**  
     * McGuire, M. L., et al., *"Application of Solar Electric Propulsion to the Low Thrust Lunar Transit of the Gateway Power and Propulsion Element"*, IEPC 2024.
     * McGuire, M. L., et al., *"Overview of the Lunar Transfer Trajectory of the Co-Manifested First Elements of NASA's Gateway"*, AAS 21-697, 2021.

3. **GTO to Lunar Orbit (SMART-1, flight data):**
   * **Trajectory Profile:** GTO (622 × 35,781 km) to polar lunar orbit with one PPS-1350 Hall thruster (67 mN, 1,540 s, ~1.2 kW).
   * **Total $\Delta V$ Budget:** **3.7 km/s** for the whole mission; 82 kg of xenon.
   * **Transfer Duration:** Launched 27 September 2003, lunar capture 15 November 2004 (~14 months).
   * **Citations:**  
     * Estublier, D., et al., *"Electric Propulsion on SMART-1: A Technology Milestone"*, ESA Bulletin 129.
     * eoPortal, *SMART-1 mission page*.

4. **LEO Staging Reference (Not Baselined):**
   * **Total $\Delta V$ Budget:** **~6 km/s** from LEO (28.5°) to GEO alone, with 20–50 kW solar electric propulsion — more than twice the GTO-to-NRHO budget.
   * **Citation:** Loghry, C., et al., *"LEO to GEO (and Beyond) Transfers using High Power Solar Electric Propulsion"*, IEPC 2017.

5. **NRHO to Low Lunar Orbit (Excluded):**
   * **Total $\Delta V$ Budget:** **+~1.6 km/s per leg** for a low-thrust spiral to a 100 km orbit (own estimate: roughly the local circular speed). With the A-01 to A-06 assumptions, the cargo one Ariane 64 can support drops from 8,500 kg to 6,600 kg.
   * **Orbit Maintenance:** NRHO costs *"on the order of 10 m/s per year, which is significantly less than lower lunar orbits"* (NASA Architecture Concept Review 2022, *"Why NRHO: The Artemis Orbit"*).

### 6.2 Consolidated Trajectory Reference Table

| Trajectory Phase | Initial State | Target State | Low-Thrust $\Delta V$ (EP Tug) | Duration at Reference Thrust (~18 kW) | Primary Published Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GTO $\to$ NRHO (Outbound, 5 t cargo)** | GTO-class | NRHO | **2.64 km/s** (2.4 + 10%) | **~430 days** | Rimani et al. (2020); McGuire et al. (2021, 2024) |
| **NRHO $\to$ GTO (Return, 0.5 t cargo)** | NRHO | GTO-class | **2.64 km/s** (assumed equal) | **~234 days** | Study assumption A-07 |
| **LEO $\to$ GEO (Reference only)** | LEO (28.5°) | GEO | **~6 km/s** | Not used | Loghry et al. (2017) |
| **NRHO $\to$ LLO (Excluded)** | NRHO | LLO (100 km) | **+~1.6 km/s** | Not used | Own estimate |

### 6.3 Round-Trip Time vs Thrust Level

Outbound carries 5 t of cargo, return 0.5 t; 85% thrusting duty cycle; 60 days per round trip at the ends (A-17, A-18). Power assumes 2,100 s and 60% thruster efficiency.

| Thrust (N) | EP Power (kW) | Outbound (days) | Return (days) | Round Trip (years) | Round Trips in 15 Years |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1.05 (reference)** | ~18 | 430 | 234 | 2.0 | **7** |
| 1.5 | ~26 | 301 | 164 | 1.4 | 10 |
| 2.0 | ~34 | 226 | 123 | 1.1 | 13 |
| 3.0 | ~51 | 151 | 82 | 0.8 | 18 |

Ten round trips in 15 years need ~25 kW; eight in 10 years need ~30 kW. These figures exclude the array and dry-mass growth that comes with more power, which Step 4 adds.

---

## 7. Concept of Operations (ConOps) Lifecycle Overview

The operational cycle is structured into eight phases and forms the baseline for the Step 2 Capella Operational Analysis:

```
                  ┌────────────────────────────────────────────────────────┐
                  ▼                                                        │
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌────────────┐ │
│   Phase 1    │    │   Phase 2    │    │   Phase 3    │    │  Phase 4   │ │
│ Launch & LEOP│───►│ Refuel &     │───►│ Outbound EP  │───►│ NRHO       │ │
│ (Ariane 64)  │    │ Cargo Capture│    │ Transfer     │    │ Delivery   │ │
└──────────────┘    └──────────────┘    └──────────────┘    └─────┬──────┘ │
                                                                  │        │
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌─────▼──────┐ │
│   Phase 8    │    │   Phase 7    │    │   Phase 6    │    │  Phase 5   │ │
│ End of Life  │◄───│ Earth Staging│◄───│ Inbound EP   │◄───│ Return     │ │
│ Disposal     │    │ Arrival      │    │ Transfer     │    │ Cargo Load │ │
└──────────────┘    └──────┬───────┘    └──────────────┘    └────────────┘ │
                           │                                               │
                           └──── (Repeats ~7x at reference thrust) ────────┘
```

1. **Phase 1: Launch and Early Orbit Phase (LEOP):** Launch of the tug on Ariane 64 into the GTO-class staging orbit. Solar array deployment, system health checks, electric propulsion commissioning.
2. **Phase 2: Refuelling & Cargo Capture:** An Ariane 64 delivers the cargo and the trip's propellant to the staging orbit (A-09). The tug is refuelled (depot, tanker or tank swap, per the Step 4 trade), then performs autonomous rendezvous and capture of the cargo.
3. **Phase 3: Outbound Low-Thrust Transfer:** Perigee raising and spiral-out through the radiation belts with thrust paused in eclipse; ~14 months at the reference thrust.
4. **Phase 4: NRHO Proximity & Delivery:** Approach to the lunar orbit customer (lander or logistics node), docking and cargo hand-over.
5. **Phase 5: Return Cargo Loading (Optional):** Collection of up to 500 kg of samples or waste.
6. **Phase 6: Inbound Low-Thrust Transfer:** Departure from NRHO and return to the staging orbit; ~8 months thanks to the lighter tug.
7. **Phase 7: Earth Staging Arrival:** Hand-over of return cargo and preparation for the next cycle. Loop back to Phase 2.
8. **Phase 8: End-of-Life Disposal:** After the last cycle, heliocentric disposal after a lunar flyby or controlled lunar impact, complying with ESA Zero Debris.

---

## 8. Requirements Flow-Down & Traceability Baseline

To seed the Capella System Analysis (Step 3), the mission statement flows down into **preliminary** top-level system requirements. Values marked TBD are set in Steps 3–4.

* **[SYS-REQ-001] Payload Delivery Capacity:** The system shall deliver a net cargo mass of at least $5,000\text{ kg}$ per trip to the Earth-Moon NRHO. *(MO-1, A-01)*
* **[SYS-REQ-002] Return Cargo:** The system shall return up to $500\text{ kg}$ of cargo per trip from NRHO to the Earth staging orbit. *(MO-2, A-02)*
* **[SYS-REQ-003] Multi-Trip Reusability:** The system shall perform repeated cislunar round trips over a design lifetime of 15 years; the minimum number of round trips is TBD by the Step 4 power trade. *(MO-3, A-03)*
* **[SYS-REQ-004] In-Orbit Refuelling:** The system shall accept in-orbit replenishment of at least one round trip's xenon load (~$2,500\text{ kg}$, TBC). *(MO-3, A-10)*
* **[SYS-REQ-005] Launcher Compatibility:** The tug shall be compatible with an Ariane 64 launch to a GTO-class orbit. *(MO-4, C-1)*
* **[SYS-REQ-006] Radiation Tolerance:** The platform avionics and solar arrays shall remain within performance after the radiation-belt crossings of all round trips over the design life (dose TBD). *(D-02)*
* **[SYS-REQ-007] Autonomous Proximity Operations:** The system shall perform autonomous rendezvous and docking with cargo in the staging orbit and with the customer in NRHO. *(MO-1)*
* **[SYS-REQ-008] European Sovereignty:** Mission-critical subsystems (electric propulsion, power processing, solar arrays, GNC software, docking and refuelling interfaces) shall be sourced from European industry. *(MO-4, C-2)*
* **[SYS-REQ-009] Disposal:** The system shall perform controlled end-of-life disposal compliant with ESA's Zero Debris approach (disposal reserve TBD). *(MO-5, C-3)*

---

## 9. Conclusion & Bridge to Step 2 (Capella Modeling)

This Mission Definition Note establishes the referenced foundation for the cislunar cargo tug project. The mission premise is anchored in **ESA Strategy 2040**, **Explore 2040** and **Technology Vision 2040**, builds on European heritage (SMART-1, ESPRIT/Lunar View, ERO) and uses flight mechanics from published, linked sources. Issue 2 corrects Issue 1's trip count, drops LLO, reflects the Gateway pause and adds a direct-launch baseline (Appendix C).

**Next Immediate Actions (Step 2 - Operational Analysis in Capella):**
1. Initialize the operational architecture model with seven operational entities: Cargo Customer, Launch Service Provider, Cislunar Cargo Transport (stands in for the tug, which stays out of the operational analysis), Ground Operations, Lunar Orbit Destination, Propellant Supplier and Space Safety Authority.
2. Formulate operational capabilities: *Provide Reusable Cislunar Cargo Logistics* (umbrella), *Deliver Cargo to Lunar Orbit*, *Return Cargo to Earth Orbit*, *Replenish Transport Propellant in Orbit* and *Dispose of Transport Assets Safely*.
3. Model the complete round-trip Operational Scenario and export the operational diagrams.

---

## Appendix A: Assumption Register

| ID | Assumption | Value | Basis |
| :--- | :--- | :--- | :--- |
| A-01 | Cargo per outbound trip | 5 t (sensitivity 3–8.5 t) | Close to the 5.4 t of Rimani et al. (2020) |
| A-02 | Return cargo per trip | Up to 0.5 t | Explore 2040, p. 14 return need |
| A-03 | Reuse and life | 15-year design life; ~7 round trips at the reference thrust; 10 need ~25 kW | Section 6.3 |
| A-04 | Earth staging orbit | GTO-class | SMART-1, Rimani et al. and Gateway PPE all start from GTO-class orbits |
| A-05 | Lunar destination | NRHO (period ~6.6 days); LLO excluded (D-10) | Rimani et al.; McGuire et al. (2021) |
| A-06 | Delta-v per leg | 2.4 km/s + 10% = 2.64 km/s; sensitivity 3.1 km/s | Rimani et al.; McGuire et al. (2024); margin is a study assumption |
| A-07 | Return-leg delta-v | Equal to outbound | Study assumption |
| A-08 | Propulsion baseline | Hall thrusters on xenon, 2,000–2,700 s | SMART-1, Rimani et al., Gateway PPE |
| A-09 | Supply per round trip | One Ariane 64 to GTO carries the cargo and the next trip's propellant | Study assumption |
| A-10 | Propellant per round trip | ~2.5 t xenon (3.3 t in the 3.1 km/s case); cargo + propellant ~7.5 t vs 11.5 t; a full launch would carry ~8.5 t of cargo | Rocket equation; 5.9 t dry mass placeholder from Rimani et al. |
| A-11 | Schedule | Phase B1 ~2029–2030; operations ~2036–2038 | Explore 2040, p. 3 and Fig. 5 |
| A-12 | Disposal | Heliocentric after a lunar flyby, or controlled lunar impact; chosen in Step 3 | Zero Debris |
| A-13 | Cost treatment | Relative cost drivers only | Public information limit |
| A-14 | Returned cargo from staging orbit to the ground | Out of scope | Explore 2040, p. 14 points to Earth return vehicles |
| A-15 | Propellant delivery route | Same Ariane 64 as the cargo, via the Propellant Supplier | Follows A-09 |
| A-16 | Ground segment in the operational model | One Ground Operations entity | Keeps the model small |
| A-17 | Reference thrust | 1.05 N at 2,100 s (~18 kW), 85% thrusting duty cycle | Rimani et al. operating point; Gateway PPE (319 of 383 days thrusting) |
| A-18 | Time at the ends of each round trip | 60 days | Study assumption |

## Appendix B: Decision Log

| ID | Decision | Why | Left Open |
| :--- | :--- | :--- | :--- |
| D-01 | Concept fixed: reusable, refuellable solar-electric tug | ESA 2040 strategy documents (Section 2) | How to build it (Step 4) |
| D-02 | Earth staging orbit = GTO-class | Less than half the low-thrust delta-v of a LEO start | LEO or higher orbits; radiation-belt dose |
| D-03 | Lunar destination = NRHO | Reachable for 2.4–3.1 km/s; designed to avoid eclipses; ~10 m/s per year to maintain | NASA paused Gateway (March 2026): NRHO is a staging orbit, not a Gateway commitment |
| D-04 | Propulsion baseline = Hall thrusters on xenon | SMART-1, Gateway PPE, ESPRIT xenon refuelling | Krypton, gridded ion (Step 4); thruster life (Step 6) |
| D-05 | 5 t out, 0.5 t back, repeated round trips over 15 years | Fits one Ariane 64 per round trip | Cargo sensitivity and trip count (Step 4) |
| D-06 | Operational analysis is solution-neutral (Cislunar Cargo Transport stands in for the tug) | Arcadia practice | Becomes the System in Step 3 |
| D-07 | "Be refuelled" becomes "Replenish transport propellant in orbit" | Stakeholder need, not a design choice | Depot, tanker or tank swap (Step 4) |
| D-08 | Returning cargo extends delivery | Return is optional per trip | — |
| D-09 | Step 4 judges the tug against a direct Ariane 64 launch to the Moon | Ariane 64 already sends ~10 t towards the Moon (Argonaut's launch mass) | Where the tug's advantage comes from |
| D-10 | LLO excluded; the tug stops at NRHO | +~1.6 km/s per leg; cargo per Ariane 64 8.5 t → 6.6 t; long eclipses | Descent belongs to the lander |

## Appendix C: Revision History

| Issue | Date | Change |
| :--- | :--- | :--- |
| 1 | 29 Sep 2026 | First release |
| 2 | 30 Sep 2026 | Self-review: GTO staging baselined instead of LEO; LLO excluded; cargo 5,000 kg; trip count made an output of Step 4 (~7 in 15 years at ~18 kW, not 5–8 in 8–10 years); Gateway pause (March 2026) reflected; direct-launch comparison added; trajectory figures and citations replaced with verified, linked sources; unsupported numerical constraints removed or set to TBD |

---

## References

1. ESA, *ESA Strategy 2040* (in-depth version).
2. ESA, *Explore2040: The European Exploration Strategy*, 2024.
3. ESA, *Technology Vision 2040*.
4. J. Rimani, C.A. Paissoni, N. Viola, G. Saccoccia, J. Gonzalez del Amo, [Multidisciplinary mission and system design tool for a reusable electric propulsion space tug](https://iris.polito.it/retrieve/handle/11583/2837701/379000), Acta Astronautica 175 (2020) 387–395.
5. M. McGuire et al., [Application of Solar Electric Propulsion to the Low Thrust Lunar Transit of the Gateway Power and Propulsion Element](https://ntrs.nasa.gov/api/citations/20240007012/downloads/IEPC24_358_v2.pdf), IEPC 2024.
6. M. McGuire et al., [Overview of the Lunar Transfer Trajectory of the Co-Manifested First Elements of NASA's Gateway](https://ntrs.nasa.gov/api/citations/20210019116/downloads/AAS_McGuire_LunarTransferTraj_v8.pdf), AAS 21-697, 2021.
7. D. Estublier et al., [Electric Propulsion on SMART-1: A Technology Milestone](https://www.esa.int/esapub/bulletin/bulletin129/bul129e_estublier.pdf), ESA Bulletin 129.
8. eoPortal, [SMART-1 mission page](https://www.eoportal.org/satellite-missions/smart-1).
9. C. Loghry et al., [LEO to GEO (and Beyond) Transfers using High Power Solar Electric Propulsion](https://ntrs.nasa.gov/api/citations/20180000689/downloads/20180000689.pdf), IEPC 2017.
10. ArianeGroup, [Number crunching: Ariane 62 and Ariane 64](https://www.ariane.group/en/news/number-crunching-ariane-6-ariane-62-and-ariane-64/).
11. OHB, [OHB and Thales Alenia Space sign contract for refuelling system for Lunar Gateway](https://www.ohb.de/en/news/2021/ohb-and-thales-alenia-space-sign-contract-for-refuelling-system-for-lunar-gateway), 2021.
12. The Register, [NASA abandons Lunar Gateway plans for base on Lunar surface](https://www.theregister.com/2026/03/24/goodbye_lunar_gateway_nasa_ditches/), 24 March 2026.
13. European Spaceflight, [ESA Details Next Steps for Agency's Gateway Contributions](https://europeanspaceflight.com/esa-details-next-steps-for-agencys-gateway-contributions/), 23 June 2026.
14. NASA Architecture Concept Review 2022, [Why NRHO: The Artemis Orbit](https://www.lpi.usra.edu/lunar/artemis/resources/WhitePaper_2023_WhyNRHA-TheArtemisOrbit.pdf).
15. Wikipedia, [Argonaut (lunar lander)](https://en.wikipedia.org/wiki/Argonaut_(lunar_lander)).
16. R. Shastry et al., [12-kW AEPS Hall Current Thruster Qualification and Production Status](https://ntrs.nasa.gov/api/citations/20240006249/downloads/AEPS%20Status%20IEPC%202024%20v7.pdf), IEPC 2024 (23,000 h life target; xenon-per-thruster figure is an own estimate).
