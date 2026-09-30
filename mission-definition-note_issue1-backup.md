# Mission Definition Note: Reusable Refuellable Electric Cargo Tug (Earth Orbit to Moon)

**Document Reference:** TUG-MDN-001  
**Project Phase:** Phase 0 / Phase A Conceptual Architecture  
**Methodology:** Model-Based Systems Engineering (MBSE) Framing Baseline  
**Security / Proprietary Classification:** Public Domain Information Only  

---

## 1. Executive Summary & Mission Statement

### 1.1 Mission Statement
> **"Deploy an autonomous, reusable, and refuellable high-power Solar Electric Propulsion (SEP) space tug within a European 'Hub-and-Spoke' logistics architecture to reliably and cost-effectively transport up to 4,500 kg of cargo per trip from Earth staging orbits to lunar orbit (Near Rectilinear Halo Orbit / Gateway and Low Lunar Orbit), supporting sustained international exploration while guaranteeing European non-dependence."**

### 1.2 Core Mission Parameters
* **Primary Role:** Trans-lunar cargo freight carrier, orbital logistics transfer, and in-space servicing node.
* **Launch Vehicle:** Ariane 64 (heavy-lift European launcher, CSG Kourou).
* **Launch Staging Orbit:** Low Earth Orbit (LEO, circular ~350–500 km, $i = 5.2^\circ$ or $28.5^\circ$) or Geostationary Transfer Orbit (GTO).
* **Target Delivery Orbit:** Near Rectilinear Halo Orbit (NRHO, southern $L_2$ Earth-Moon halo, 9:2 orbital resonance, perilune ~3,200 km, apolune ~70,000 km, period ~6.5 days) and Low Lunar Orbit (LLO, circular ~100 km).
* **Net Cargo Capacity:** 4,000 to 5,000 kg (nominal baseline: **4,500 kg**) of pressurized/unpressurized logistics or lunar modules per outbound leg.
* **Reusability & Life Cycle:** Designed for a multi-trip service life of **8 to 10 years**, accomplishing **5 to 8 complete round-trip cycles** via in-orbit refuelling.

---

## 2. Strategic Rationale & Premise: "Why a Reusable Electric Tug"

The decision to architect a reusable, refuellable electric cargo tug is not a local trade-off; it is the fundamental **mission premise** mandated by European space policy and industrial strategies toward 2040. 

```
                                  ESA POLICY MANDATES
 ┌─────────────────────────────────────────┼────────────────────────────────────────┐
 │                                         │                                        │
 ▼                                         ▼                                        ▼
ESA Strategy 2040                    Explore 2040                             Technology 2040
• Objective 3.1 (Transport):         • Next-gen electric tugs:                • Very-High-Power EP
  "Hub-and-Spoke" logistics,           Lower costs, fly more/larger             for large cargo missions (p.50).
  reusable in-space tugs (p.23).       missions to Moon/Mars (p.16).          • Circular Space Economy:
• Strategic Action 2a:               • Heritage synergy:                      "Four Rs" in orbit, modular &
  Commercial refuelling &              Earth Return Orbiter (ERO) (p.16)        repairable architectures (p.45).
  servicing in orbit (p.23).           and Gateway resupply (p.14).           • Deep-Space Solar Power:
• Objective 2.2:                     • Common capabilities:                     High-efficiency arrays &
  Non-dependence for cislunar          In-orbit refuelling & fuel               power distribution (p.59).
  logistics & Gateway (p.20-21).       depots for dual launch (p.19).
```

### 2.1 Alignment with ESA Strategy 2040 (In-Depth)
* **The "Hub-and-Spoke" Logistics Network (Objective 3.1, Action 3c, p. 23):**  
  Strategy 2040 explicitly identifies space transportation as the backbone of European sovereignty, calling for a transition from one-way expendable missions to a *"scalable 'Hub-and-Spoke' network approach for space logistics through new launchers and space tugs."* Ariane 6 acts as the high-capacity launcher to the LEO "hub," while the electric tug provides the long-range "spoke" to cislunar destinations.
* **In-Orbit Servicing & Refuelling (Objective 3.1, Action 2a, p. 23):**  
  Mandates the stimulation of commercial in-orbit operations, prioritizing *"innovative technologies for in-orbit data storage, processing, manufacturing, refuelling, servicing, and debris removal."* Reusability requires propellant replenishment as an operational routine.
