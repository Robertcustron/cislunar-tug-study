"""Trade 2: weighted scoring of refuelling concepts.

The scores are engineering judgement, so they live in a TOML file
(``config/refuelling_trade.toml``) next to their rationale and sources.
This module only checks the file and does the arithmetic, so the ranking
and its sensitivity to the weights can be reproduced and challenged.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

Row = dict[str, float | int | str]


class ScoringError(ValueError):
    """Raised when the scoring file is incomplete or inconsistent."""


@dataclass(frozen=True)
class Option:
    """One refuelling concept with its scores and rationale per criterion."""

    option_id: str
    name: str
    short: str
    scores: Mapping[str, int]
    rationale: Mapping[str, str]


@dataclass(frozen=True)
class ScoringTable:
    """Criteria, options and weight sets of one qualitative trade."""

    criteria: Mapping[str, str]
    weight_sets: Mapping[str, Mapping[str, float]]
    options: tuple[Option, ...]

    def totals(self, weight_set: str = "baseline") -> dict[str, float]:
        """Weighted score per option, on the 1-5 scale."""
        weights = self.weight_sets[weight_set]
        return {
            o.option_id: round(sum(weights[c] * o.scores[c] for c in self.criteria) / 100.0, 3)
            for o in self.options
        }

    def ranking(self, weight_set: str = "baseline") -> list[str]:
        """Option IDs from best to worst for a weight set."""
        totals = self.totals(weight_set)
        return sorted(totals, key=lambda k: (-totals[k], k))


def load_scoring(path: str | Path) -> ScoringTable:
    """Load and validate a scoring file.

    Checks: every option scores every criterion with an integer 1-5 and a
    rationale; every weight set covers all criteria and sums to 100.
    """
    data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    criteria = {cid: c["name"] for cid, c in data["criteria"].items()}
    weight_sets = {"baseline": {cid: float(c["weight"]) for cid, c in data["criteria"].items()}}
    for name, w in data.get("sensitivity", {}).items():
        weights = {c: float(v) for c, v in w.items()}
        if name == "baseline" and weights != weight_sets["baseline"]:
            raise ScoringError("Sensitivity set 'baseline' differs from the criteria weights.")
        weight_sets[name] = weights
    for name, weights in weight_sets.items():
        if set(weights) != set(criteria):
            raise ScoringError(f"Weight set '{name}' does not cover exactly the criteria {sorted(criteria)}.")
        if abs(sum(weights.values()) - 100.0) > 0.05:
            raise ScoringError(f"Weight set '{name}' sums to {sum(weights.values()):.2f}, not 100.")
    options = []
    for oid, o in data["options"].items():
        scores, rationale = {}, {}
        for cid in criteria:
            if cid not in o["scores"]:
                raise ScoringError(f"Option {oid} has no score for {cid}.")
            value, why = o["scores"][cid]
            if not isinstance(value, int) or not 1 <= value <= 5:
                raise ScoringError(f"Option {oid} {cid}: score must be an integer 1-5, got {value!r}.")
            if not str(why).strip():
                raise ScoringError(f"Option {oid} {cid}: missing rationale.")
            scores[cid], rationale[cid] = value, str(why)
        options.append(Option(oid, o["name"], o.get("short", o["name"]), scores, rationale))
    return ScoringTable(criteria, weight_sets, tuple(options))


def score_rows(table: ScoringTable) -> list[Row]:
    """Scores per option and criterion, with the baseline weighted total."""
    totals = table.totals()
    rows: list[Row] = []
    for o in table.options:
        row: Row = {"option": o.option_id, "name": o.short}
        row.update({cid: o.scores[cid] for cid in table.criteria})
        row["weighted_total"] = totals[o.option_id]
        rows.append(row)
    return rows


def sensitivity_rows(table: ScoringTable) -> list[Row]:
    """Weighted total of every option under every weight set, plus the winner."""
    rows: list[Row] = []
    for name in table.weight_sets:
        totals = table.totals(name)
        row: Row = {"weight_set": name}
        row.update(totals)
        row["first"] = table.ranking(name)[0]
        rows.append(row)
    return rows
