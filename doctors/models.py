from django.db import models
from accounts.models import User
from clinics.models import Clinic


# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    specialization = models.CharField(max_length=100)
    available_from = models.TimeField()
    available_to = models.TimeField()

    def __str__(self):
        # If name is provided, use it; else fallback to user's full name or username
        if self.name:
            return self.name
        full_name = self.user.get_full_name()
        return full_name if full_name.strip() else self.user.username