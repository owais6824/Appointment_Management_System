from django.core.exceptions import ValidationError
from appointments.models import Appointment


# -------------------------------
# Allowed Transitions
# -------------------------------
ALLOWED_TRANSITIONS = {
    "PENDING": ["CONFIRMED", "CANCELED"],
    "CONFIRMED": ["COMPLETED", "CANCELED", "RESCHEDULED", "NO_SHOW"],
    "RESCHEDULED": ["CONFIRMED", "CANCELED"],
    "COMPLETED": [],
    "CANCELED": [],
    "NO_SHOW": [],
}


# -------------------------------
# Validate Transition
# -------------------------------
def validate_transition(current_status, new_status):
    allowed = ALLOWED_TRANSITIONS.get(current_status, [])

    if new_status not in allowed:
        raise ValidationError(
            f"Invalid status transition from {current_status} to {new_status}"
        )


# -------------------------------
# Cancel Appointment
# -------------------------------
def cancel_appointment(appt: Appointment):
    validate_transition(appt.status, "CANCELED")

    appt.status = "CANCELED"
    appt.save()

    return appt


# -------------------------------
# Reschedule Appointment
# -------------------------------
def reschedule_appointment(appt: Appointment, new_date, new_time):
    validate_transition(appt.status, "RESCHEDULED")

    appt.appointment_date = new_date
    appt.appointment_time = new_time
    appt.status = "RESCHEDULED"

    appt.full_clean()
    appt.save()

    return appt


# -------------------------------
# Confirm Appointment
# -------------------------------
def confirm_appointment(appt: Appointment):
    validate_transition(appt.status, "CONFIRMED")

    appt.status = "CONFIRMED"
    appt.save()

    return appt


# -------------------------------
# Complete Appointment
# -------------------------------
def complete_appointment(appt: Appointment):
    validate_transition(appt.status, "COMPLETED")

    appt.status = "COMPLETED"
    appt.save()

    return appt