from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AvailableSlotsSerializer, AppointmentSerializer
from .models import Appointment
from appointments.services.booking_service import create_booking



class AvailabileSlotsAPIView(APIView):
    def get(self, request):
        serializer = AvailableSlotsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception = True)
        data = serializer.validated_data
        return Response(serializer.to_representaion(data))
    
class BookAppointmentAPIView(APIView):

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        appointment = create_booking(serializer.validated_data)

        return Response(
            AppointmentSerializer(appointment).data,
            status=status.HTTP_201_CREATED
        )

class CancelAppointmentAPIView(APIView):

    def patch(self, request, pk):
        appt = get_object_or_404(Appointment, pk=pk)

        appt.status = "CANCELED"
        appt.save()

        return Response({"status" : "Canceled"})
    

class RescheduleAPIView(APIView):
    def patch(self, request, pk):
        appt = get_object_or_404(Appointment, pk=pk)

        new_time = request.data.get("appointment_time")
        new_date = request.data.get("appointment_date")

        appt.appointment_time = new_time
        appt.appointment_date = new_date

        appt.full_clean()
        appt.save()

        return Response({"Status": "Rescheduled"})