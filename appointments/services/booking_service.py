from datetime import datetime, date
from django.core.exceptions import ValidationError
from appointments.models import Appointment
from .slot_engine import generate_slots


def create_booking(validated_data):

    doctor = validated_data["doctor"]
    booking_date = validated_data["appointment_date"]
    booking_time = validated_data["appointment_time"]

    # ---------- Rule 1: No past booking ----------
    if booking_date < date.today():
        raise ValidationError("Cannot book past dates")

    # ---------- Rule 2: Slot must exist ----------
    available_slots = generate_slots(doctor, booking_date)

    if booking_time not in available_slots:
        raise ValidationError("Invalid or unavailable slot")

    # ---------- Rule 3: Prevent race condition ----------
    exists = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=booking_date,
        appointment_time=booking_time
    ).exists()

    if exists:
        raise ValidationError("Slot already booked")

    # ---------- Create booking ----------
    return Appointment.objects.create(**validated_data)