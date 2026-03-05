from django.utils.timezone import now
from appointments.models import Appointment
from doctors.models import Doctor


def get_doctor_dashboard_data(user):
    doctor = Doctor.objects.get(user=user)

    today = now().date()

    return {
        "total_appointments": Appointment.objects.filter(doctor=doctor).count(),
        "today_appointments": Appointment.objects.filter(
            doctor=doctor,
            appointment_date=today
        ).count(),
        "pending_appointments": Appointment.objects.filter(
            doctor=doctor,
            status="PENDING"
        ).count(),
        "completed_appointments": Appointment.objects.filter(
            doctor=doctor,
            status="COMPLETED"
        ).count(),
    }