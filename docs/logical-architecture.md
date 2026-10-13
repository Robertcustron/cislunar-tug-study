# Logical Architecture (Capella)

**Issue:** 1 (11 October 2026)

The logical architecture opens the black box of the system analysis. The tug is split into logical components, every system function is allocated to one of them, and the flows between components become component exchanges, which are the tug's internal and external interfaces. The decisions of the trade-offs (25 kW, 5+1 thruster strings, refuelling from a co-launched propellant module) are built into the architecture, and the power chain is sized with a budget per mode in the Python model (CALC-29 to CALC-39).

**Results in four lines**

- **Eight logical components.** Propulsion, power and the docking and refuelling interface keep the boundaries of the subsystems flowed down in the system analysis, so that flow-down still holds. Thermal control and structure appear for the first time, because heat rejection and load paths only exist once there is a design.
- **Twenty component exchanges and seven interface requirements.** The xenon path from the propellant module to the thrusters crosses two interfaces (CE-13 and CE-02). Each thruster string touches the rest of the tug only through power, xenon and data (IR-04), which keeps a later propulsion-module exchange open for the thruster wear-out risk (D-18).
- **The power budget closes A-21 and corrects the array size.** The highest platform load is 1.11 kW in Docking, or 1.33 kW with a 20 % margin, inside the 2 kW allocation. Sized to that allocation, the array needs 29.1 kW at end of life, not the 27 kW counted in the trade-offs: distribution losses and battery recharge add the difference. The battery needs 8.8 kWh for a 2.5 h eclipse.
- **One ambiguity removed.** "25 kW to the electric propulsion" now means 25 kW at the PPU inputs. The 60 % efficiency used in every trade is read as PPU (95 %) × thruster (63 %), which gives back 59.9 % (CALC-31), so no trade-off number changes.

> **Note after the TRL and cost assessment.** The mass budget showed that the tug has no propulsion for the last metres of a capture. One function was added: *Provide proximity thrust* (LF-09, PROP), commanded by *Control trajectory and attitude* through FE-33, carried by CE-03, with requirement PROP-06. The propulsion module was made exchangeable (PROP-05, IR-08). See [the TRL and cost assessment](trl-and-cost.md).

## 1. Purpose and scope

In Arcadia the logical architecture answers "how will the system work to meet its needs?" without yet naming equipment. It works from the system analysis (functions, exchanges, modes, requirements) and the trade-off decisions (D-16 to D-20).

| Input | Used for |
| --- | --- |
| 17 leaf system functions and 24 functional exchanges (system analysis) | Transitioned to logical functions; refined where a function spans two components |
| Modes (system analysis) | Power budget per mode |
| D-16 25 kW, D-20 5+1 strings, A-27 rotation | High-power interface and thruster string boundary |
| D-17 refuelling from a co-launched module, D-19 propellant module actor | Refuelling interface, functional chain FC-2 |
| D-18 thruster wear-out risk | Interface rule that keeps a propulsion-module exchange possible |
| A-21 platform power 2 kW (TBC), PWR-03 eclipse and DoD (TBD), SR-12 eclipse (TBD) | Closed by the power budget |

**Out of scope here:** equipment choices, data bus standard and harness (physical architecture); the mass budget by component, which the TRL and cost assessment builds bottom-up with maturity margins (D-28); and detailed thermal design.

## 2. Logical components

| ID | Component | What it contains (logically) | Allocated functions |
| --- | --- | --- | --- |
| LC-1 | **Electric propulsion (PROP)** | Six thruster strings (one PPU per 5 kW Hall thruster, flow control), xenon tanks and feed | 3 |
| LC-2 | **Electrical power (PWR)** | Solar arrays, 100 V regulated bus (TBC), Li-ion battery, distribution | 3 |
| LC-3 | Guidance, navigation and control (GNC) | Attitude and orbit sensors and actuators, low-thrust guidance, rendezvous sensors | 3 |
| LC-4 | **Docking and refuelling interface (DRI)** | One androgynous docking port, xenon coupling, cargo latches | 5 |
| LC-5 | Command and data handling (CDH) | On-board computer, modes and FDIR, command routing, telemetry | 4 |
| LC-6 | Communications (COMMS) | X-band TT&C to 450,000 km, proximity link to the destination | 2 |
| LC-7 | Thermal control (TCS) | Pumped loop for the PPU heat, radiators, heaters | 1 |
| LC-8 | Structure and mechanisms (STR) | Primary structure, launch adapter, deployments | 1 |

