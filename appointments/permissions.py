from rest_framework.permissions import BasePermission
from accounts.models import User


class IsAuthenticatedAndRole(BasePermission):
    """
    Base role checker.
    Usage: Inherit and define allowed_roles.
    """
    allowed_roles = []

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in self.allowed_roles
        )


class IsSuperAdmin(IsAuthenticatedAndRole):
    allowed_roles = [User.SUPER_ADMIN]


class IsClinicAdmin(IsAuthenticatedAndRole):
    allowed_roles = [User.CLINIC_ADMIN]


class IsDoctor(IsAuthenticatedAndRole):
    allowed_roles = [User.DOCTOR]


class IsReceptionist(IsAuthenticatedAndRole):
    allowed_roles = [User.RECEPTIONIST]


class IsPatient(IsAuthenticatedAndRole):
    allowed_roles = [User.PATIENT]


class IsDoctorOrAdmin(IsAuthenticatedAndRole):
    allowed_roles = [
        User.DOCTOR,
        User.SUPER_ADMIN,
        User.CLINIC_ADMIN
    ]