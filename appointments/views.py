from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AvailableSlotsSerializer, AppointmentSerializer
from .models import Appointment

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
        appointment = serializer.save(status='PENDING')
        return Response(AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED)
