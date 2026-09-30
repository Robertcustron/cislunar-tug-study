"""Behavioural tests for the round-trip model."""

import pytest

from cislunar_tug.mission import (
    LinearPowerDryMass,
    MissionInputs,
    max_cargo_per_launch,
    simulate_round_trip,
    thrust_for_trips,
    trips_in_life,
)


@pytest.fixture()
def inputs(params) -> MissionInputs:
    return MissionInputs.from_parameters(params)


def test_mass_bookkeeping_closes(inputs):
    trip = simulate_round_trip(inputs)
    expected = trip.dry_mass_kg + inputs.cargo_outbound_kg + trip.propellant_total_kg
    assert trip.initial_mass_kg == pytest.approx(expected)


def test_transfer_time_scales_inversely_with_thrust(inputs):
    slow = simulate_round_trip(inputs)
    fast = simulate_round_trip(inputs.with_changes(thrust_n=2 * inputs.thrust_n))
    assert fast.transfer_outbound_days == pytest.approx(slow.transfer_outbound_days / 2)
    # Propellant does not depend on thrust while dry mass is constant.
    assert fast.propellant_total_kg == pytest.approx(slow.propellant_total_kg)


def test_more_cargo_needs_more_propellant(inputs):
    light = simulate_round_trip(inputs.with_changes(cargo_outbound_kg=3000.0))
    heavy = simulate_round_trip(inputs.with_changes(cargo_outbound_kg=8000.0))
    assert heavy.propellant_total_kg > light.propellant_total_kg
    # The return leg does not carry outbound cargo.
    assert heavy.propellant_return_kg == pytest.approx(light.propellant_return_kg)


def test_trips_in_life_floors():
    assert trips_in_life(round_trip_days=730.5, design_life_years=15.0) == 7


def test_max_cargo_fills_the_launcher(inputs):
    capacity = 11_500.0
    cargo = max_cargo_per_launch(inputs, capacity)
    trip = simulate_round_trip(inputs.with_changes(cargo_outbound_kg=cargo))
    assert trip.launch_mass_per_trip_kg == pytest.approx(capacity, rel=1e-6)


def test_thrust_for_trips_hits_target(inputs):
    thrust = thrust_for_trips(inputs, trips=10, within_years=15.0)
    trip = simulate_round_trip(inputs.with_changes(thrust_n=thrust))
    assert trip.round_trip_days == pytest.approx(15.0 * 365.25 / 10, rel=1e-6)
    assert trip.trips_in_life == 10


def test_power_dependent_dry_mass_needs_more_power(inputs):
    """Step 4 hook: if arrays get heavier with power, more power is needed for the same trips."""
    constant = thrust_for_trips(inputs, trips=10, within_years=15.0)
    growing = inputs.with_changes(
        dry_mass_model=LinearPowerDryMass(5900.0, 18_000.0, specific_mass_kg_per_w=0.02)
    )
    assert thrust_for_trips(growing, trips=10, within_years=15.0) > constant
