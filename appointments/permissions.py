from rest_framework.permissions import BasePermission

class IsDoctor(BasePermission):
    """
    Allows access only to users with role DOCTOR.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'DOCTOR')
    
class IsDoctorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['DOCTOR', 'SUPER_ADMIN']
        )