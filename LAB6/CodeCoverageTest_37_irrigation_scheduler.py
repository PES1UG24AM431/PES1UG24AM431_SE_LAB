
import pytest
from irrigation_scheduler import should_irrigate, water_volume, schedule


def test_wet_soil_no_irrigation():
    assert should_irrigate(70, 0, "seedling") is False


def test_heavy_rain_no_irrigation():
    assert should_irrigate(20, 10, "flowering") is False


def test_seedling_dry_soil():
    assert should_irrigate(30, 0, "seedling") is True


def test_seedling_not_dry_enough():
    assert should_irrigate(45, 0, "seedling") is False


def test_flowering_needs_water():
    assert should_irrigate(50, 0, "flowering") is True


def test_flowering_does_not_need_water():
    assert should_irrigate(55, 0, "flowering") is False


def test_other_stage_rain_at_least_five():
    assert should_irrigate(30, 5, "mature") is False


def test_other_stage_dry_soil():
    assert should_irrigate(30, 0, "mature") is True


def test_other_stage_moisture_boundary():
    assert should_irrigate(40, 0, "mature") is False


def test_seedling_water_volume():
    assert water_volume(10, "seedling", 20) == 20


def test_flowering_water_volume():
    assert water_volume(2, "flowering", 20) == 10


def test_other_stage_water_volume():
    assert water_volume(2, "mature", 20) == 8


def test_invalid_area_zero():
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(0, "seedling", 20)


def test_invalid_area_negative():
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(-1, "seedling", 20)


def test_high_temperature_multiplier():
    assert water_volume(2, "seedling", 36) == 6


def test_low_temperature_multiplier():
    assert water_volume(2, "seedling", 9) == 2


def test_schedule_adds_irrigated_zone():
    zones = [("Zone A", 2, 30, 0, "seedling", 20)]
    assert schedule(zones, 10) == ["Zone A"]


def test_schedule_skips_zone_that_does_not_need_water():
    zones = [("Zone A", 2, 70, 0, "seedling", 20)]
    assert schedule(zones, 10) == []


def test_schedule_stops_when_budget_is_insufficient():
    zones = [
        ("Zone A", 2, 30, 0, "seedling", 20),
        ("Zone B", 2, 30, 0, "seedling", 20),
    ]
    assert schedule(zones, 3) == []


def test_schedule_uses_exact_budget():
    zones = [("Zone A", 2, 30, 0, "seedling", 20)]
    assert schedule(zones, 4) == ["Zone A"]


def test_schedule_empty_zones():
    assert schedule([], 10) == []
