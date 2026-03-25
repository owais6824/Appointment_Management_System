from django.contrib import admin
from .models import Appointment, DoctorSchedule, DoctorUnavailable

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

@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'doctor',
        'weekday',
        'start_time',
        'end_time',
        'slot_duration',
        'is_active'
    )


@admin.register(DoctorUnavailable)
class DoctorUnavailableAdmin(admin.ModelAdmin):
    list_display = (
        'doctor',
        'date',
        'is_full_day',
        'start_time',
        'end_time'
    )