* **Autonomous Cislunar Mobility & Gateway Presence (Objective 2.2, p. 20–21):**  
  Directs Europe to provide sovereign cislunar infrastructure, resupply the lunar Gateway, and establish synergies with the Argonaut lunar lander and European Service Modules (ESMs) while maintaining independent access free from non-European bottlenecks.
* **A Circular Space Economy (Objective 4.1, Action 8, p. 29):**  
  Commits ESA to a net-zero debris footprint by instituting the *"four Rs of in-orbit servicing (remove, reuse, refurbish, recycle)."* A reusable tug completely eliminates the reckless paradigm of expending upper stages and multi-ton propulsion modules after a single cislunar transfer.

### 2.2 Alignment with ESA Explore 2040
* **Cost Reduction & Mission Cadence (Explore 2040, p. 16):**  
  States unequivocally: *"For orbital and surface missions, the next-generation electric propulsion space tugs, with the potential to evolve towards nuclear propulsion, will help lower the costs, leading to more frequent missions carrying ever larger payloads between Mars, the Moon and Earth."*
* **Synergies with European Exploration Assets (Explore 2040, p. 14, 16):**  
  Builds directly upon European investments in the **Earth Return Orbiter (ERO)**—Europe's flagship high-power electric propulsion tug for the Mars Sample Return campaign—and creates operational links with LEO cargo return vehicles and Gateway resupply needs.
* **Enabling Rendezvous, Docking, and Refuelling (Explore 2040, p. 19):**  
  Highlights common capabilities across destinations, specifying that *"rendezvous, docking and refueling, especially for dual launches to increase the payload masses for Moon and Mars missions, including fuel depots"* are essential enablers of European non-dependence.

### 2.3 Alignment with ESA Technology Vision 2040
* **High-Power Electric Propulsion (p. 50):** Classifies *"Very-High-Power Electric propulsion to enable large cargo missions"* as a primary strategic technology to ensure European industrial leadership.
* **Circular Spacecraft Architecture (p. 45):** Advocates for systems *"no longer constrained by the need to fit everything on a single launch"* through modularity, standard interfaces, and in-space lifetime extension.
* **Advanced Deep-Space Power (p. 59):** Demands next-generation multi-junction photovoltaic arrays and advanced power conditioning units (PCDUs) capable of sustained high-voltage EP operations.

### 2.4 Existing European Heritage to Leverage
The tug concept directly capitalizes on established and ongoing European industrial capabilities:
1. **ESPRIT (European System Providing Refuelling, Infrastructure and Telecommunications):** Thales Alenia Space / ESA element for Gateway, establishing European leadership in pressurized xenon and chemical propellant transfer systems in microgravity.
2. **Earth Return Orbiter (ERO):** Airbus Defence and Space prime development of a high-power (~40 kW array, ~20 kW EP) deep-space electric propulsion carrier.
3. **Electric Propulsion Heritage:** Safran Snecma PPS-1350 / PPS-5000 Hall thrusters (SMART-1 heritage; telecom satellite all-electric orbit raising), QinetiQ T6/T5 gridded ion thrusters (BepiColombo), and Sitael HT-series.
4. **Automated Rendezvous & Docking (RVD):** Automated Transfer Vehicle (ATV) optical GNC and docking sensors, Columbus / Bartolomeo berthing interfaces, and European active docking mechanisms (IBDM - International Berthing and Docking Mechanism).

---

## 3. Mission Objectives & Success Criteria

