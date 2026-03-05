from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .pagination import StandardResultsSetPagination
from accounts.permissions import IsPatient
from doctors.models import Doctor
from .services.calender_service import get_doctor_monthly_calender
from .serializers import AvailableSlotsSerializer, AppointmentSerializer, DoctorCalendarDaySerializer
from .models import Appointment
from appointments.services.booking_service import create_booking
from accounts.permissions import (
    CanBookAppointment,
    IsDoctor,
    IsClinicAdmin,
    IsSuperAdmin, 
    IsReceptionist
)
from accounts.models import User
from .permissions import IsDoctorOrAdmin
from .services.dashboard_service import get_doctor_dashboard_data


# -----------------------------------------
# Available Slots API
# -----------------------------------------

class AvailabileSlotsAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        CanBookAppointment  # Patient, Receptionist, Clinic Admin
    ]

    def get(self, request):
        serializer = AvailableSlotsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return Response(serializer.to_representation(data))


# -----------------------------------------
# Book Appointment
# -----------------------------------------

class BookAppointmentAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        CanBookAppointment
    ]

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        appointment = create_booking(serializer.validated_data)

        return Response(
            AppointmentSerializer(appointment).data,
            status=status.HTTP_201_CREATED
        )


# -----------------------------------------
# Cancel Appointment
# -----------------------------------------

class CancelAppointmentAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        appt = get_object_or_404(Appointment, pk=pk)

        # Role-based ownership enforcement
        if request.user.role == User.PATIENT:
            if appt.patient.user != request.user:
                return Response(
                    {"detail": "You cannot cancel this appointment."},
                    status=status.HTTP_403_FORBIDDEN
                )

        elif request.user.role == User.DOCTOR:
            if appt.doctor.user != request.user:
                return Response(
                    {"detail": "You cannot cancel this appointment."},
                    status=status.HTTP_403_FORBIDDEN
                )

        elif request.user.role not in [
            User.CLINIC_ADMIN,
            User.SUPER_ADMIN,
            User.RECEPTIONIST
        ]:
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN
            )

        appt.status = "CANCELED"
        appt.save()

        return Response({"status": "Canceled"})


# -----------------------------------------
# Reschedule Appointment
# -----------------------------------------

class RescheduleAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        appt = get_object_or_404(Appointment, pk=pk)

        # Ownership enforcement
        if request.user.role == User.PATIENT:
            if appt.patient.user != request.user:
                return Response(
                    {"detail": "You cannot reschedule this appointment."},
                    status=status.HTTP_403_FORBIDDEN
                )

        elif request.user.role == User.DOCTOR:
            if appt.doctor.user != request.user:
                return Response(
                    {"detail": "You cannot reschedule this appointment."},
                    status=status.HTTP_403_FORBIDDEN
                )

        elif request.user.role not in [
            User.CLINIC_ADMIN,
            User.SUPER_ADMIN,
            User.RECEPTIONIST
        ]:
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN
            )

        new_time = request.data.get("appointment_time")
        new_date = request.data.get("appointment_date")

        if not new_time or not new_date:
            return Response(
                {"detail": "appointment_date and appointment_time are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        appt.appointment_time = new_time
        appt.appointment_date = new_date

        appt.full_clean()
        appt.save()

        return Response({"status": "Rescheduled"})
    
class PatientAppointmentHistoryAPIView(ListAPIView):

    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsPatient]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Return only appointments belonging to logged-in patient.
        Ordered by newest first.
        """
        return (
            Appointment.objects
            .filter(patient__user=self.request.user)
            .order_by("-appointment_date", "-appointment_time")
        )
    

# -----------------------------------------
# Doctor Availability
# -----------------------------------------

class DoctorAvailabilityCalendarAPIView(APIView):
    """
    Returns a doctor's availability calendar for a given month.
    """
    
    permission_classes = [IsAuthenticated, IsDoctorOrAdmin]

    def get(self, request):
        # Required query parameters
        doctor_id = request.query_params.get("doctor_id")
        year = request.query_params.get("year")
        month = request.query_params.get("month")

        if not doctor_id or not year or not month:
            return Response(
                {"detail": "doctor_id, year and month are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate year/month integers
        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return Response(
                {"detail": "Invalid year or month format."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch the doctor safely
        doctor = get_object_or_404(Doctor, pk=int(doctor_id))

        # Permissions
        user_role = request.user.role
        if user_role == User.DOCTOR:
            if doctor.user != request.user:
                return Response(
                    {"detail": "Doctors can only view their own calendar."},
                    status=status.HTTP_403_FORBIDDEN
                )
        elif user_role not in [
            User.CLINIC_ADMIN,
            User.RECEPTIONIST,
            User.SUPER_ADMIN
        ]:
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Generate calendar data
        calender_data = get_doctor_monthly_calender(
            doctor_id=doctor.id,
            year=year,
            month=month
        )

        serializer = DoctorCalendarDaySerializer(calender_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# -----------------------------------------
# Dashboard Class
# -----------------------------------------

class DoctorDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request):
        data = get_doctor_dashboard_data(request.user)
        return Response(data)