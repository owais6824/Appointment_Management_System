from datetime import datetime, timedelta
from appointments.models import Appointment


def generate_slots(doctor, date, slot_minutes=30):
    """
    Generate available time slots for doctor on given date
    """

    # -------- Safety Checks --------
    if doctor is None:
        raise ValueError("Doctor cannot be None")

    if doctor.available_from is None or doctor.available_to is None:
        raise ValueError("Doctor availability not configured")

    if doctor.available_from >= doctor.available_to:
        raise ValueError("Invalid availability window")

    # -------- Build Time Range --------
    start = datetime.combine(date, doctor.available_from)
    end = datetime.combine(date, doctor.available_to)

    # -------- Fetch Existing Bookings --------
    booked = set(
        Appointment.objects.filter(
            doctor=doctor,
            appointment_date=date
        )
        .exclude(status="CANCELED")
        .values_list("appointment_time", flat=True)
    )

    # -------- Generate Slots --------
    slots = []
    current = start

    while current < end:
        time_val = current.time()

        if time_val not in booked:
            slots.append(time_val)

        current += timedelta(minutes=slot_minutes)

    return sorted(slots)