| ID | Objective Category | Description | Success Metric / Verification |
| :--- | :--- | :--- | :--- |
| **OBJ-01** | **Primary Transport** | Transport discrete cargo modules from Earth staging orbit to Lunar Gateway NRHO or Low Lunar Orbit (LLO). | Delivery of $\ge 4,500\text{ kg}$ net cargo to NRHO within specified transfer window. |
| **OBJ-02** | **Reusability** | Return tug from lunar orbit to Earth staging orbit without cargo for subsequent operational cycles. | Successful return insertion and Earth orbit phasing; minimum 5 round trips. |
| **OBJ-03** | **In-Orbit Refuelling** | Autonomous fluid and electrical coupling to receive propellant (Xenon) from a dedicated depot or tanker. | Replenishment of operational propellant load with $<1\%$ leakage; verified via telemetry. |
| **OBJ-04** | **Autonomous RVD** | Perform autonomous rendezvous, proximity operations, and docking (RVD) with cargo modules and Gateway. | Compliant with ESA/NASA safe rendezvous corridor standards; zero collision incidents. |
| **OBJ-05** | **Zero Debris Disposal** | Perform compliant end-of-life disposal at mission completion. | Controlled de-orbit into Earth ocean or targeted lunar surface disposal / heliocentric graveyard. |
| **OBJ-06** | **Non-Dependence** | Maintain European strategic sovereignty across all critical subsystems. | 100% ITAR-free design utilizing European supply chain for propulsion, power, and avionics. |

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
  • ESA Exploration (HRE)        • Launch Provider:             • NASA / Artemis Gateway
    Owner of Terrae Novae,         Arianespace / ArianeGroup      Logistics customer for
    Gateway logistics resupply.    (Ariane 64 launcher).          NRHO cargo delivery.
  • ESA STS (Transport):         • Spacecraft Primes:           • Commercial Cargo Owners:
    Sponsor of Hub-and-Spoke       Airbus DS, OHB SE, Thales      Commercial payloads, lunar
    space tug network.             Alenia Space.                  landers (Argonaut cargo).
  • European Commission:         • Subsystem Suppliers:         • In-Orbit Service Providers:
    EU Space Programme, Horizon    Safran / QinetiQ (Thrusters),  Future commercial propellant
    Europe non-dependence.         TAS (Refuelling/ESPRIT).       depot / tanker operators.
```

* **ESA Exploration Directorate (Terrae Novae):** Requires sustained, affordable logistics to maintain Europe’s seat at the lunar Gateway table and resupply surface expeditions via the Argonaut lunar lander.
* **ESA Space Transportation (STS):** Requires a complementary in-space mobility layer that maximizes Ariane 6 market relevance and establishes the Hub-and-Spoke infrastructure.
* **Industrial Primes (Airbus, OHB, Thales Alenia Space):** Seek to expand in-space transportation and servicing portfolios, commercializing Phase 0/A concepts (e.g., Airbus CLTV "Moon Cruiser" derivatives).
* **International Partners (NASA / JAXA / CSA):** Depend on interoperable, standard-compliant logistics delivery (IDSS/IBDM docking interfaces) to sustain continuous Gateway operations.

---

## 5. Mission Constraints & Baseline Assumptions

### 5.1 System Constraints
1. **Launcher Fairing & Mass Envelopes:**  
   * Launcher: Ariane 64 with standard 5.4 m fairing (usable internal diameter 4.5 m).
   * Launch Capacity: Ariane 64 injects up to **21,600 kg into LEO** (circular ~300 km) or up to **11,500 kg into GTO**. The combined mass of tug, initial propellant load, and cargo must fit within this single-launch performance limit if co-manifested, or cargo launches independently once the tug is stationed.
2. **Radiation Environment (Van Allen Belts):**  
   * Low-thrust spiral departure from LEO involves prolonged residence (several months) in the proton and electron belts ($1,000\text{ km}$ to $15,000\text{ km}$).
   * Requires rad-hard avionics ($>100\text{ krad}$ TID) and heavy coverglass shielding or thin-film radiation-resistant solar cell technology to limit array degradation to $<15\%$ over the lifetime.
3. **Power Availability & Eclipses:**  
   * Orbital night durations in LEO reach up to ~35 minutes per 90-minute orbit. The tug cannot operate high-power thrusters during eclipse, requiring robust secondary battery reserves (Li-ion) for platform keep-alive and heaters.
4. **Docking & Interoperability Interfaces:**  
   * Must comply with the International Docking System Standard (IDSS) / International Berthing and Docking Mechanism (IBDM) architecture for Gateway and cargo module compatibility.
   * Fluid refuelling interfaces must follow emerging European standards (ESPRIT / ESA Clean Space fluid quick-disconnect couplings).
5. **Space Debris Mitigation:**  
   * Full compliance with ESA Zero Debris Charter: tug must possess sufficient delta-v reserves ($\ge 150\text{ m/s}$) to guarantee controlled, demisable disposal at end of mission life.

### 5.2 Baseline Mission Assumptions
* **Electric Propulsion System:** Dual-mode Hall Effect Thrusters (HET) or Gridded Ion Thrusters (GIT) operating with high-voltage Power Processing Units (PPUs) at $I_{sp} \approx 1,800 - 3,200\text{ s}$.
* **Power Level:** Scalable Solar Electric Propulsion bus of **30 kW to 60 kW** beginning-of-life (BOL) array power.
* **Propellant:** High-purity Xenon (heritage standard). Krypton retained as a low-cost trade option.
* **Operational Cycle Time:** Tug completes approximately 1 cislunar cargo cycle every **12 to 18 months**, accounting for outbound transit, orbital operations, inbound transit, and Earth-orbit refuelling/re-docking.

---

## 6. Flight Mechanics: Delta-V Budget & Transfer Durations

Because electric propulsion imparts continuous, low thrust rather than impulsive burns, trajectories follow many-revolution spirals out of Earth's gravity well into weakly bound chaotic manifolds before capture into the lunar three-body gravity environment.

```
                               CISLUNAR TRAJECTORY PHASES
  [LEO Staging] ──(Low-Thrust Spiral-Out)──► [Earth Escape Boundary]
         │                                              │
         ▼                                              ▼
  ΔV ≈ 6.5 - 7.0 km/s                           ΔV ≈ 0.5 - 0.8 km/s
  Duration: ~6 - 8 months                       Duration: ~1 - 2 months
         │                                              │
         └──────────────────────┬───────────────────────┘
                                ▼
                        [NRHO Insertion]
                                │
               (Optional Low-Thrust Descent)
                                ▼
                       [Low Lunar Orbit - LLO]
                        ΔV ≈ 0.7 - 0.9 km/s
                        Duration: ~20 - 40 days
