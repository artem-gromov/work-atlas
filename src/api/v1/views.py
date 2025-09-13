from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from rest_framework import permissions, viewsets, generics

from companies.models import Company
from profiles.models import EmployeeProfile
from tenancy.models import Domain, Tenant

from .serializers import CompanySerializer, EmployeeProfileSerializer, TenantCreateSerializer
from .permissions import IsOwnerOrAdmin


class TenantCreateAPIView(generics.CreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantCreateSerializer
    permission_classes = [permissions.AllowAny]

    @transaction.atomic
    def perform_create(self, serializer):
        data = serializer.validated_data
        tenant = Tenant(
            schema_name=data["schema_name"],
            name=data["name"],
            domain_url=data["domain_url"],
        )
        tenant.save()
        Domain(domain=data["domain_url"], tenant=tenant, is_primary=True).save()
        user_model = get_user_model()
        admin = user_model.objects.create_user(
            username=data["admin_email"], email=data["admin_email"], password=data["admin_password"]
        )
        Group.objects.get_or_create(name="TENANT_ADMIN")
        admin.groups.add(Group.objects.get(name="TENANT_ADMIN"))


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeProfileSerializer
    queryset = EmployeeProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]


class CompanyView(generics.RetrieveAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Company.objects.first()

