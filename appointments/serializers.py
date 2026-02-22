from rest_framework import serializers
from .models import Appointment
from doctors.models import Doctor
from patients.models import Patient
from .services.slot_engine import generate_slots
from datetime import date as dt_date

class AvailableSlotsSerializer(serializers.Serializer):
    doctor_id = serializers.IntegerField()
    date = serializers.DateField()

    def validate(self, data):
        try:
            doctor = Doctor.objects.get(id=data['doctor_id'])
        except Doctor.DoesNotExist:
            raise serializers.ValidationError("Doctor does not exist.")
        data['doctor'] = doctor
        return data
    
    def to_representation(self, instance):
        doctor = instance['doctor']
        date_obj = instance['date']
        slots = generate_slots(doctor, date_obj)
        return {
            "doctor_id": doctor.id,
            "date": date_obj,
            "available_slots": slots
        }
    
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

    def validate(self, data):
        doctor = data["doctor"]
        time = data["appointment_time"]
        
        if not (doctor.available_from <= time < doctor.available_to):
            raise serializers.ValidationError(
                "Appointment time outside doctor avaialbility."
            )
        
        return data

