from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    SUPER_ADMIN = "SUPER_ADMIN"
    CLINIC_ADMIN = "CLINIC_ADMIN"
    DOCTOR = "DOCTOR"
    RECEPTIONIST = "RECEPTIONIST"
    PATIENT = "PATIENT"

    ROLE_CHOICES = (
        (SUPER_ADMIN, "Super Admin"),
        (CLINIC_ADMIN, "Clinic Admin"),
        (DOCTOR, "Doctor"),
        (RECEPTIONIST, "Receptionist"),
        (PATIENT, "Patient"),
    )

    role = models.CharField(
    max_length=20,
    choices=ROLE_CHOICES,
    default=SUPER_ADMIN
)

    def __str__(self):
        return f"{self.username} ({self.role})"