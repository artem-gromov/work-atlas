import pytest
from django.contrib.gis.geos import Point

from accounts.models import User
from api.v1.serializers import EmployeeProfileSerializer
from profiles.models import EmployeeProfile


@pytest.mark.django_db
def test_city_precision_hides_location():
    user = User.objects.create_user(email="city@example.com", password="pwd")
    profile = EmployeeProfile.objects.create(
        user=user,
        location=Point(1, 2),
        city="NY",
        country="US",
        precision="CITY",
    )
    data = EmployeeProfileSerializer(profile).data
    assert "location" not in data
    assert data["city"] == "NY"
    assert data["country"] == "US"


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
