import math
import pytest
from django.contrib.gis.geos import Point

from accounts.models import User
from api.v1.serializers import EmployeeProfileSerializer
from profiles.models import EmployeeProfile


def haversine(a, b):
    lat1, lon1 = a.y, a.x
    lat2, lon2 = b.y, b.x
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    h = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return 2 * 6371 * math.asin(math.sqrt(h))


@pytest.mark.django_db
def test_city_precision_randomizes_location_within_radius():
    user = User.objects.create_user(email="city@example.com", password="pwd")
    original = Point(1, 2)
    profile = EmployeeProfile.objects.create(
        user=user,
        location=original,
        city="NY",
        country="US",
        precision="CITY",
    )
    data1 = EmployeeProfileSerializer(profile).data
    data2 = EmployeeProfileSerializer(profile).data
    assert "location" in data1
    assert "location" in data2
    p1 = Point(*data1["location"]["coordinates"])  # type: ignore[arg-type]
    p2 = Point(*data2["location"]["coordinates"])  # type: ignore[arg-type]
    assert p1 != original
    assert p2 != original
    assert p1 != p2
    assert haversine(original, p1) <= 5
    assert haversine(original, p2) <= 5


@pytest.mark.django_db
def test_exact_precision_keeps_location():
    user = User.objects.create_user(email="exact@example.com", password="pwd")
    profile = EmployeeProfile.objects.create(
        user=user,
        location=Point(3, 4),
        city="NY",
        country="US",
        precision="EXACT",
    )
    data = EmployeeProfileSerializer(profile).data
    assert "location" in data
    assert data["location"] is not None
