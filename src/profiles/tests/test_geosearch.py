import pytest
from django.contrib.gis.geos import Point
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import User
from profiles.models import EmployeeProfile


@pytest.mark.django_db
def test_geosearch_returns_sorted_results_within_radius():
    auth_user = User.objects.create_user(email="auth@example.com", password="pwd")
    u1 = User.objects.create_user(email="p1@example.com", password="pwd")
    u2 = User.objects.create_user(email="p2@example.com", password="pwd")
    u3 = User.objects.create_user(email="p3@example.com", password="pwd")

    p1 = EmployeeProfile.objects.create(
        user=u1, location=Point(0, 0), precision="EXACT"
    )
    p2 = EmployeeProfile.objects.create(
        user=u2, location=Point(1, 0), precision="EXACT"
    )
    EmployeeProfile.objects.create(
        user=u3, location=Point(10, 0), precision="EXACT"
    )

    client = APIClient()
    client.force_authenticate(user=auth_user)
    resp = client.get(
        reverse("api-v1:profile-list"), {"near": "0,0", "radius_km": "200"}
    )
    assert resp.status_code == 200
    ids = [item["id"] for item in resp.data]
    assert ids == [p1.id, p2.id]
