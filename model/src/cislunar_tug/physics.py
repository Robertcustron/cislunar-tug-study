"""Pure physics functions: rocket equation, electric propulsion, orbits.

All functions are stateless, take SI-based inputs and are unit-tested
independently of any mission assumption.
"""

from __future__ import annotations

import math
from typing import Callable

from .constants import G0, MU_EARTH_KM3_S2, MU_MOON_KM3_S2, R_EARTH_KM, R_MOON_KM


# --------------------------------------------------------------- propulsion
def exhaust_velocity(isp_s: float) -> float:
    """Effective exhaust velocity ``v_e = Isp * g0`` [m/s]."""
    _require_positive(isp_s=isp_s)
    return isp_s * G0


def jet_power(thrust_n: float, isp_s: float, efficiency: float) -> float:
    """Electric input power needed for a given thrust [W].

    ``P = T * v_e / (2 * eta)``, where eta is the thruster total efficiency
    (jet power over electrical input power).
    """
    _require_positive(thrust_n=thrust_n, efficiency=efficiency)
    if efficiency > 1.0:
        raise ValueError(f"efficiency must be <= 1, got {efficiency}")
    return thrust_n * exhaust_velocity(isp_s) / (2.0 * efficiency)


def thrust_from_power(power_w: float, isp_s: float, efficiency: float) -> float:
    """Inverse of :func:`jet_power`: ``T = 2 * eta * P / v_e`` [N]."""
    _require_positive(power_w=power_w, efficiency=efficiency)
    return 2.0 * efficiency * power_w / exhaust_velocity(isp_s)


def mass_flow_rate(thrust_n: float, isp_s: float) -> float:
    """Propellant mass flow ``mdot = T / v_e`` [kg/s]."""
    _require_positive(thrust_n=thrust_n)
    return thrust_n / exhaust_velocity(isp_s)


def propellant_for_dv_from_final(final_mass_kg: float, dv_m_s: float, isp_s: float) -> float:
    """Propellant needed to give ``dv`` to a vehicle of known *final* mass [kg].

    Tsiolkovsky: ``m_p = m_f * (exp(dv / v_e) - 1)``.
    """
    _require_positive(final_mass_kg=final_mass_kg)
    _require_non_negative(dv_m_s=dv_m_s)
    return final_mass_kg * math.expm1(dv_m_s / exhaust_velocity(isp_s))


def propellant_for_dv_from_initial(initial_mass_kg: float, dv_m_s: float, isp_s: float) -> float:
    """Propellant needed to give ``dv`` to a vehicle of known *initial* mass [kg].

    Tsiolkovsky: ``m_p = m_0 * (1 - exp(-dv / v_e))``.
    """
    _require_positive(initial_mass_kg=initial_mass_kg)
    _require_non_negative(dv_m_s=dv_m_s)
    return -initial_mass_kg * math.expm1(-dv_m_s / exhaust_velocity(isp_s))


def burn_time(propellant_kg: float, thrust_n: float, isp_s: float) -> float:
    """Thrusting time to expel ``propellant_kg`` at constant thrust and Isp [s].

    Exact for constant ``mdot``: ``t = m_p / mdot``.
    """
    _require_non_negative(propellant_kg=propellant_kg)
    return propellant_kg / mass_flow_rate(thrust_n, isp_s)


# --------------------------------------------------------------- lunar orbits
def circular_speed_moon(altitude_km: float) -> float:
    """Circular orbit speed around the Moon [m/s]: ``v = sqrt(mu / r)``."""
    _require_non_negative(altitude_km=altitude_km)
    radius_km = R_MOON_KM + altitude_km
    return math.sqrt(MU_MOON_KM3_S2 / radius_km) * 1_000.0


def orbital_period_moon(altitude_km: float) -> float:
    """Circular orbit period around the Moon [s]: ``T = 2 pi sqrt(r^3 / mu)``."""
    _require_non_negative(altitude_km=altitude_km)
    radius_km = R_MOON_KM + altitude_km
    return 2.0 * math.pi * math.sqrt(radius_km**3 / MU_MOON_KM3_S2)


