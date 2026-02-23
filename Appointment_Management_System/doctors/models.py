from django.db import models
from accounts.models import User
from clinics.models import Clinic

# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.CASCADE
    )

    specialization = models.CharField(max_length=100)
    available_from = models.TimeField()
    available_to = models.TimeField()

    def __str__(self):
        return self.user.get_full_name()