import csv
import io

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db import transaction
from django.db.models import Q
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, parsers, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from companies.models import Company
from profiles.models import EmployeeProfile
from tenancy.models import Domain, Tenant

from .permissions import IsOwnerOrAdmin, IsTenantAdmin
from .serializers import (
    CompanySerializer,
    EmployeeProfileSerializer,
    RegisterSerializer,
    TenantCreateSerializer,
)


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
            email=data["admin_email"], password=data["admin_password"], is_staff=True
        )
        Group.objects.get_or_create(name="TENANT_ADMIN")
        admin.groups.add(Group.objects.get(name="TENANT_ADMIN"))


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = self.object
        uid = urlsafe_base64_encode(str(user.pk).encode())
        token = default_token_generator.make_token(user)
        verify_url = request.build_absolute_uri(
            reverse("api-v1:auth-verify") + f"?uid={uid}&token={token}"
        )
        from django.core.mail import send_mail

        send_mail(
            "Verify your email",
            f"Click the link to verify: {verify_url}",
            getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com"),
            [user.email],
        )
        refresh = RefreshToken.for_user(user)
        response.data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return response

    def perform_create(self, serializer):
        self.object = serializer.save()


class VerifyEmailAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        uid = request.query_params.get("uid")
        token = request.query_params.get("token")
        try:
            uid = int(urlsafe_base64_decode(uid).decode())
            user = get_user_model().objects.get(pk=uid)
        except Exception:
            return Response({"detail": "invalid"}, status=status.HTTP_400_BAD_REQUEST)
        if default_token_generator.check_token(user, token):
            user.is_email_verified = True
            user.save(update_fields=["is_email_verified"])
            return Response({"detail": "verified"})
        return Response({"detail": "invalid"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        qs = EmployeeProfile.objects.filter(visible=True, is_active=True)
        q = self.request.query_params.get("q")
        city = self.request.query_params.get("city")
        country = self.request.query_params.get("country")
        near = self.request.query_params.get("near")
        radius = self.request.query_params.get("radius_km")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(user__email__icontains=q))
        if city:
            qs = qs.filter(city__iexact=city)
        if country:
            qs = qs.filter(country__iexact=country)
        if near and radius:
            try:
                lat, lon = map(float, near.split(","))
                point = Point(lon, lat)
                qs = (
                    qs.filter(location__distance_lte=(point, D(km=float(radius))))
                    .annotate(distance=Distance("location", point))
                    .order_by("distance")
                )
            except Exception:
                pass
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CompanyView(generics.RetrieveUpdateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsTenantAdmin]

    def get_object(self):
        return Company.objects.get(tenant=self.request.tenant)


class EmployeeImportAPIView(generics.GenericAPIView):
    permission_classes = [IsTenantAdmin]
    parser_classes = [parsers.MultiPartParser]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        if not file:
            return Response(
                {"detail": "file required"}, status=status.HTTP_400_BAD_REQUEST
            )
        decoded = file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(decoded))
        user_model = get_user_model()
        for row in reader:
            email = row["email"]
            user, created = user_model.objects.get_or_create(
                email=email,
                defaults={"password": user_model.objects.make_random_password()},
            )
            if created:
                from django.core.mail import send_mail

                send_mail(
                    "Invitation",
                    "You have been invited to WorkAtlas",
                    getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com"),
                    [email],
                )
            defaults = {
                "title": row.get("title", ""),
                "city": row.get("city", ""),
                "country": row.get("country", ""),
            }
            if row.get("lat") and row.get("lon"):
                defaults["location"] = Point(float(row["lon"]), float(row["lat"]))
            EmployeeProfile.objects.update_or_create(user=user, defaults=defaults)
        return Response({"detail": "imported"})
