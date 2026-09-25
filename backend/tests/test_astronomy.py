from datetime import datetime

import pytest

from app.core.astronomy import calculate_karana, calculate_tithi, calculate_yoga


@pytest.mark.parametrize(
    ("elongation", "name", "paksha"),
    [
        (174, "Purnima", "Shukla"),
        (186, "Pratipada", "Krishna"),
        (342, "Chaturdashi", "Krishna"),
        (354, "Amavasya", "Krishna"),
        (6, "Pratipada", "Shukla"),
    ],
)
def test_tithi_names_follow_lunar_month_boundaries(elongation, name, paksha):
    result = calculate_tithi(datetime(2026, 1, 1), sun_lon=0, moon_lon=elongation)

    assert result["name"] == name
    assert result["paksha"] == paksha


@pytest.mark.parametrize(
    ("elongation", "name"),
    [
        (0, "Kimstughna"),
        (6, "Bava"),
        (12, "Balava"),
        (339, "Vishti"),
        (342, "Shakuni"),
        (348, "Chatushpada"),
        (354, "Naga"),
        (359.9, "Naga"),
    ],
)
def test_karana_sequence_includes_fixed_and_repeating_names(elongation, name):
    result = calculate_karana(datetime(2026, 1, 1), sun_lon=0, moon_lon=elongation)

    assert result["name"] == name


def test_yoga_uses_sidereal_longitude_sum_and_standard_name():
    result = calculate_yoga(datetime(2026, 1, 1), sun_lon=27, moon_lon=27)

    assert result["yoga_index"] == 0
    assert result["name"] == "Vishkambha"