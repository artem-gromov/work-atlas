from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.groups.filter(name="TENANT_ADMIN").exists():
            return True
        return obj.user == request.user

