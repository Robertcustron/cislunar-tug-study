# Capella model

Arcadia model of the cislunar cargo tug, built in **Capella 7.0.1**.

| Layer | Content | Diagrams |
| --- | --- | --- |
| Operational Analysis | 7 entities, 5 capabilities, 20 activities, 19 interactions, 11 communication means, scenario SC-1 | [`diagrams/operational-analysis/`](diagrams/operational-analysis/) |
| System Analysis | System and 6 actors, mission and 4 capabilities, 19 system functions (17 leaves) and 9 actor functions, 24 functional exchanges, 9 component exchanges, 3 functional chains, 7 modes and 14 transitions, design point as property values | [`diagrams/system-analysis/`](diagrams/system-analysis/) |
| Logical Architecture | 8 logical components, 6 logical actors, 28 logical functions (23 leaves) and 9 actor functions, 33 functional exchanges, 20 component exchanges (CE-01 to CE-20), 3 functional chains | [`diagrams/logical-architecture/`](diagrams/logical-architecture/) |

Every element carries its study ID (OE-, OC-, ACT-, INT-, SF-, LF-, FE-, CE-, CAP-, FC-) in its name or description, and the requirement IDs (SR-, PROP-, PWR-, DRI-, IR-) allocated to it in its description, so the model traces back to the [study documents](../docs/) and the [mission definition note](../mission-definition-note.md).

## Diagrams

| # | Diagram | SVG | PNG |
| --- | --- | --- | --- |
| OA-1 | Operational Capabilities Blank | [SVG](diagrams/operational-analysis/OA-1_OCB.svg) | [PNG](diagrams/operational-analysis/OA-1_OCB.png) |
| OA-2 | Operational Architecture Blank | [SVG](diagrams/operational-analysis/OA-2_OAB.svg) | [PNG](diagrams/operational-analysis/OA-2_OAB.png) |
| OA-3 | Operational Entity Scenario, SC-1 reusable round trip | [SVG](diagrams/operational-analysis/OA-3_OES_SC-1.svg) | [PNG](diagrams/operational-analysis/OA-3_OES_SC-1.png) |
| OA-4 | Operational Activity Interaction Blank | – | [PNG](diagrams/operational-analysis/OA-4_OAIB.png) |
| SA-1 | Missions and Capabilities Blank | [SVG](diagrams/system-analysis/SA-1_MCB.svg) | [PNG](diagrams/system-analysis/SA-1_MCB.png) |
| SA-2 | System Architecture Blank | [SVG](diagrams/system-analysis/SA-2_SAB.svg) | [PNG](diagrams/system-analysis/SA-2_SAB.png) |
| SA-3 | System Architecture Blank with functional chains FC-1 to FC-3 highlighted | [SVG](diagrams/system-analysis/SA-3_SAB_chains.svg) | [PNG](diagrams/system-analysis/SA-3_SAB_chains.png) |
| SA-4 | Mode state machine | [SVG](diagrams/system-analysis/SA-4_MSM.svg) | [PNG](diagrams/system-analysis/SA-4_MSM.png) |
| LA-1 | Logical Component Breakdown | [SVG](diagrams/logical-architecture/LA-1_LCBD.svg) | [PNG](diagrams/logical-architecture/LA-1_LCBD.png) |
| LA-2 | Logical Architecture Blank | [SVG](diagrams/logical-architecture/LA-2_LAB.svg) | [PNG](diagrams/logical-architecture/LA-2_LAB.png) |
| LA-3 | Logical Architecture Blank, propulsion and refuelling | [SVG](diagrams/logical-architecture/LA-3_LAB_FC-2.svg) | [PNG](diagrams/logical-architecture/LA-3_LAB_FC-2.png) |

The SVG files are the Capella exports and the PNG files are rendered from them, except OA-4, which is exported from Capella as PNG only. The colour-coded diagrams carry their legend as a note (for example red for physical flows and dashed blue for information in the SAB). The diagram names in the model carry the Capella type prefix, for example `[SAB] Functional Chains` for SA-3.

## Opening the model

1. Install Capella 7.0.x from [mbse-capella.org](https://mbse-capella.org).
2. Download or clone this repository.
3. In Capella: **File > Import > General > Existing Projects into Workspace**, select the `capella/CislunarCargoTug` folder, **Finish**.
4. Open `CislunarCargoTug.aird` in the Project Explorer to see the diagrams.

## Validation

The Operational Analysis passed **Validate Model** with no errors. The System Analysis and Logical Architecture were added afterwards; their validation run in Capella is not yet recorded here.

Every system and logical element has a realisation link to the layer above: functions, functional exchanges, actors, capabilities, functional chains and the boundary component exchanges. Some OA elements stay unrealised on purpose, because they sit outside the system boundary: the customer's requests, ground planning, the Space Safety Authority, and the interactions between actors (INT-01 to 05, 08, 11, 16 to 18).

The system capabilities are not yet realised by capability realisations in the logical architecture, so validation may flag that.