Bold = the three subsystems of the system analysis flow-down (PROP, PWR, DRI), kept with the same boundaries (D-21).

## 3. Logical functions and allocation

The 17 leaf system functions are transitioned to the logical architecture, each keeping a realisation link to its system function. Three of them span two components, so they become parents and are split; two functions are new.

| Function | ID | Realises | Component |
| --- | --- | --- | --- |
| Generate thrust | SF-03.1 | SF-03.1 | PROP |
| Store and feed propellant | SF-03.2 | SF-03.2 | PROP |
| Vent residual propellant | LF-05 | SF-07.2 (split) | PROP |
| Generate electrical power | SF-03.5 | SF-03.5 | PWR |
| Store and distribute electrical power | SF-03.6 | SF-03.6 | PWR |
| Discharge and isolate batteries | LF-06 | SF-07.2 (split) | PWR |
| Determine orbit and attitude | SF-03.3 | SF-03.3 | GNC |
| Control trajectory and attitude | SF-03.4 | SF-03.4 | GNC |
| Perform rendezvous and proximity navigation | SF-03.10 | SF-03.10 | GNC |
| Capture cargo in Earth staging orbit | SF-01 | SF-01 | DRI |
| Receive propellant in orbit | SF-02 | SF-02 | DRI |
| Hand over cargo at lunar destination | SF-04 | SF-04 | DRI |
| Collect return cargo | SF-05 | SF-05 | DRI |
| Hand over return cargo in Earth orbit | SF-06 | SF-06 | DRI |
| Manage modes and failures | SF-03.9 | SF-03.9 | CDH |
| Perform disposal manoeuvre | SF-07.1 | SF-07.1 | CDH |
| Validate and route commands | LF-02 | SF-03.7 (split) | CDH |
| Collect and format telemetry | LF-03 | SF-03.8 (split) | CDH |
| Receive radio messages | LF-01 | SF-03.7 (split) | COMMS |
| Transmit telemetry | LF-04 | SF-03.8 (split) | COMMS |
| Control temperatures and reject heat | LF-07 | new (design-induced) | TCS |
| Carry loads and interface with the launcher | LF-08 | new (design-induced) | STR |

**Why these splits.** *Execute telecommands* and *Provide telemetry* each mix a radio job (COMMS) with a data job (CDH); all ground and proximity messages now enter through *Receive radio messages* (D-27). *Passivate the system* acts on two different stores of energy, xenon in PROP and charge in PWR, so each component gets its own passivation function, both ordered by the disposal sequence in CDH.

**Why two new functions.** The black-box system analysis did not need them. Once 25 kW flows through PPUs that are 95 % efficient, 1.25 kW of heat has to go somewhere (LF-07). The launch requirement SR-06 had no function in the system analysis; it now has one in STR (LF-08). Both are design-induced functions, a normal result of the logical architecture.

**Coverage:** 22 leaf functions, each allocated to exactly one component; every component holds at least one function.

## 4. Functional exchanges

The 24 system exchanges are transitioned. Seven have one end moved to a refined function, and eight are added.

| ID | Exchange | From → to | Change |
| --- | --- | --- | --- |
| FE-03 | Telecommands | Ground Segment → Receive radio messages | End moved (was Execute telecommands) |
| FE-04 | Telemetry | Transmit telemetry → Ground Segment | End moved (was Provide telemetry) |
| FE-05 | Approach clearance | Lunar Orbit Destination → Receive radio messages | End moved (was Rendezvous and proximity navigation) |
| FE-09 | Disposal command | Ground Segment → Receive radio messages | End moved (was Perform disposal manoeuvre) |
| FE-18 | Operational commands | Validate and route commands → Manage modes and failures | End moved (was Execute telecommands) |
| FE-19 | Housekeeping and mode status | Manage modes and failures → Collect and format telemetry | End moved (was Provide telemetry) |
| FE-24 | Passivation order | Perform disposal manoeuvre → Vent residual propellant | End moved (was Passivate the system) |
| FE-25 | Received messages | Receive radio messages → Validate and route commands | New |
| FE-26 | Approach clearance (routed) | Validate and route commands → Rendezvous and proximity navigation | New: the clearance now reaches GNC through CDH |
| FE-27 | Telemetry frames | Collect and format telemetry → Transmit telemetry | New |
| FE-28 | Battery passivation order | Perform disposal manoeuvre → Discharge and isolate batteries | New |
| FE-29 | PPU waste heat | Generate thrust → Control temperatures and reject heat | New, physical (1.25 kW, CALC-37) |
| FE-30 | Launch loads and separation | Launch Vehicle → Carry loads and interface with the launcher | New, physical (SR-06) |
| FE-31 | Capture approach state | Rendezvous and proximity navigation → Capture cargo | New: capture of the stack needs relative navigation (SR-14, SR-25) |
| FE-32 | Disposal command (routed) | Validate and route commands → Perform disposal manoeuvre | New |

