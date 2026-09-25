from datetime import datetime

import pytest

from app.core.astronomy import calculate_karana, calculate_tithi, calculate_yoga
from app.services.panchanga_service import get_cosmic_panchanga


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


def test_cosmic_payload_has_traceable_positions_for_all_nine_bodies():
    result = get_cosmic_panchanga(datetime(2026, 9, 25, 12, 0))

    assert result["ayanamsha"] == "Lahiri"
    assert len(result["planets"]) == 9
    assert {planet["name"] for planet in result["planets"]} == {
        "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"
    }
    assert all(0 <= planet["longitude"] < 360 for planet in result["planets"])
    assert all(1 <= planet["pada"] <= 4 for planet in result["planets"])