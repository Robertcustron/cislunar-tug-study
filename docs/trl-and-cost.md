# TRL and Cost Assessment

**Issue:** 1 (11 October 2026)

This phase answers the questions the earlier phases handed on. How mature are the technologies the tug depends on, and what does it take to reach TRL 6 by the end of Phase B1? How heavy is the tug when built up from its components with ESA margins? How is thruster wear-out handled? And what drives the cost of moving cargo with a tug rather than launching it directly? Costs stay relative (A-13): no public figures exist for a European cislunar tug, so the drivers are ranked and quantified in launches, hardware counts and mass, not in euros.

**Results in four lines**

- **Five critical technologies, all at TRL 3 to 5 for this application.** The longest gap is thruster life. The European 5 kW thruster is flight-proven (TRL 9) for its rated 15,000 to 20,000 h, but the tug needs about 50,000 h per string to avoid frequent replacements. For this mission that makes it TRL 4.
- **Dry mass: 4.6 t bottom-up against 6.1 t parametric.** With ESA maturity margins and a 20 % system margin, the bottom-up estimate is 23 % below the published placeholder used so far. At the lighter mass the tug flies 11 round trips instead of 9, so 9 is a floor, and the parametric value stays the baseline (D-32).
- **The launch per trip is the largest cost driver, and it answers D-09.** A direct Ariane 64 launch with a small expendable carrier on a ballistic transfer puts about 7.1 t into NRHO. The tug brings 5 t per resupply launch, so over 15 years it needs 10 launches where direct launch needs 7. Filling the launcher with about 7 t of cargo per trip keeps 9 trips and cuts the gap to one launch (D-30).
- **Thruster life becomes a dual-path decision.** With today's thruster the propulsion module is exchanged 4 to 8 times over the life. A 380 kg module fits the 3.5 t spare capacity of every resupply launch. A long-life thruster would cut that to one exchange. Both paths run through Phase A, with a decision at its end (D-29).

## 1. Purpose and scope

| Input | From | Used for |
| --- | --- | --- |
| Thruster wear-out: about 90,000 h of thrusting, 15,000 to 23,000 h rated life | Trade-offs (D-18) | Critical technology CT-1; life strategy |
| 5+1 strings of the 5 kW class; R4 module exchange as growth path | Trade-offs (D-20, R4) | Life strategy; CT-5 |
| 8 logical components, interfaces IR-01 to IR-07, array 29.1 kW EOL | Logical architecture | Mass budget by component; CT-3 |
| Mass budget deferred to this phase | Logical architecture (D-28) | Section 3 |
| Figure of merit judged against a direct Ariane 64 launch | Mission definition (D-09) | Section 5 |
| Phase B1 about 2029 to 2030 | Mission definition (A-11) | Target dates for TRL 6 |

**Method.** TRL follows the ESA TRL handbook and ECSS-E-HB-11A: a technology's TRL is judged against the application's requirements, not against its best use elsewhere. A product that is flight-proven in one envelope can therefore sit at a low TRL for this mission. The target is TRL 6 at the end of Phase B1, in line with ESA's practice of reaching TRL 5 to 6 before mission adoption (A-37). Mass margins follow the ESA margin philosophy for assessment studies: 5, 10 or 20 % by maturity, plus 20 % at system level (A-35).

**Out of scope:** euro cost estimates, the ground segment (D-11), and schedule beyond the Phase B1 target.

## 2. Critical technologies and TRL

A technology is critical when the mission depends on it and it has not yet been demonstrated at the level the mission needs. Five pass that test. Proximity propulsion (PROP-06) does not: it is mature, just missing from the architecture (section 3).