FE-31 fills a gap in the system analysis: capture (SF-01) received the cargo but no navigation input, although SR-14 and SR-25 ask for an autonomous capture of the stack. The logical architecture is where this showed up, because the GNC-to-DRI interface had to carry something for capture as well as for docking.

Total: 32 functional exchanges, 14 physical and 18 information.

## 5. Component exchanges and interfaces

Every functional exchange between functions on two different components is carried by a component exchange (CE). Exchanges inside one component (FE-11, 14, 15, 16, 18, 19, 20, 22, 32) need none.

| ID | Component exchange | From → to | Carries | Kind |
| --- | --- | --- | --- | --- |
| CE-01 | High-power bus | PWR → PROP | FE-12 | Power |
| CE-02 | Xenon transfer line | DRI → PROP | FE-13 | Xenon |
| CE-03 | Thrust commands | GNC → PROP | FE-17 | Data |
| CE-04 | Propulsion commands | CDH → PROP | FE-24 | Data |
| CE-05 | Power commands | CDH → PWR | FE-28 | Data |
| CE-06 | GNC commands | CDH → GNC | FE-23, FE-26 | Data |
| CE-07 | Proximity state | GNC → DRI | FE-21, FE-31 | Data |
| CE-08 | Received messages | COMMS → CDH | FE-25 | Data |
| CE-09 | Telemetry frames | CDH → COMMS | FE-27 | Data |
| CE-10 | Thermal interface | PROP → TCS | FE-29 | Heat |
| CE-11 | Launch adapter | Launch Vehicle → STR | FE-30 | Mechanical |
| CE-12 | Cargo and module stack | Launch Vehicle → DRI | FE-01 | Mechanical |
| CE-13 | Xenon coupling | Propellant Module → DRI | FE-02 | Xenon |
| CE-14 | TT&C uplink | Ground Segment → COMMS | FE-03, FE-09 | Radio |
| CE-15 | TT&C downlink | COMMS → Ground Segment | FE-04 | Radio |
| CE-16 | Proximity link | Lunar Orbit Destination → COMMS | FE-05 | Radio |
| CE-17 | Cargo delivery | DRI → Lunar Orbit Destination | FE-06 | Mechanical |
| CE-18 | Return cargo | Lunar Orbit Destination → DRI | FE-07 | Mechanical |
| CE-19 | Returned cargo | DRI → Cargo Customer | FE-08 | Mechanical |
| CE-20 | Sunlight | Sun → PWR | FE-10 | Power |

Ten are internal (CE-01 to CE-10) and ten cross the system boundary (CE-11 to CE-20). Seven of the internal ones are data; physically they will share one redundant data bus, chosen in the physical architecture (IR-05).

**Interface requirements.** The interfaces that drive the design get their own requirements (file `requirements/interface_requirements.csv`):

