from django.contrib.auth import get_user_model
from rest_framework import serializers

from companies.models import Company
from profiles.models import EmployeeProfile
from tenancy.models import Tenant


class TenantCreateSerializer(serializers.ModelSerializer):
    admin_email = serializers.EmailField(write_only=True)
    admin_password = serializers.CharField(write_only=True)

    class Meta:
        model = Tenant
        fields = ["name", "domain_url", "schema_name", "admin_email", "admin_password"]


class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = ["id", "user", "title", "location", "city", "country", "precision", "visible"]


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["brand_name", "logo"]

