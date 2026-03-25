from datetime import datetime, timedelta
from appointments.models import Appointment, DoctorSchedule, DoctorUnavailable


def generate_slots(doctor, date):
    """
    Advanced slot generator using:
    - Weekly schedules
    - Slot duration
    - Unavailability rules
    - Existing bookings
    """

    # -------- 1. Get weekday schedule --------
    weekday = date.weekday()

    try:
        schedule = DoctorSchedule.objects.get(
            doctor=doctor,
            weekday=weekday,
            is_active=True
        )
    except DoctorSchedule.DoesNotExist:
        return []

    start_time = schedule.start_time
    end_time = schedule.end_time
    duration = schedule.slot_duration

    # -------- 2. Full-day unavailability --------
    if DoctorUnavailable.objects.filter(
        doctor=doctor,
        date=date,
        is_full_day=True
    ).exists():
        return []

    # -------- 3. Generate raw slots --------
    slots = []

    current = datetime.combine(date, start_time)
    end = datetime.combine(date, end_time)

    while current + timedelta(minutes=duration) <= end:
        slots.append(current.time())
        current += timedelta(minutes=duration)

    # -------- 4. Remove partial unavailable blocks --------
    partial_blocks = DoctorUnavailable.objects.filter(
        doctor=doctor,
        date=date,
        is_full_day=False
    )

    for block in partial_blocks:
        slots = [
            s for s in slots
            if not (block.start_time <= s < block.end_time)
        ]

    # -------- 5. Remove booked slots (important) --------
    booked_slots = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=date
    ).exclude(status="CANCELED").values_list(
        "appointment_time", flat=True
    )

    slots = [s for s in slots if s not in booked_slots]

    return sorted(slots)