| ID | Interface | Requirement | Derived from | CE |
| --- | --- | --- | --- | --- |
| IR-01 | High-power bus | PWR shall supply the thruster strings from a 100 V regulated bus (TBC), delivering at least 25 kW at the PPU inputs at end of life through six individually protected and switchable feeds of at least 5 kW each. | SR-11, PWR-01, D-20, D-22, D-23, D-25 | CE-01 |
| IR-02 | Refuelling | The xenon path from the DRI coupling to the PROP tanks shall carry at least 2,550 kg per refuelling within 21 days (an average of about 121 kg/day), with an isolation valve on each side of the DRI-PROP interface (leak rate TBD). | SR-09, SR-25, DRI-02, A-26, CALC-39 | CE-13, CE-02 |
| IR-03 | Thermal | TCS shall remove up to 1.25 kW of PPU waste heat from the PROP thermal interface at the design point, and up to 3.3 kW in total in Transfer (interface temperatures TBD). | SR-11, CALC-37, CALC-38, A-29 | CE-10 |
| IR-04 | Thruster string boundary | Each thruster string (PPU, thruster and flow control) shall connect to the rest of the tug only through its power feed, its xenon feed and the on-board data bus, so that strings, or a whole propulsion module, can later be exchanged without changing other components. | D-18, D-23, D-24, A-27 | CE-01, CE-03, CE-04 |
| IR-05 | On-board data | CDH, GNC, PROP, PWR, DRI and COMMS shall exchange commands and status over a redundant on-board data bus (standard chosen in the physical architecture). | SR-19, SR-20, SR-21 | CE-03 to CE-09 |
| IR-06 | Proximity link | COMMS shall receive approach clearance from the lunar orbit destination over a proximity radio link (band TBC, range TBD) and pass it to GNC through CDH within TBD s. | SR-15 | CE-16, CE-08, CE-06 |
| IR-07 | Launch adapter | STR shall provide a launch adapter interface compatible with Ariane 64 for a tug launch mass of up to 11,500 kg (adapter type TBD from the Ariane 6 user's manual). | SR-06, C-1 | CE-11 |

The external docking interfaces (CE-12, CE-13, CE-17 to CE-19) are already covered by DRI-01 to DRI-04 from the system analysis, and the radio links by SR-18.

## 6. How the trade-off decisions shape the architecture

| Decision | Where it shows in the architecture |
| --- | --- |
| D-16 25 kW | CE-01 sized at 25 kW at the PPU inputs (IR-01); array and battery sized in section 7 |
| D-20 5+1 strings of the 5 kW class | Six PPUs, one per thruster, each on its own switchable feed (D-23, IR-01) |
| A-27 rotation of the spare | Individually switchable feeds let any five of the six strings run, and a failed string is isolated without losing another |
| D-17 refuelling from a co-launched module | FC-2 runs Propellant Module → DRI → PROP, crossing CE-13 (coupling, DRI-02) and CE-02 (transfer line, IR-02) |
| D-19 one rendezvous for cargo and module | CE-12 carries the cargo and module stack; FE-31 gives capture its navigation input |
| D-18 thruster wear-out | IR-04: the strings are a clean module boundary, so the propulsion-module exchange (R4) stays possible without redesigning the rest of the tug |

## 7. Power budget and sizing

The budget lists the nominal platform load of each component in each mode, from `model/config/power_budget.toml`, where every line carries its basis (A-33). The electric propulsion input (25 kW) flows only in Transfer and is added separately. *Eclipse* is Transfer with the thrusters off in the Earth's shadow.

| Component | Launch | Commissioning | Transfer | Eclipse | Docking | Refuelling | Safe | Disposal |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| LC-1 Electric propulsion (housekeeping only) | 0 | 150 | 120 | 100 | 60 | 300 | 60 | 120 |
| LC-2 Electrical power | 20 | 60 | 60 | 60 | 60 | 60 | 60 | 60 |
| LC-3 Guidance, navigation and control | 0 | 150 | 150 | 150 | 260 | 120 | 120 | 150 |
| LC-4 Docking and refuelling interface | 0 | 10 | 10 | 10 | 200 | 80 | 10 | 10 |
| LC-5 Command and data handling | 50 | 80 | 80 | 80 | 80 | 80 | 80 | 80 |
| LC-6 Communications | 15 | 120 | 50 | 50 | 150 | 120 | 120 | 120 |
| LC-7 Thermal control | 0 | 300 | 250 | 400 | 300 | 300 | 350 | 250 |
| LC-8 Structure and mechanisms | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Total (nominal)** | **85** | **870** | **720** | **850** | **1,110** | **1,060** | **800** | **790** |
| **Total with 20 % margin** | **102** | **1,044** | **864** | **1,020** | **1,332** | **1,272** | **960** | **948** |

*Source: `model/results/baseline/power_budget.csv`. All values in W.*

Docking is the worst platform mode: the rendezvous sensors, the capture mechanism and continuous communications all run at once. Even with a 20 % margin it stays at two thirds of the 2 kW allocation, so **A-21 is confirmed and kept as the allocation** (PWR-01). All sizing below uses the allocation, not the estimate, because the allocation is what PWR-01 promises.

| ID | Result | Value | How |
| --- | --- | --- | --- |
| CALC-29 | Longest eclipse in the GTO-class staging orbit | 2.2 h | Earth's shadow (2 R_E) crossed at the apogee speed of a 250 × 35,786 km orbit (1.60 km/s) |
| CALC-30 | Period of the staging orbit | 10.5 h | Kepler |
| CALC-31 | Thruster total efficiency, PPU × thruster | 0.599 (A-19: 0.60, MATCH) | 0.95 × 0.63 |
| CALC-32 | Highest platform load with margin (Docking) | 1.33 kW | Budget table × 1.2 |
| CALC-33 | Battery energy | 8.8 kWh | 2 kW × 2.5 h / (0.95 × 0.60 DoD) |
| CALC-34 | Battery recharge power in Transfer | 0.69 kW | Energy drawn in eclipse, replaced over the 8 h of sunlight per orbit |
| CALC-35 | Solar array power at end of life | 29.1 kW | (25 + 2 + 0.69 kW) / 0.95 distribution efficiency |
| CALC-36 | Solar array power at beginning of life | 38.9 kW | 29.1 kW / 0.75 (EOL/BOL, A-32) |
| CALC-37 | PPU waste heat | 1.25 kW | 25 kW × (1 − 0.95) |
| CALC-38 | Heat to reject in Transfer | 3.25 kW | PPU heat + 2 kW platform |
| CALC-39 | Xenon transfer rate | 121 kg/day | 2,537 kg per trip at 25 kW / 21 days |

Three things to read from it:

- **The eclipse is a mission-design constraint as much as a battery size.** In a GTO-class orbit the longest eclipse is about 2.2 h. Electric orbit-raising tools such as OHB's ELECTRO switch the thrusters off in eclipse and choose the perigee placement to keep eclipses short (Bastante and Peñarroya), which is the approach taken here. Further out on the spiral the apogee speed drops and an eclipse at apogee would last longer. Rather than carry a larger battery for every case, eclipses longer than 2.5 h are excluded by trajectory phasing (D-26). NRHO eclipses are below an hour and can be avoided altogether (Zimovan-Spreen, Howell and Davis, AAS 20-562).
- **The array is larger than the trade-offs counted.** The trade-offs added 25 kW and 2 kW. Distribution losses and battery recharge bring the end-of-life need to 29.1 kW, and radiation degradation over 15 years of belt crossings to about 39 kW at beginning of life. That is well above the 12 to 22 kW payload power of today's largest European platform (Alphabus), so the array and the power electronics are a development item for the TRL and cost assessment.
- **Thermal control is a real subsystem here.** About 3.3 kW has to be rejected in Transfer, 1.25 kW of it from the PPUs alone (IR-03).

## 8. Requirements

**Allocation to logical components.** Each system requirement follows its functions to the components that hold them (file `requirements/component_allocation.csv`). Every component carries at least one requirement.

| Req. | PROP | PWR | GNC | DRI | CDH | COMMS | TCS | STR |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| SR-01 | ● | ● | ● | ● | ● | ● |  |  |
| SR-02 |  |  |  | ● |  |  |  |  |
| SR-03 | ● |  |  |  |  |  |  |  |
| SR-04 | ● | ● | ● |  | ● | ● |  |  |
| SR-05 | ● | ● | ● | ● | ● | ● | ● | ● |
| SR-06 |  |  |  |  |  |  |  | ● |
| SR-07 | ● |  |  |  |  |  |  |  |
| SR-08 | ● |  |  |  |  |  |  |  |
| SR-09 |  |  |  | ● |  |  |  |  |
| SR-10 | ● |  |  |  |  |  |  |  |
| SR-11 | ● | ● |  |  |  |  |  |  |
| SR-12 |  | ● |  |  |  |  | ● |  |
| SR-13 | ● | ● | ● | ● | ● | ● | ● | ● |
| SR-14 |  |  | ● | ● |  |  |  |  |
| SR-15 |  |  | ● | ● |  |  |  |  |
| SR-16 |  |  |  | ● |  |  |  |  |
| SR-17 |  |  |  | ● |  |  |  |  |
| SR-18 |  |  |  |  | ● | ● |  |  |
| SR-19 |  |  | ● |  |  |  |  |  |
| SR-20 |  | ● |  |  | ● |  | ● |  |
| SR-21 |  |  | ● |  | ● | ● |  |  |
| SR-22 | ● |  |  |  | ● |  |  |  |
| SR-23 | ● | ● |  |  | ● |  |  |  |
| SR-24 | ● | ● | ● | ● |  |  |  |  |
| SR-25 |  |  | ● | ● |  |  |  |  |
| SR-26 |  |  |  | ● |  |  |  |  |

**Changed and new requirements** (column `changed_in` = "Logical architecture" in the CSV files):

| ID | Change | Source |
| --- | --- | --- |
| SR-12 | Eclipse duration TBD → eclipses of up to 2.5 h; longer eclipses excluded by trajectory design | A-28, CALC-29, D-26 |
| PWR-01 | 2 kW platform load no longer TBC: confirmed as the allocation by the power budget | CALC-32 |
| PWR-03 | Eclipse and depth of discharge TBD → 2.5 h at 60 % DoD, at least 8.8 kWh | CALC-33, A-28, A-31 |
| **PWR-04 (new)** | The solar array shall provide at least 29.1 kW at end of life (about 38.9 kW at beginning of life with an EOL/BOL ratio of 0.75, TBC by PWR-02) | CALC-34 to CALC-36 |
| DRI-02 | Flow rate TBD → an average of about 121 kg/day (leak rate still TBD) | IR-02, CALC-39 |
| **IR-01 to IR-07 (new)** | Interface requirements, section 5 | — |

## 9. New assumptions and decisions

These continue the numbering of the mission note's registers.

| ID | Assumption | Value | Basis |
| --- | --- | --- | --- |
| A-28 | Design eclipse carried by the battery | 2.5 h | CALC-29 (2.2 h at GTO-class apogee) rounded up; NRHO eclipses under 1 h and avoidable (AAS 20-562) |
| A-29 | PPU and thruster efficiencies | 95 % and 63 % | PPU: ESA ARTES PPS 5000 project, high-power PPU breadboard at 95 %; thruster: own estimate, same as the 12 kW-class unit |
| A-30 | Power margin and distribution efficiency | 20 % on estimates; 95 % from array to loads | Own convention for Phase 0/A; own estimate |
| A-31 | Battery depth of discharge and efficiency | 60 %; 95 % | Own estimate for a Li-ion battery cycled a few thousand times |
| A-32 | Solar array end-of-life to beginning-of-life ratio | 0.75 | Own estimate for 15 years with two belt crossings per round trip; TBC by the dose analysis (PWR-02) |
| A-33 | Platform loads per component and mode | `power_budget.toml` | Own estimates, each with its basis |

| ID | Decision | Why | Left open |
| --- | --- | --- | --- |
| D-21 | Eight logical components; PROP, PWR and DRI keep the boundaries of the flowed-down subsystems; TCS and STR added for design-induced functions | The system analysis flow-down stays valid; every function and requirement has an owner | — |
| D-22 | EP power is defined at the PPU inputs; A-19 (60 %) is read as PPU × thruster | Makes the PWR-PROP interface unambiguous; CALC-31 shows no trade-off number changes | — |
| D-23 | Six thruster strings, one PPU per thruster, each on its own switchable feed | Supports rotation (A-27) and isolates a failed string | Cross-strapping, if the PPU count drives cost |
| D-24 | Thruster strings touch the rest of the tug only through power, xenon and data (IR-04) | Keeps the propulsion-module exchange (R4) open for the wear-out risk (D-18) | Whether to use it: TRL and cost assessment |
| D-25 | 100 V regulated high-power bus (TBC) | European heritage: Alphabus offers 100 V and 50 V regulated buses | Direct-drive alternative not assessed |
| D-26 | Eclipses longer than 2.5 h are avoided by trajectory phasing rather than carried by the battery | Battery stays at 8.8 kWh; constraint handed to mission analysis | Trajectory design |
| D-27 | All radio traffic enters and leaves through COMMS; CDH validates, routes and formats | One owner per job; COMMS and CDH can be specified separately | — |
| D-28 | The mass budget by logical component is built in the TRL and cost assessment | Bottom-up with maturity margins; replaces the A-10/A-23 placeholder there | — |

## Sources

- J. C. Bastante and P. Peñarroya (OHB System AG), *ELECTRO: A SW Tool for the Electric Propulsion Trajectory Optimisation*, ICATT 2018: <https://indico.esa.int/event/224/papers/3875/files/204-ICATT-2018_Bastante_ELECTRO.pdf>
- E. M. Zimovan-Spreen, K. C. Howell and D. C. Davis, *Eclipse Avoidance in Dynamical Structures Nearby NRHOs in a Higher-Fidelity Model*, AAS 20-562: <https://engineering.purdue.edu/people/kathleen.howell.1/Publications/Conferences/2020_AAS_SprHowDav.pdf>
- ESA ARTES, *Electric Thruster Based on Plasma Propulsion including Power Processing Unit* (PPS 5000, HPPU breadboard 95 %): <https://artes.esa.int/projects/electric-thruster-based-plasma-propulsion-including-power-processing-unit>
- ESA, *Alphabus: An Extended European Capability* (100 V and 50 V regulated buses, 12–22 kW payload power): <https://resilience.esa.int/archives/news/alphabus-extended-european-capability>
