from django.db import models
from clinics.models import Clinic
from doctors.models import Doctor
from patients.models import Patient

class Appointment(models.Model):
    STATUS_CHOICES = (
    ('PENDING', 'Pending'),
    ('CONFIRMED', 'Confirmed'),
    ('COMPLETED', 'Completed'),
    ('CANCELED', 'Canceled'),
    ('NO_SHOW', 'No Show'),
    ('RESCHEDULED', 'Rescheduled'),
)

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date", "appointment_time"],
                name="unique_doctor_slot"
            )
    ]

    def __str__(self):
        return f"{self.doctor} - {self.appointment_date} {self.appointment_time}"
    

class DoctorSchedule(models.Model):
    WEEKDAYS = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )

    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE, related_name='schedules')
    weekday = models.IntegerField(choices=WEEKDAYS)

    start_time = models.TimeField()
    end_time = models.TimeField()

    slot_duration = models.IntegerField(help_text="Duration in minutes (e.g. 15, 30)")

    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('doctor', 'weekday')

    def __str__(self):
        return f"{self.doctor} - {self.get_weekday_display()}"
    

class DoctorUnavailable(models.Model):
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE, related_name='unavailable_dates')

    date = models.DateField()

    reason = models.CharField(max_length=255, blank=True)

    is_full_day = models.BooleanField(default=True)

    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.doctor} unavailable on {self.date}"