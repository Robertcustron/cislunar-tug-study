# Study report

`cislunar-tug-study-report.pdf` is the study report: a summary of every phase of the study in 16 pages, followed by the assumption and decision registers, the Capella diagrams and a guide to reproducing the results.

It is a personal learning study, not for professional use (see "About this study" in the report).

## Rebuilding it

From the repository root:

```
cd model && cislunar-tug run && cd ..          # model results (optional, already committed)
python report/figures/make_figures.py          # report figures, from the model results and requirement tables
cd report && latexmk -pdf cislunar-tug-study-report.tex
```

Needs a LaTeX distribution with `latexmk` (TeX Live, MiKTeX, or Overleaf) and matplotlib for the figures.

## Figures

| File | Drawn from |
| --- | --- |
| `fig01_mission_concept` | `power_trade.csv`, 25 kW row |
| `fig02_flowdown` | `requirements/system_requirements.csv`, `subsystem_requirements.csv` |
| `fig03_power_trade` | `power_trade.csv` |
| `fig04_logical_architecture` | Component exchange table in `docs/logical-architecture.md` |
| `fig05_power_modes` | `power_budget.csv` |
| `fig06_mass_budget` | `mass_budget.csv`, `power_trade.csv` |
| `fig07_trl` | Critical technology table in `docs/trl-and-cost.md` |
| `fig08_launch_campaign` | `launch_campaign.csv` |
| `capella/*.pdf` | Capella diagram exports (`capella/diagrams/*.svg` in the repository), converted to vector PDF |

The `fig` files are drawn by `make_figures.py`. The Capella diagrams are exported from the model as SVG (`capella/diagrams/` in the repository) and converted to vector PDF in `figures/capella/`; the report shows the Operational Architecture Blank in Section 3 (Operational analysis) and all the others in its appendix.
