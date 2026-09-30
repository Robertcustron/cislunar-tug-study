"""Shared fixtures."""

from pathlib import Path

import pytest

from cislunar_tug.parameters import ParameterSet, load_parameters

CONFIG = Path(__file__).resolve().parents[1] / "config" / "baseline.toml"


@pytest.fixture(scope="session")
def params() -> ParameterSet:
    return load_parameters(CONFIG)
