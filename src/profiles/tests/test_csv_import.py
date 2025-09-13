import pytest
from django.contrib.auth.models import Group
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import User
from profiles.models import EmployeeProfile


@pytest.mark.django_db
def test_csv_import_creates_users_profiles_and_sends_emails():
    admin = User.objects.create_user(email="admin@example.com", password="pwd")
    group, _ = Group.objects.get_or_create(name="TENANT_ADMIN")
    admin.groups.add(group)
    client = APIClient()
    client.force_authenticate(user=admin)

    csv_content = (
        "email,title,city,country,lat,lon\n"
        "u1@example.com,Dev,NY,US,0,0\n"
        "u2@example.com,Mgr,,US,,\n"
    )
    upload = SimpleUploadedFile(
        "employees.csv", csv_content.encode("utf-8"), content_type="text/csv"
    )
    resp = client.post(
        reverse("api-v1:employees-import"), {"file": upload}, format="multipart"
    )
    assert resp.status_code == 200
    assert User.objects.filter(email="u1@example.com").exists()
    assert User.objects.filter(email="u2@example.com").exists()
    assert EmployeeProfile.objects.filter(user__email="u1@example.com", city="NY").exists()
    assert EmployeeProfile.objects.filter(user__email="u2@example.com").exists()
    assert len(mail.outbox) == 2
