"""Unit tests for pure physics functions (independent of study assumptions)."""

import math

import pytest

from cislunar_tug import physics
from cislunar_tug.constants import G0


def test_exhaust_velocity():
    assert physics.exhaust_velocity(1000.0) == pytest.approx(1000.0 * G0)


def test_power_and_thrust_are_inverse():
    power = physics.jet_power(1.0, 2000.0, 0.6)
    assert physics.thrust_from_power(power, 2000.0, 0.6) == pytest.approx(1.0)


def test_rocket_equation_forms_agree():
    """Propellant from initial mass equals propellant from the matching final mass."""
    m0, dv, isp = 10_000.0, 2_500.0, 2_100.0
    mp = physics.propellant_for_dv_from_initial(m0, dv, isp)
    assert physics.propellant_for_dv_from_final(m0 - mp, dv, isp) == pytest.approx(mp)


def test_rocket_equation_recovers_dv():
    m0, dv, isp = 5_000.0, 3_000.0, 1_500.0
    mp = physics.propellant_for_dv_from_initial(m0, dv, isp)
    recovered = physics.exhaust_velocity(isp) * math.log(m0 / (m0 - mp))
    assert recovered == pytest.approx(dv)


def test_zero_dv_needs_no_propellant():
    assert physics.propellant_for_dv_from_final(1_000.0, 0.0, 2_000.0) == 0.0


def test_burn_time_is_propellant_over_mass_flow():
    t = physics.burn_time(100.0, 0.5, 2_000.0)
    assert t == pytest.approx(100.0 / (0.5 / (2_000.0 * G0)))


def test_lunar_circular_speed_at_surface():
    # sqrt(4902.8 / 1737.4) km/s = 1.680 km/s
    assert physics.circular_speed_moon(0.0) == pytest.approx(1679.9, abs=0.5)


def test_eclipse_fraction_limits():
    assert physics.max_eclipse_fraction_moon(0.0) == pytest.approx(0.5)
    assert physics.max_eclipse_fraction_moon(1e7) == pytest.approx(0.0, abs=1e-4)


def test_bisect_finds_root():
    assert physics.bisect(lambda x: x**2 - 2.0, 0.0, 2.0) == pytest.approx(math.sqrt(2.0))


def test_bisect_rejects_unbracketed_root():
    with pytest.raises(ValueError):
        physics.bisect(lambda x: x + 10.0, 0.0, 1.0)


@pytest.mark.parametrize(
    "call",
    [
        lambda: physics.exhaust_velocity(0.0),
        lambda: physics.jet_power(1.0, 2000.0, 1.5),
        lambda: physics.propellant_for_dv_from_final(-1.0, 100.0, 2000.0),
    ],
)
def test_invalid_inputs_raise(call):
    with pytest.raises(ValueError):
        call()
