from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "clinic",
        "doctor",
        "patient",
        "appointment_date",
        "appointment_time",
        "status",
        "created_at",
        )
    search_fields = ("doctor_name", "patient_name", "clinic_name")
    list_filter = ("clinic", "doctor", "status", "appointment_date")
    ordering = ("-appointment_date", "-appointment_time")

