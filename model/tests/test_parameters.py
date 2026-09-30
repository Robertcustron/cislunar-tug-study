"""Tests for parameter loading and traceability metadata."""

import pytest

from cislunar_tug.parameters import Parameter, ParameterError


def test_every_parameter_is_traceable(params):
    for p in params.parameters.values():
        assert p.ref and p.source and p.unit


def test_recorded_path_is_not_absolute(params):
    assert not params.source_file.startswith("/")
    assert ":" not in params.source_file  # no Windows drive letters


def test_override_is_marked_and_does_not_mutate(params):
    changed = params.with_overrides(thrust=2.0)
    assert changed.value("thrust") == 2.0
    assert changed["thrust"].ref.endswith("(override)")
    assert params.value("thrust") == 1.05


def test_unknown_parameter_raises(params):
    with pytest.raises(ParameterError):
        params.with_overrides(not_a_parameter=1.0)


def test_bad_unit_rejected():
    with pytest.raises(ParameterError):
        Parameter("x", 1.0, "furlongs", "A-01", "test")
