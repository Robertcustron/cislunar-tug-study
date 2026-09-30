"""Regression tests: the model must reproduce every number stated in TUG-MDN-001 Issue 2.

If one of these fails after a parameter change, either the document or the
parameter file must be updated so they agree again.
"""

import pytest

from cislunar_tug.baseline import build_baseline_log
from cislunar_tug.mission import MissionInputs
from cislunar_tug.trades import thrust_sweep
from cislunar_tug.traceability import CheckStatus


@pytest.fixture(scope="module")
def log(params):
    return build_baseline_log(params)


def test_no_discrepancies_with_document(log):
    bad = [f"{c.calc_id} {c.title}: {c.value:.4g} vs {c.mdn_value}" for c in log.discrepancies()]
    assert not bad, "Model and MDN disagree:\n" + "\n".join(bad)


def test_calculation_ids_are_unique(log):
    ids = [c.calc_id for c in log.calculations]
    assert len(ids) == len(set(ids))


def test_every_calculation_lists_inputs(log):
    for calc in log.calculations:
        assert calc.inputs, calc.calc_id
        assert calc.formula, calc.calc_id


def test_key_figures(log):
    assert log["CALC-07"].value == pytest.approx(2.49, abs=0.01)  # t xenon per round trip
    assert log["CALC-09"].value == pytest.approx(430, abs=1)  # days outbound
    assert log["CALC-10"].value == pytest.approx(234, abs=1)  # days return
    assert log["CALC-12"].value == 7  # trips in 15 years
    assert log["CALC-12"].status is CheckStatus.MATCH


# MDN §6.3 table: thrust -> (power kW, outbound d, return d, round trip yr, trips)
MDN_TABLE_6_3 = {
    1.05: (18, 430, 234, 2.0, 7),
    1.5: (26, 301, 164, 1.4, 10),
    2.0: (34, 226, 123, 1.1, 13),
    3.0: (51, 151, 82, 0.8, 18),
}


@pytest.mark.parametrize("thrust", sorted(MDN_TABLE_6_3))
def test_table_6_3(params, thrust):
    power, out_d, ret_d, rt_yr, trips = MDN_TABLE_6_3[thrust]
    (row,) = thrust_sweep(MissionInputs.from_parameters(params), [thrust])
    assert row["power_kw"] == pytest.approx(power, abs=0.6)
    assert row["outbound_days"] == pytest.approx(out_d, abs=1)
    assert row["return_days"] == pytest.approx(ret_d, abs=1)
    assert row["round_trip_years"] == pytest.approx(rt_yr, abs=0.05)
    assert row["trips_in_life"] == trips
