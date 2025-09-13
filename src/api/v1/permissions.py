from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.groups.filter(name="TENANT_ADMIN").exists():
            return True
        return obj.user == request.user


class IsTenantAdmin(permissions.BasePermission):
    """Allow access only to users belonging to TENANT_ADMIN group."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.groups.filter(name="TENANT_ADMIN").exists()
        )
