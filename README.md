# Cislunar Electric Cargo Tug: a Phase 0/A systems engineering study

A small, public-information-only study of a **reusable, refuellable solar-electric cargo tug** that moves cargo from a high Earth orbit (GTO-class) to a Near-Rectilinear Halo Orbit (NRHO) and back, modelled with **Arcadia / Capella**.

> **Status: work in progress (step 1 of 7 complete, step 2 in progress).**
> This is a personal learning and portfolio project. It is not a flight-ready design, and every number is a stated, traceable assumption rather than a verified result.

## Why this study

ESA Strategy 2040 and Explore2040 both point to a "Hub-and-Spoke" logistics network with electric-propulsion space tugs, in-orbit refuelling and servicing, and European non-dependence. This study takes that premise and asks what a minimal, credible tug concept looks like, and how its requirements, trade-offs, technology maturity and cost drivers would be worked through at Phase 0/A.

The focus is on the systems engineering process:

- mission definition and operational analysis
- requirements flow-down from system to 2-3 subsystems, with traceability
- architecture trade-offs (power level vs transfer time; refuelling concept)
- logical architecture
- TRL assessment of critical technologies and main cost drivers

## Mission in one paragraph

A 5,000 kg cargo is launched by Ariane 6 to GTO, picked up by the tug, carried by low-thrust electric propulsion to NRHO, and the tug returns to be refuelled and repeat. Reference design point: about 1.05 N thrust at about 2,100 s Isp (roughly 18 kW electric propulsion power), which gives a round trip of about 2 years and about 7 trips in a 15-year life. Low lunar orbit is deliberately excluded from the baseline (about 1.6 km/s more delta-v per leg, a lower cargo limit, long eclipses). A direct-launch baseline is kept as the comparison the tug has to beat.

## Repository contents

| File | Description | Status |
|---|---|---|
| `mission-definition-note.md` | Mission definition note (TUG-MDN-001, Issue 2): objectives, stakeholders, constraints, flight mechanics, ConOps, preliminary system requirements, assumption log (A-01..A-18), decision log (D-01..D-10), references | Done (self-reviewed) |
| `docs/step2-operational-analysis.md` | Operational analysis in Capella: 7 entities, 5 capabilities, 20 activities, 19 interactions, one round-trip scenario, build guide | In progress |
| `capella/` | Capella 7.0 model and SVG/PDF diagram exports | Planned |
| `trade-offs/` | Power vs transfer-time model (Python) and refuelling concept scoring | Planned |
| `report/` | About 10-page study report and 5-slide summary deck | Planned |

## Key results so far

- **Staging orbit:** GTO-class rather than LEO. LEO to GEO alone costs about 6 km/s, more than twice the GTO to NRHO leg (about 2.4 to 3.1 km/s).
- **Delta-v per leg:** 2.4 km/s plus 10% margin = 2.64 km/s (3.1 km/s sensitivity case).
- **Propellant:** about 2.5 t of xenon per round trip for the reference design.
- **Throughput vs power:** 18 kW gives about 7 trips in 15 years; about 25 kW gives 10 trips; about 30 kW gives 8 trips in 10 years.
- **Open decision:** whether to keep return cargo (MO-2). Cutting it would simplify the study.

All figures are documented with sources or labelled as own estimates in the assumption log.

## Method and ground rules

- **Public information only:** ESA Strategy 2040, Explore2040, Technology Vision 2040, and published papers and news. No proprietary or employer data.
- **Every assumption is stated** and numbered in the note's appendix; every design choice has a decision-log entry with rationale.
- **Self-review is documented:** the note includes a review section listing the weaknesses found and how they were fixed.
- **Tooling:** Capella 7.0 (Arcadia method), Python for the trade model.

## Roadmap

| # | Step | Status |
|---|---|---|
| 1 | Mission definition note | Done |
| 2 | Operational analysis in Capella | In progress |
| 3 | System analysis and requirements flow-down (traceability table) | Not started |
| 4 | Trade-offs: power level vs transfer time (quantitative), refuelling concept (qualitative) | Not started |
| 5 | Logical architecture | Not started |
| 6 | TRL assessment and cost drivers | Not started |
| 7 | Study report, interview deck, diagram exports | Not started |

## Sources

Full reference list with links is at the end of `mission-definition-note.md`. Main sources: ESA Strategy 2040, ESA Explore2040, ESA Technology Vision 2040, published low-thrust cislunar transfer studies, and public reporting on the ESPRIT / Lunar View and Gateway programme status.

## Disclaimer

This is an independent personal project. It is not affiliated with, endorsed by, or based on information from any space agency or company. Programme status (for example Gateway, Lunar View) changes quickly; statements reflect public sources as of the date in the document header.

## Licence

Text: CC BY 4.0. Code (when added): MIT.

## Feedback

Comments on assumptions, numbers or method are welcome. Please open an issue.