def max_eclipse_fraction_moon(altitude_km: float) -> float:
    """Worst-case (beta angle = 0) eclipse fraction of a circular lunar orbit [-].

    Cylindrical shadow model: the spacecraft is in shadow while its angle from
    the anti-Sun direction is below ``asin(R / r)``, so the fraction is
    ``2 * asin(R / r) / (2 pi)``. Penumbra is ignored.
    """
    _require_non_negative(altitude_km=altitude_km)
    radius_km = R_MOON_KM + altitude_km
    return math.asin(R_MOON_KM / radius_km) / math.pi


# --------------------------------------------------------------- Earth orbits
def apoapsis_speed_earth(perigee_alt_km: float, apogee_alt_km: float) -> float:
    """Speed at apogee of an Earth orbit [m/s], from the vis-viva equation."""
    _require_non_negative(perigee_alt_km=perigee_alt_km)
    if apogee_alt_km < perigee_alt_km:
        raise ValueError("apogee must not be below perigee")
    r_p = R_EARTH_KM + perigee_alt_km
    r_a = R_EARTH_KM + apogee_alt_km
    a = 0.5 * (r_p + r_a)
    return math.sqrt(MU_EARTH_KM3_S2 * (2.0 / r_a - 1.0 / a)) * 1_000.0


def orbital_period_earth(perigee_alt_km: float, apogee_alt_km: float) -> float:
    """Period of an Earth orbit [s]: ``T = 2 pi sqrt(a^3 / mu)``."""
    a = R_EARTH_KM + 0.5 * (perigee_alt_km + apogee_alt_km)
    return 2.0 * math.pi * math.sqrt(a**3 / MU_EARTH_KM3_S2)


def max_eclipse_at_apogee_earth(perigee_alt_km: float, apogee_alt_km: float) -> float:
    """Longest eclipse of an Earth orbit whose apogee lies in the shadow [s].

    Cylindrical shadow, apogee on the anti-Sun line: the spacecraft crosses a
    shadow of width ``2 R_E`` at roughly its apogee speed, so
    ``t = 2 R_E / v_a``. Slightly conservative (the real path curves through
    the shadow) and ignores penumbra.
    """
    return 2.0 * R_EARTH_KM * 1_000.0 / apoapsis_speed_earth(perigee_alt_km, apogee_alt_km)


# --------------------------------------------------------------- numerics
def bisect(
    func: Callable[[float], float],
    lower: float,
    upper: float,
    tolerance: float = 1e-9,
    max_iterations: int = 200,
) -> float:
    """Find a root of a monotonic function on ``[lower, upper]`` by bisection.

    Used instead of a closed form so that inverse questions ("what power gives
    N trips?") still work once dry mass depends on power (trade-offs).
    """
    f_lower, f_upper = func(lower), func(upper)
    if f_lower == 0.0:
        return lower
    if f_upper == 0.0:
        return upper
    if f_lower * f_upper > 0.0:
        raise ValueError(f"Root not bracketed: f({lower})={f_lower:.4g}, f({upper})={f_upper:.4g}")
    for _ in range(max_iterations):
        mid = 0.5 * (lower + upper)
        f_mid = func(mid)
        if abs(upper - lower) < tolerance or f_mid == 0.0:
            return mid
        if f_lower * f_mid < 0.0:
            upper = mid
        else:
            lower, f_lower = mid, f_mid
    raise RuntimeError("Bisection did not converge.")


# --------------------------------------------------------------- guards
def _require_positive(**values: float) -> None:
    for name, value in values.items():
        if not value > 0.0:
            raise ValueError(f"{name} must be > 0, got {value}")


def _require_non_negative(**values: float) -> None:
    for name, value in values.items():
        if value < 0.0:
            raise ValueError(f"{name} must be >= 0, got {value}")
