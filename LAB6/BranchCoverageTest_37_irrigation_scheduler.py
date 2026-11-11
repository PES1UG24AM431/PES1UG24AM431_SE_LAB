
import pytest
from irrigation_scheduler import should_irrigate, water_volume, schedule


# should_irrigate: exercise both outcomes of every decision.
@pytest.mark.parametrize(
    "moisture,rain,stage,expected",
    [
        (60, 0, "seedling", False),
        (30, 0, "seedling", True),
        (30, 10, "flowering", False),
        (30, 0, "seedling", True),
        (45, 0, "seedling", False),
        (44, 0, "seedling", True),
        (54, 0, "flowering", True),
        (55, 0, "flowering", False),
        (30, 5, "mature", False),
        (30, 0, "mature", True),
        (40, 0, "mature", False),
    ],
)
def test_should_irrigate_all_branches(moisture, rain, stage, expected):
    assert should_irrigate(moisture, rain, stage) is expected


# water_volume: exercise all branches.
@pytest.mark.parametrize(
    "area,stage,temp,expected",
    [
        (0, "seedling", 20, None),
        (-2, "flowering", 20, None),
        (2, "seedling", 20, 4),
        (2, "flowering", 20, 10),
        (2, "mature", 20, 8),
        (2, "seedling", 36, 6),
        (2, "seedling", 9, 2),
        (2, "seedling", 35, 4),
        (2, "seedling", 10, 4),
    ],
)
def test_water_volume_all_branches(area, stage, temp, expected):
    if expected is None:
        with pytest.raises(ValueError, match="invalid area"):
            water_volume(area, stage, temp)
    else:
        assert water_volume(area, stage, temp) == expected


# schedule: exercise loop, continue, append, break and completion.
def test_schedule_empty_list_loop_not_entered():
    assert schedule([], 10) == []


def test_schedule_continue_then_append_and_finish():
    zones = [
        ("Wet", 2, 70, 0, "seedling", 20),
        ("Needs water", 2, 30, 0, "seedling", 20),
    ]
    assert schedule(zones, 4) == ["Needs water"]


def test_schedule_break_when_need_exceeds_budget():
    zones = [("Too expensive", 2, 30, 0, "seedling", 20)]
    assert schedule(zones, 3) == []


def test_schedule_exact_budget_and_continue_loop():
    zones = [
        ("First", 2, 30, 0, "seedling", 20),
        ("Second", 2, 70, 0, "seedling", 20),
    ]
    assert schedule(zones, 4) == ["First"]