| ID | Critical technology | Required by | TRL now | Evidence | Target |
| --- | --- | --- | :---: | --- | :---: |
| CT-1 | Long-life 5 kW Hall thruster string (thruster and PPU): about 50,000 h per string at about 2,100 s | PROP-01, PROP-03, SR-24 | **4** | PPS 5000: qualified in 2021 during a life test that had passed 12,800 h, first flown on Hotbird 13F (Eurostar Neo, 2022), rated life about 15,000 to 20,000 h, catalogue Isp 1,730 to 2,000 s. Magnetic shielding is the known route to longer life (NASA HERMeS designed for more than 50,000 h; 3,570 h wear test), but no European 5 kW shielded thruster exists beyond the laboratory. The PPU (95 % breadboard) is not the gap | 6 |
| CT-2 | In-orbit xenon transfer from a passive module: 2,550 kg in 21 days, 54 coupling matings | DRI-02, DRI-03, IR-02 | **5** | ESPRIT xenon refuelling for Gateway: couplers developed and ground-tested, not flown; its flight is tied to Gateway, paused in March 2026. ESPRIT refuels a few times; the tug mates 54 times | 6 |
| CT-3 | High-power solar array (about 39 kW at beginning of life) and 100 V power control at about 29 kW | PWR-01, PWR-02, PWR-04, IR-01 | **5** | Alphabus flies 100 V regulated buses for 12 to 22 kW of payload power. The arrays of this size in development are US-built (ROSA, 60 kW class, for Gateway's PPE), outside SR-24. Degradation over 18 belt crossings is not characterised (PWR-02) | 6 |
| CT-4 | Autonomous rendezvous and capture of a passive cargo stack with an androgynous docking mechanism, 54 matings | SR-14, SR-25, DRI-01, DRI-03 | **5** | ATV docked with the ISS automatically five times (2008 to 2014), but with a cooperative target. IBDM (under 325 kg) passed CDR in 2015, with a flight model ordered for Dream Chaser. Capturing a passive stack in a GTO-class orbit, and 54 matings, are not demonstrated | 6 |
| CT-5 | In-orbit propulsion-module exchange: latch, 25 kW power connector, xenon and data couplings | PROP-05, IR-08 | **3** | No 25 kW connector has been mated in orbit (refuelling trade, criterion C1). Needed only on the module-exchange path (D-29) | 5 (6 by PDR) |

**Path to TRL 6 by the end of Phase B1 (about 2030):**

| ID | Phase A (to TRL 5) | Phase B1 (to TRL 6) | If it slips |
| --- | --- | --- | --- |
| CT-1 | Erosion model and a short wear test (about 1,000 h) of a magnetically shielded 5 kW variant at 2,100 s | Long-duration wear test (5,000 h or more) with erosion extrapolated to 50,000 h; PPU at the mission operating point | Module exchange with today's thruster (CT-5): 4 to 8 exchanges |
| CT-2 | Breadboard transfer at 121 kg/day with thermal control during recompression | Full-scale ground transfer of 2,550 kg; coupling cycle test to 54 matings with margin | Fewer, larger transfers; depot later |
| CT-3 | Cell radiation tests at belt-crossing fluence (closes PWR-02); 30 kW PCDU breadboard at 100 V | Full-size wing deployment test; PCDU engineering model | Lower EOL/BOL ratio means a larger array; or accept a non-European array (waiver of SR-24) |
| CT-4 | Relative-navigation sensor and GNC hardware-in-the-loop tests on a representative passive target | Closed-loop capture demonstration; IBDM qualification-model cycle test | Add cooperative aids (reflectors, beacon) to the cargo and module |
| CT-5 | 25 kW connector and coupling breadboards | Engineering model mating cycles in vacuum | Not needed if CT-1 succeeds |

One more finding on CT-1: the mission's 2,100 s sits above the PPS 5000 catalogue range (1,730 to 2,000 s), although the development model reached 2,200 s in endurance testing. Running at about 1,800 s gives more thrust per kW (11 trips in the trade-off sensitivity) but 20 % more xenon per trip, so the operating point is part of the CT-1 qualification, not a free choice.

## 3. Mass budget

The dry mass so far was a parametric placeholder: 5.9 t from a published tug design (Rimani et al.), growing by 25 kg/kW above 18 kW (A-10, A-23), so 6.08 t at 25 kW. The logical architecture now gives a component list, so the mass can be built bottom-up. Each line in `model/config/mass_budget.toml` has its basis and an ESA maturity category: 5 % for off-the-shelf items, 10 % for modified ones, 20 % for new developments.

| Component | Nominal (kg) | Maturity margin (kg) | With margin (kg) | Share |
| --- | ---: | ---: | ---: | ---: |
| LC-1 Electric propulsion | 770 | 75 | 845 | 21.8 % |
| LC-2 Electrical power | 958 | 161 | 1,119 | 28.9 % |
| LC-3 Guidance, navigation and control | 113 | 7 | 120 | 3.1 % |
| LC-4 Docking and refuelling interface | 395 | 44 | 438 | 11.3 % |
| LC-5 Command and data handling | 50 | 2 | 52 | 1.4 % |
| LC-6 Communications | 55 | 6 | 60 | 1.6 % |
| LC-7 Thermal control | 155 | 16 | 172 | 4.4 % |
| LC-8 Structure and mechanisms | 900 | 167 | 1,067 | 27.5 % |
| **Total** | **3,396** | **478** | **3,874** | |
| **With 20 % system margin** | | | **4,649** | |

*Source: `model/results/baseline/mass_budget.csv`; line items in `mass_budget_items.csv`.*

The main sourced lines are the xenon tanks (3 × ESA L-XTA, 1,548 kg of xenon each in a tank under 104 kg), the docking mechanism (IBDM class, under 325 kg), the thrusters and PPUs (scaled from AEPS: under 47 kg and under 50 kg for 12.5 kW), and the array (60 W/kg at end of life for large GEO arrays).

What it shows:

- **Power and structure carry 56 % of the dry mass.** The array is the largest single item (582 kg with margin), so CT-3 is also the largest mass lever. The structure (960 kg with margin) is an own estimate and the biggest uncertainty in the budget.
- **The bottom-up estimate is 23 % below the parametric one.** 4.65 t against 6.08 t (CALC-42, CALC-43). At 4.65 t the tug would fly 11 trips (CALC-44). The parametric value comes from a complete published design, so it stays the baseline until the bottom-up estimate matures in Phase A (D-32). SR-05 (at least 9 trips) holds either way. This also corrects the trade-offs: dry mass looked like a weak driver there because only the slope above 18 kW was swept, but the 5.9 t starting point moves the trip count by two.
- **The budget found a missing function.** The Hall thrusters give about 1.5 N along one axis, with a slow start-up and a plume that would hit the cargo. They cannot give the small six-axis impulses that the final metres of a capture need. The tug needs a separate proximity propulsion system (PROP-06, D-31). It now has a 60 kg dry allowance; its type and its own refuelling are open for Phase A. In the logical architecture it becomes a new function, *Provide proximity thrust* (LF-09, PROP), commanded by GNC through a new exchange (FE-33, carried by CE-03).

## 4. Thruster life strategy

At the design point each of the six strings fires about 8,300 h per round trip (CALC-47). How often the strings must be replaced depends only on their rated life:

| Strings | Rated life per string | One set lasts | Exchanges over 9 trips | Strings used over life |
| --- | ---: | ---: | ---: | ---: |
| 5 kW class, 5+1 | 15,000 h (A-24) | 1 trip | 8 | 54 |
| 5 kW class, 5+1 | 20,000 h (A-38) | 2 trips | 4 | 30 |
| 5 kW class, 5+1 | 50,000 h (CT-1 target) | 6 trips | 1 | 12 |
| 5 kW class, 5+1 | 75,000 h | 9 trips | 0 | 6 |
| 12 kW class at 24 kW, 2+1 | 23,000 h | 3 trips | 2 | 9 |

*Source: `model/results/baseline/thruster_life_strategies.csv`.*

Carrying all the spares on board is not an option: at 15,000 h the life consumes 30 string lifetimes. Of today's products the 12 kW class needs the fewest replacements, but it is a US product and conflicts with European sourcing (SR-24).

Replacement is affordable in launches. One exchangeable propulsion module (six strings, their PPUs and pointing mechanisms, plus its structure) weighs 380 kg with margin (CALC-45). Every resupply launch has 3.46 t of spare capacity (CALC-46), so a new module rides along at no launch cost. What it does need is CT-5, an in-orbit interface for 25 kW, xenon and data, which is at TRL 3.

**Decision D-29: run two paths through Phase A.** Path 1 develops the long-life thruster (CT-1), which removes almost all exchanges. Path 2 develops the module-exchange interface (CT-5), which works with today's thruster. Choose at the end of Phase A on the wear-test evidence. Meanwhile the architecture keeps the propulsion module exchangeable (PROP-05, IR-08), which costs little and protects both paths. This closes the trade-offs' open item D-18 and the R4 growth path: module exchange is now designed in, while refuelling stays R1.

## 5. Cost drivers

**The D-09 comparison.** A direct Ariane 64 launch to a lunar transfer orbit (8.6 t) can reach NRHO on a ballistic lunar transfer. That needs 17 to 41 m/s of deterministic delta-v and takes about 100 to 110 days (Parrish et al.). With 100 m/s budgeted and an expendable carrier of 1.2 t (A-36), it delivers about 7.1 t of cargo per launch (CALC-49). The tug delivers 5 t per resupply launch.

| Cargo per trip | Trips | Cargo over 15 years | Tug launches (1 + resupply) | Direct launches for the same cargo | Extra launches with the tug |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 5.0 t (baseline) | 9 | 45 t | 10 | 7 | 3 |
| 6.5 t | 9 | 58.5 t | 10 | 9 | 1 |
| 7.0 t | 9 | 63 t | 10 | 9 | 1 |

*Source: `model/results/baseline/launch_campaign.csv`. The trip count holds up to 7.29 t per trip (CALC-50), with no margin left at that value. At 7 t the resupply launch carries 10.3 t, so a replacement propulsion module (0.38 t) still fits.*

At the baseline cargo the tug needs three more launches than direct delivery. It can only pay for itself if the seven expendable carriers that direct delivery would need cost more than those three extra launches plus the tug programme and its consumables (propellant modules, propulsion modules). Filling the launcher with about 7 t per trip cuts the extra launches to one at no cost in trips. That is the cheapest improvement this study found (D-30). The tug's other advantages are not launch counts: it can return cargo (D-13), use any GTO-class launch, and act as reusable infrastructure in ESA's hub-and-spoke logistics.

**Ranked cost drivers:**

| Rank | Driver | Type | Evidence | Lever |
| :---: | --- | --- | --- | --- |
| 1 | One Ariane 64 per trip | Recurring | 10 launches over the life; 4.5 t of cargo per launch against 7.1 t direct | Fill the launcher: about 7 t per trip keeps 9 trips (D-30) |
| 2 | Thruster life | Recurring and development | 30 string lifetimes consumed; 4 to 8 module exchanges with today's thruster | Long-life thruster (CT-1) or module exchange (CT-5), D-29 |
| 3 | Power chain beyond the European class | Development and recurring | 39 kW BOL array and 29 kW PCDU; electrical power is 29 % of dry mass | Radiation data to firm up EOL/BOL; 100 V Alphabus heritage (CT-3) |
| 4 | Refuelling consumables | Recurring | 8 expendable propellant modules (0.5 t each) | Larger modules or a depot later (R3) |
| 5 | Rendezvous and docking | Development | Docking and refuelling interface 11 % of dry mass; passive-stack capture; proximity propulsion missing | IBDM and ATV heritage; cooperative aids on the cargo (CT-4) |
| 6 | Dry mass uncertainty | Programme risk | 4.65 t against 6.08 t: 11 against 9 trips | Bottom-up maturity in Phase A (D-32) |

## 6. Requirements

| ID | Change | Source |
| --- | --- | --- |
| **PROP-05 (new)** | The thruster strings, their PPUs and pointing mechanisms shall be grouped in one exchangeable propulsion module of no more than 0.4 t (with maturity margin), so that a replacement module fits the spare capacity of a resupply launch | D-29, CALC-45, CALC-46 |
| **PROP-06 (new)** | PROP shall provide translation and attitude thrust for proximity operations and capture, independent of the Hall thrusters (delta-v per rendezvous TBD, propellant TBD) | D-31 |
| **IR-08 (new)** | The propulsion module shall connect to the tug through one mechanical latch, one power connector rated for 25 kW at 100 V (TBC), one xenon feed coupling and one data connector, all mated and demated in orbit | D-29, CT-5 |

Column `changed_in` = "TRL and cost assessment (new)" in the CSV files.

## 7. New assumptions and decisions

| ID | Assumption | Value | Basis |
| --- | --- | --- | --- |
| A-34 | Mass of each component line | `mass_budget.toml` | Public sources where they exist (L-XTA, IBDM, AEPS, NASA array survey), own estimates otherwise, each with its basis |
| A-35 | Mass margins | 5 / 10 / 20 % by maturity, 20 % system | ESA margin philosophy for science assessment studies (SRE-PA/2011.097, issue 1.3); its 20 % system power margin also supports A-30 |
| A-36 | Direct-launch alternative | 8.6 t to lunar transfer orbit; 100 m/s ballistic transfer; 300 s; 1.2 t expendable carrier | Ariane 64 capability (D-09); Parrish et al. for the transfer; carrier mass own estimate (swept 0.8 to 1.6 t gives 7.5 to 6.7 t of cargo) |
| A-37 | TRL target | TRL 6 at the end of Phase B1 (about 2030) | ESA: TRL 5 to 6 before mission adoption; Phase B1 dates from A-11 |
| A-38 | PPS 5000 rated life, sensitivity | 20,000 h (baseline stays 15,000 h, A-24) | Published figures differ: about 15,000 h (satcatalog) and about 20,000 h (Safran representative) |

| ID | Decision | Why | Left open |
| --- | --- | --- | --- |
| D-29 | Thruster life: dual path through Phase A (long-life thruster CT-1, and module exchange CT-5); propulsion module kept exchangeable (PROP-05, IR-08) | Neither path is above TRL 4 today; keeping the module exchangeable protects both | Down-select at the end of Phase A |
| D-30 | Recommend about 7 t of cargo per trip for Phase A; the study keeps 5 t (A-01) for consistency | Same 9 trips, 40 % more cargo, one extra launch against direct instead of three | Customer demand for 7 t loads |
| D-31 | Add a proximity propulsion system (PROP-06) with a mass allowance | Hall thrust cannot translate the stack for capture | Type (hydrazine, green monopropellant, xenon cold gas) and its refuelling |
| D-32 | Parametric 6.08 t stays the baseline dry mass; the 4.65 t bottom-up estimate is an upside | The parametric value is a complete published design; the bottom-up has own estimates for structure and harness | Converge in Phase A |
| D-33 | Five critical technologies, CT-1 to CT-5, each with a Phase A and Phase B1 step to TRL 6 | Section 2 | Funding lines |

## Sources

- ESA, [Technology Readiness Levels (TRL)](https://www.esa.int/Enabling_Support/Space_Engineering_Technology/Shaping_the_Future/Technology_Readiness_Levels_TRL); ECSS-E-HB-11A, [Technology readiness level (TRL) guidelines](https://ecss.nl/home/ecss-e-hb-11a-technology-readiness-level-trl-guidelines-1-march-2017/)
- ESA, [Technology development in support of future science missions](https://sci.esa.int/web/sci-ft/-/50034-technology-development-in-support-of-future-science-missions) (TRL 5 to 6 before adoption)
- ESA, [Margin philosophy for science assessment studies](https://sci.esa.int/documents/34375/36249/1567260131067-Margin_philosophy_for_science_assessment_studies_1.3.pdf), SRE-PA/2011.097, issue 1.3
- Safran, PPS 5000 life test and qualification, [IAC-21 abstract](https://p.iafastro.directory/iac/paper/id/64241/abstract-pdf/IAC-21,C4,5,5,x64241.brief.pdf); [satcatalog PPS 5000](https://www.satcatalog.com/component/pps5000/); [Safran representative product page](https://psirep.com/products/safran-dsi-pps5000-hall-effect-thruster); [Spaceflight Now, Hotbird 13F on Eurostar Neo](https://spaceflightnow.com/2022/10/14/spacex-launch-to-deploy-first-in-new-generation-of-airbus-built-satellites/)
- Frieman et al., [Completion of the Long Duration Wear Test of the NASA HERMeS Hall Thruster](https://ntrs.nasa.gov/api/citations/20190031949/downloads/20190031949.pdf)
- NASA, [12-kW AEPS Hall Current Thruster Qualification and Production Status](https://ntrs.nasa.gov/citations/20250003901), 2025 (12 kW, thruster 53 kg). The under-47 kg thruster and under-50 kg PPU figures come from the L3Harris AEPS spec sheet (2023), which is no longer online.
- ESA ARTES, [L-XTA large xenon tank assembly](https://resilience.esa.int/archives/projects/l-xta-large-xenon-tank-assembly)
- C. Mercer, NASA GRC, [Advanced Solar Arrays](https://discovery.larc.nasa.gov/pdf_files/02-AdvSolrArry-CMercer-2.pdf), 2014
- [International Berthing and Docking Mechanism](https://en.wikipedia.org/wiki/International_Berthing_and_Docking_Mechanism) (Wikipedia)
- CNES, [ATV missions](https://cnes.fr/en/projects/atv)
- Parrish et al., [Ballistic Lunar Transfers to Near Rectilinear Halo Orbit: Operational Considerations](https://ntrs.nasa.gov/api/citations/20200011549/downloads/20200011549.pdf)
- ESA, [Alphabus: An Extended European Capability](https://resilience.esa.int/archives/news/alphabus-extended-european-capability)
