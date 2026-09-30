"""Loading, validating and overriding study parameters.

Every numeric input to the model is a :class:`Parameter` read from a TOML
file. Each parameter carries its unit, a traceability reference into the
Mission Definition Note (A-xx, C-x, D-xx or a section number) and a source.
Model code never contains study assumptions as literals.
"""

from __future__ import annotations

import hashlib
import tomllib
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Mapping

ALLOWED_UNITS: frozenset[str] = frozenset({"kg", "m/s", "s", "N", "W", "days", "years", "hours", "km", "-"})


class ParameterError(ValueError):
    """Raised when a parameter file is incomplete or inconsistent."""


@dataclass(frozen=True)
class Parameter:
    """A single traceable model input."""

    name: str
    value: float
    unit: str
    ref: str
    source: str

    def __post_init__(self) -> None:
        if self.unit not in ALLOWED_UNITS:
            raise ParameterError(
                f"Parameter '{self.name}' has unknown unit '{self.unit}'. Allowed: {sorted(ALLOWED_UNITS)}"
            )
        if not self.ref.strip():
            raise ParameterError(f"Parameter '{self.name}' has no traceability ref.")
        if not self.source.strip():
            raise ParameterError(f"Parameter '{self.name}' has no source.")


@dataclass(frozen=True)
class ParameterSet:
    """An immutable, named collection of parameters plus trade settings."""

    parameters: Mapping[str, Parameter]
    trades: Mapping[str, Any]
    meta: Mapping[str, Any]
    source_file: str = "<in-memory>"
    source_sha256: str = ""

    def __getitem__(self, name: str) -> Parameter:
        try:
            return self.parameters[name]
        except KeyError as exc:
            raise ParameterError(f"Unknown parameter '{name}'.") from exc

    def value(self, name: str) -> float:
        """Return the numeric value of parameter ``name``."""
        return self[name].value

    def with_overrides(self, **overrides: float) -> ParameterSet:
        """Return a copy with some values replaced.

        The ref of an overridden parameter is suffixed with ``(override)`` so
        that every saved result shows it did not come from the baseline file.
        """
        updated = dict(self.parameters)
        for name, new_value in overrides.items():
            old = self[name]
            updated[name] = replace(
                old,
                value=float(new_value),
                ref=old.ref if old.ref.endswith("(override)") else f"{old.ref} (override)",
            )
        return replace(self, parameters=updated)


def _display_path(path: Path) -> str:
    """Path as recorded in outputs: relative to the project, never absolute.

    Keeps personal folder names out of files that may be published.
    """
    resolved = path.resolve()
    for anchor in (Path.cwd(), *Path.cwd().parents):
        if (anchor / "pyproject.toml").exists() and resolved.is_relative_to(anchor):
            return resolved.relative_to(anchor).as_posix()
    return path.name


def load_parameters(path: str | Path) -> ParameterSet:
    """Load and validate a parameter file.

    Args:
        path: Path to a TOML file with ``[parameters.<name>]`` tables.

    Returns:
        A validated :class:`ParameterSet`.

    Raises:
        ParameterError: If a table is missing a field or has a bad unit.
    """
    path = Path(path)
    raw_bytes = path.read_bytes()
    data = tomllib.loads(raw_bytes.decode("utf-8"))

    raw_params = data.get("parameters")
    if not raw_params:
        raise ParameterError(f"No [parameters] tables found in {path}.")

    parameters: dict[str, Parameter] = {}
    for name, fields in raw_params.items():
        missing = {"value", "unit", "ref", "source"} - fields.keys()
        if missing:
            raise ParameterError(f"Parameter '{name}' is missing {sorted(missing)}.")
        parameters[name] = Parameter(
            name=name,
            value=float(fields["value"]),
            unit=str(fields["unit"]),
            ref=str(fields["ref"]),
            source=str(fields["source"]),
        )

    return ParameterSet(
        parameters=parameters,
        trades=data.get("trades", {}),
        meta=data.get("meta", {}),
        source_file=_display_path(path),
        source_sha256=hashlib.sha256(raw_bytes).hexdigest(),
    )
