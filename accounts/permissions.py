from rest_framework.permissions import BasePermission
from accounts.models import User


def has_role(user, allowed_roles):
    """
    Utility function to check if user has one of allowed roles
    """
    return user.is_authenticated and user.role in allowed_roles


# ----------------------------------------
# Individual Role Permissions
# ----------------------------------------

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return has_role(request.user, [User.SUPER_ADMIN])


class IsClinicAdmin(BasePermission):
    def has_permission(self, request, view):
        return has_role(request.user, [User.CLINIC_ADMIN])


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return has_role(request.user, [User.DOCTOR])


class IsReceptionist(BasePermission):
    def has_permission(self, request, view):
        return has_role(request.user, [User.RECEPTIONIST])


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return has_role(request.user, [User.PATIENT])


# ----------------------------------------
# Composite Permissions
# ----------------------------------------

class CanBookAppointment(BasePermission):
    """
    Patient, Receptionist, Clinic Admin can book
    """
    def has_permission(self, request, view):
        return has_role(
            request.user,
            [
                User.PATIENT,
                User.RECEPTIONIST,
                User.CLINIC_ADMIN
            ]
        )


class CanManageClinic(BasePermission):
    """
    Super Admin + Clinic Admin
    """
    def has_permission(self, request, view):
        return has_role(
            request.user,
            [
                User.SUPER_ADMIN,
                User.CLINIC_ADMIN
            ]
        )
    

# ----------------------------------------
# Object Level Permissions
# ----------------------------------------

class IsAppointmentOwnerPatient(BasePermission):
    """
    Patient can access only their own appointment
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == User.PATIENT and
            obj.patient.user == request.user
        )


class IsAppointmentOwnerDoctor(BasePermission):
    """
    Doctor can access only their own appointments
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == User.DOCTOR and
            obj.doctor.user == request.user
        )