```

### 6.1 Published Literature Trajectory Data & Citations

The baseline flight mechanics data are compiled from peer-reviewed astrodynamics studies and ESA/NASA concurrent engineering reports:

1. **LEO to Lunar Gateway NRHO (Low-Thrust Spiral):**
   * **Trajectory Profile:** Edelbaum spiral out from circular LEO ($h = 400\text{ km}$, $v_c \approx 7.67\text{ km/s}$) through the Earth gravity well to lunar transfer boundary, followed by stable manifold capture into the southern $L_2$ 9:2 NRHO.
   * **Total $\Delta V$ Budget (Outbound with Cargo):** **$7,200\text{ to }7,800\text{ m/s}$**  
     *(Includes ~6,700 m/s spiral-out, ~700 m/s lunar trans-insertion/capture, and 200 m/s navigation/margin).*
   * **Transfer Duration:** **240 to 350 days (~8 to 11.5 months)** at power-to-mass ratio $P/m \approx 4 - 6\text{ W/kg}$.
   * **Citations:**  
     * Hack, K. J., et al. (NASA GRC), *"Solar Electric Propulsion for Cislunar and Deep Space Missions"*, AIAA/SAE/ASEE Joint Propulsion Conference.
     * McGuire, M. L., et al., *"Low-Thrust Lunar Freight Mission Design"*, NASA Glenn Research Center.
     * Whitley, R., et al., *"Earth-Moon Near Rectilinear Halo and Distant Retrograde Orbits for Lunar Exploration"*, AAS/AIAA Space Flight Mechanics Meeting.

2. **NRHO to LEO (Return Spiral - Tug Only / No Cargo):**
   * **Trajectory Profile:** NRHO departure via unstable manifold, Earth spiral-in back to circular LEO staging orbit.
   * **Total $\Delta V$ Budget (Inbound Tug Dry):** **$6,800\text{ to }7,200\text{ m/s}$**.
   * **Transfer Duration:** **150 to 220 days (~5 to 7.5 months)**. Due to the absence of the 4,500 kg payload, the tug's higher acceleration significantly shortens the return phase.
   * **Citation:** Merrill, C., et al., *"Trajectory Design for the Power and Propulsion Element (PPE) and Co-Manifested Vehicle (CMV)"*, AIAA SciTech Forum.

3. **High Staging Alternative (GTO to NRHO):**
   * **Trajectory Profile:** Ariane 64 injects tug + cargo directly into Geosynchronous Transfer Orbit ($250 \times 35,786\text{ km}$). Tug raises perigee and spirals out.
   * **Total $\Delta V$ Budget:** **$2,800\text{ to }3,400\text{ m/s}$**.
   * **Transfer Duration:** **120 to 180 days (~4 to 6 months)**.
   * **Benefit:** Slashes transfer time by >50% and dramatically reduces radiation exposure in the dense inner Van Allen belt, though launcher payload mass is lower than in LEO.
   * **Citations:**  
     * Racca, G. D., Schoenmaekers, J., et al., *"SMART-1: Electric Propulsion for a Lunar Science Mission"*, Acta Astronautica / ESA Bulletin.
     * Airbus Defence and Space, *"Moon Cruiser / Cis-Lunar Transfer Vehicle (CLTV) Architecture Study"*, ESA GNC / CDF Reports.

4. **NRHO to Low Lunar Orbit (LLO, 100 km circular):**
   * **Total $\Delta V$ Budget:** **$700\text{ to }900\text{ m/s}$** low-thrust transfer.
   * **Transfer Duration:** **25 to 45 days**.
   * **Citation:** ESA Concurrent Design Facility (CDF), *"Lunar Space Tug (LST) Assessment Study"*.

### 6.2 Consolidated Trajectory Reference Table

| Trajectory Phase | Initial State | Target State | Impulsive $\Delta V$ (Chemical Ref) | Low-Thrust $\Delta V$ (EP Tug) | Low-Thrust Duration (30–50 kW class) | Primary Published Source |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **LEO $\to$ NRHO (Outbound)** | LEO (400 km) | Gateway NRHO | $3,950\text{ m/s}$ (5 days) | **$7,400\pm 300\text{ m/s}$** | **240–320 days** | McGuire et al. (NASA GRC); Hack et al. |
| **NRHO $\to$ LEO (Inbound Return)** | Gateway NRHO | LEO (400 km) | $3,900\text{ m/s}$ (5 days) | **$7,000\pm 250\text{ m/s}$** | **150–210 days** (dry tug) | Merrill et al. (AIAA SciTech) |
| **GTO $\to$ NRHO (High Staging)** | GTO | Gateway NRHO | $1,800\text{ m/s}$ (5 days) | **$3,100\pm 300\text{ m/s}$** | **120–170 days** | SMART-1 / Racca et al.; Airbus CLTV |
| **NRHO $\to$ LLO (Delivery Branch)** | Gateway NRHO | LLO (100 km) | $730\text{ m/s}$ (12 hrs) | **$820\pm 60\text{ m/s}$** | **25–40 days** | ESA CDF Lunar Tug Study |

---

## 7. Concept of Operations (ConOps) Lifecycle Overview

The operational cycle is structured into eight standardized phases to form the direct baseline for the Step 2 Capella Operational Analysis:

```
                  ┌────────────────────────────────────────────────────────┐
                  ▼                                                        │
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌────────────┐ │
│   Phase 1    │    │   Phase 2    │    │   Phase 3    │    │  Phase 4   │ │
│ Launch & LEOP│───►│ Cargo Pickup │───►│ Outbound EP  │───►│ Gateway /  │ │
│ (Ariane 64)  │    │ & Validation │    │ Spiral Transit│   │ LLO Delivery││
└──────────────┘    └──────────────┘    └──────────────┘    └─────┬──────┘ │
                                                                  │        │
┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │        │
│   Phase 8    │    │   Phase 7    │    │   Phase 6    │          │        │
│ End of Life  │◄───│ In-Orbit     │◄───│ Inbound EP   │◄─────────┘        │
│ Safe Disposal│    │ Refuelling   │    │ Return Spiral│ (Repeats 5-8x)────┘
└──────────────┘    └──────────────┘    └──────────────┘
```

1. **Phase 1: Launch and Early Orbit Phase (LEOP):** Initial launch of the tug (dry or partially fuelled) on Ariane 64. Solar array deployment, system health checks, electric propulsion system priming.
2. **Phase 2: Cargo Rendezvous & Staging:** Autonomous rendezvous and soft docking with the cargo module launched by Ariane 6 into the Earth staging node. Interface clamping, power/data bridging, and mass-properties recalibration.
3. **Phase 3: Outbound Low-Thrust Transfer:** Continuous thrust spiral-out through Van Allen belts with duty-cycle throttling during eclipse. Trajectory guidance via autonomous optical navigation and ground station tracking.
4. **Phase 4: Cislunar Proximity & Delivery:** Approach along Gateway rendezvous corridor. Relative navigation handover (LiDAR/optical). Docking at Gateway cargo port or handoff to lunar lander. Cargo unberthing and verification.
5. **Phase 5: Lunar Staging / Servicing (Optional):** Potential propellant top-off at Gateway (via ESPRIT interface) or deployment of secondary smallsat payloads.
6. **Phase 6: Inbound Low-Thrust Transfer:** Departure burn from NRHO back to Earth staging orbit. Rapid descent due to high thrust-to-weight ratio in dry configuration.
7. **Phase 7: Earth Staging & Refuelling:** Rendezvous and docking with an orbital propellant depot or dedicated refuelling tanker launched by Ariane 6. High-pressure xenon transfer and system inspection. Loop back to Phase 2 for next cargo trip.
8. **Phase 8: End-of-Life Disposal:** After 5–8 operational cycles, perform controlled disposal burn into high graveyard orbit or targeted destructive re-entry complying with ESA Zero Debris standards.

---

## 8. Requirements Flow-Down & Traceability Baseline

To seed the subsequent Capella Operational and System Analysis (Steps 2 and 3), the mission statement flows down into preliminary top-level system requirements:

* **[SYS-REQ-001] Payload Delivery Capacity:** The system shall deliver a net cargo payload mass of at least $4,500\text{ kg}$ to a 9:2 Earth-Moon Near Rectilinear Halo Orbit (NRHO).
* **[SYS-REQ-002] Multi-Trip Reusability:** The system shall be capable of performing a minimum of 5 complete cislunar round-trip mission cycles over a nominal design lifetime of 10 years.
* **[SYS-REQ-003] In-Orbit Fluid Refuelling:** The system shall incorporate a standardized microgravity fluid interface capable of receiving at least $3,000\text{ kg}$ of pressurized Xenon propellant from an orbital depot or tanker.
* **[SYS-REQ-004] Launcher Envelope Compatibility:** The launch mass and stowed geometric envelope of the tug platform shall be fully compatible with the Ariane 64 launcher and standard 5.4 m fairing.
* **[SYS-REQ-005] Radiation Hardness:** The platform avionics and solar arrays shall maintain nominal mission functionality after accumulating a total ionizing dose (TID) representative of 5 spiral passages through the Earth radiation belts ($>100\text{ krad}$ with screening).
* **[SYS-REQ-006] Autonomous Proximity Operations:** The system shall execute autonomous rendezvous and docking within a $500\text{ m}$ keep-out sphere of the target vehicle or Gateway station without real-time ground human-in-the-loop intervention.
* **[SYS-REQ-007] European Sovereignty:** All mission-critical platform subsystems (electric propulsion thrusters, PPUs, solar arrays, autonomous GNC software, and docking interfaces) shall be procured from European industrial sources without ITAR restrictions.

---

## 9. Conclusion & Bridge to Step 2 (Capella Modeling)

This Mission Definition Note establishes the complete, referenced foundation for the cislunar cargo tug project. The mission premise is firmly anchored in the strategic directives of **ESA Strategy 2040**, **Explore 2040**, and **Technology 2040**, utilizing proven European industrial heritage and realistic flight mechanics from peer-reviewed literature.

**Next Immediate Actions (Step 2 - Operational Analysis in Capella):**
1. Initialize the operational architecture model with the identified stakeholders and operational entities: Cargo Customer, Ariane 6, Ground Segment, Gateway/Lunar Customer, and Refuelling Depot.
2. Formulate operational capabilities: *Deliver Cislunar Cargo*, *Perform In-Orbit Refuelling*, and *Perform Compliant End-of-Life Disposal*.
3. Model the complete round-trip Operational Scenario and export operational architecture diagrams.
