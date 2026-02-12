from datetime import datetime, timedelta
from appointments.models import Appointment

def generate_slots(doctor, date, slot_minutes=30):
    """
    Generate available slots for a doctor ona given date
    """
    if doctor.available_from is None or doctor.available_to is None:
        raise ValueError(f"Doctor {doctor} availability not set")
    
    start = datetime.combine(date, doctor.available_from)
    end = datetime.combine(date, doctor.available_to)

    #Existig bookings
    booked = Appointment.objects.filter(
        doctor=doctor,
        appointment_date = date
    ).values_list("appointment_time", flat=True)

    slots = []

    current = start

    while current < end:
        time_value = current.time()

        if time_value not in booked:
            slots.append(time_value)

        current += timedelta(minutes=slot_minutes)

    return slots