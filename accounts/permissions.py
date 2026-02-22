from rest_framework.permissions import BasePermission


def has_role(user, roles):
    return user.is_authenticated and user.role in roles


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return has_role(request.user, ["SUPER_ADMIN"])


class IsClinicAdmin(BasePermission):
    def has_permission(self, request, view):
        return has_role(request.user, ["CLINIC_ADMIN"])


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return has_role(request.user, ["DOCTOR"])


class IsReceptionist(BasePermission):
    def has_permission(self, request, view):
        return has_role(request.user, ["RECEPTIONIST"])


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return has_role(request.user, ["PATIENT"])