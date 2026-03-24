from datetime import date
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from appointments.models import Appointment
from .slot_engine import generate_slots


@transaction.atomic
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

    # ---------- Rule 3: Prevent race condition (LOCK) ----------
    exists = (
        Appointment.objects
        .select_for_update()   # 🔥 IMPORTANT
        .filter(
            doctor=doctor,
            appointment_date=booking_date,
            appointment_time=booking_time
        )
        .exists()
    )

    if exists:
        raise ValidationError("Slot already booked")

    # ---------- Rule 4: DB-level safety ----------
    try:
        return Appointment.objects.create(**validated_data)

    except IntegrityError:
        # In case 2 requests hit at exact same time
        raise ValidationError("Slot already booked (DB constraint)")