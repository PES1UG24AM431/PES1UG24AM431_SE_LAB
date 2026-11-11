import pytest
from hypothesis import given, strategies as st
from irrigation_scheduler import parse_zone, moisture_average, water_needed


@given(st.text() | st.none())
def test_parse_zone_no_unexpected_crash(s):
    try:
        result = parse_zone(s)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert result[1] > 0
    except ValueError:
        pass


@given(st.text() | st.none())
def test_moisture_average_no_unexpected_crash(s):
    try:
        result = moisture_average(s)
        assert isinstance(result, int)
        assert 0 <= result <= 100
    except ValueError:
        pass


@given(st.text() | st.none())
def test_water_needed_no_unexpected_crash(s):
    try:
        result = water_needed(s)
        assert isinstance(result, (int, float))
        assert result >= 0
    except ValueError:
        pass