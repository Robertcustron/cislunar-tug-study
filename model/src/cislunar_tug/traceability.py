"""Calculation log: every reported number with its formula, inputs and check.

Each :class:`Calculation` records

* a stable ID (``CALC-xx`` for results, ``VAL-xx`` for checks against
  published data) so documents can cite it,
* the formula in words,
* every input with its value, unit and traceability ref (A-xx or CALC-xx),
* where the number appears in the Mission Definition Note and the value
  stated there, so a rerun shows at once whether the document still agrees.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path

from .parameters import ParameterSet


class CheckStatus(str, Enum):
    """Outcome of comparing a computed value with the value in the MDN."""

    MATCH = "MATCH"  # within tolerance of the document value
    DIFFERS = "DIFFERS"  # outside tolerance: document or model must be fixed
    NEW = "NEW"  # not stated in the document (new result)


@dataclass(frozen=True)
class InputRef:
    """One input to a calculation."""

    name: str
    value: float
    unit: str
    ref: str


@dataclass(frozen=True)
class Calculation:
    """One traceable result."""

    calc_id: str
    title: str
    value: float
    unit: str
    formula: str
    inputs: tuple[InputRef, ...]
    mdn_ref: str = ""
    mdn_value: float | None = None
    rel_tolerance: float = 0.03
    note: str = ""

    @property
    def status(self) -> CheckStatus:
        if self.mdn_value is None:
            return CheckStatus.NEW
        if self.mdn_value == 0.0:
            ok = abs(self.value) <= self.rel_tolerance
        else:
            ok = abs(self.value - self.mdn_value) / abs(self.mdn_value) <= self.rel_tolerance
        return CheckStatus.MATCH if ok else CheckStatus.DIFFERS

    def as_input(self, name: str | None = None) -> InputRef:
        """Use this result as an input to a later calculation."""
        return InputRef(name or self.title, self.value, self.unit, self.calc_id)


@dataclass
class CalculationLog:
    """Ordered collection of calculations for one model run."""

    params: ParameterSet
    calculations: list[Calculation] = field(default_factory=list)

    # ------------------------------------------------------------ building
    def param(self, name: str) -> InputRef:
        """Input reference for a configuration parameter."""
        p = self.params[name]
        return InputRef(name, p.value, p.unit, p.ref)

    def add(self, calc: Calculation) -> Calculation:
        if any(c.calc_id == calc.calc_id for c in self.calculations):
            raise ValueError(f"Duplicate calculation ID {calc.calc_id}.")
        self.calculations.append(calc)
        return calc

    def __getitem__(self, calc_id: str) -> Calculation:
        for calc in self.calculations:
            if calc.calc_id == calc_id:
                return calc
        raise KeyError(calc_id)

    # ------------------------------------------------------------ queries
    def discrepancies(self) -> list[Calculation]:
        return [c for c in self.calculations if c.status is CheckStatus.DIFFERS]

    # ------------------------------------------------------------ export
    def to_json(self, path: Path) -> None:
        records = []
        for c in self.calculations:
            record = asdict(c)
            record["status"] = c.status.value
            records.append(record)
        path.write_text(json.dumps(records, indent=2), encoding="utf-8")

    def to_csv(self, path: Path) -> None:
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(
                ["calc_id", "title", "value", "unit", "mdn_ref", "mdn_value", "status", "formula", "inputs"]
            )
            for c in self.calculations:
                inputs = "; ".join(f"{i.name}={_fmt(i.value)} {i.unit} [{i.ref}]" for i in c.inputs)
                writer.writerow(
                    [
                        c.calc_id,
                        c.title,
                        f"{c.value:.6g}",
                        c.unit,
                        c.mdn_ref,
                        "" if c.mdn_value is None else c.mdn_value,
                        c.status.value,
                        c.formula,
                        inputs,
                    ]
                )

    def to_markdown(self, path: Path) -> None:
        lines = [
            "# Calculation log",
            "",
            f"Parameters: `{self.params.source_file}` (sha256 `{self.params.source_sha256[:12]}`)",
            "",
            "Status: **MATCH** = agrees with TUG-MDN-001 within tolerance; "
            "**DIFFERS** = document and model disagree; **NEW** = not in the document.",
            "",
            "## Summary",
            "",
            "| ID | Result | Value | Unit | MDN ref | MDN value | Status |",
            "|---|---|---|---|---|---|---|",
        ]
        for c in self.calculations:
            mdn = "" if c.mdn_value is None else _fmt(c.mdn_value)
            lines.append(
                f"| {c.calc_id} | {c.title} | {_fmt(c.value)} | {c.unit} | {c.mdn_ref} | {mdn} | {c.status.value} |"
            )
        lines += ["", "## Details", ""]
        for c in self.calculations:
            lines += [
                f"### {c.calc_id}: {c.title}",
                "",
                f"- **Result:** {_fmt(c.value)} {c.unit} ({c.status.value})",
                f"- **Formula:** `{c.formula}`",
            ]
            if c.mdn_ref:
                lines.append(f"- **In MDN:** {c.mdn_ref}")
            if c.note:
                lines.append(f"- **Note:** {c.note}")
            lines.append("- **Inputs:**")
            lines += [f"  - {i.name} = {_fmt(i.value)} {i.unit} [{i.ref}]" for i in c.inputs]
            lines.append("")
        path.write_text("\n".join(lines), encoding="utf-8")

    def parameters_to_markdown(self, path: Path) -> None:
        """Write the parameter register used in this run."""
        lines = [
            "# Parameters used",
            "",
            "| Name | Value | Unit | Ref | Source |",
            "|---|---|---|---|---|",
        ]
        for p in self.params.parameters.values():
            lines.append(f"| {p.name} | {_fmt(p.value)} | {p.unit} | {p.ref} | {p.source} |")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _fmt(value: float) -> str:
    """Compact number formatting for reports."""
    if value == 0:
        return "0"
    magnitude = abs(value)
    if magnitude >= 1000:
        return f"{value:,.0f}"
    if magnitude >= 10:
        return f"{value:.1f}"
    if magnitude >= 1:
        return f"{value:.3f}"
    return f"{value:.4g}"
