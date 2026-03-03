from datetime import date
import calendar
from doctors.models import Doctor
from appointments.models import Appointment
from .slot_engine import generate_slots


def get_doctor_monthly_calender(doctor_id, year, month):
    doctor = Doctor.objects.get(id=doctor_id)

    month_range = calendar.monthrange(year, month)[1]

    calendar_data = []

    for day in range(1, month_range + 1):
        current_date = date(year, month, day)

        # Generate all possible slots
        total_slots_list = generate_slots(doctor, current_date)
        total_slots = len(total_slots_list)

        # Get booked appointments count
        booked_slots = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=current_date
        ).count()

        available_slots = total_slots - booked_slots

        calendar_data.append({
            "date": current_date,
            "total_slots": total_slots,
            "booked_slots": booked_slots,
            "available_slots": available_slots
        })

    return calendar_data