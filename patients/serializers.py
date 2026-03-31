from rest_framework import serializers
from .models import Patient,Appointment

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Patient
        fields='__all__'
    
    def validate_age(self,value):
        if not (0 <= value <= 120):
            raise serializers.ValidationError("Age must br b/w 0 to 120")
        return value

    def validate_contact_number(self,value):
        if len(value) != 10 or not value.isdigit():
            raise serializers.ValidationError("Contact number be exactly 10 digits")
        return value

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name=serializers.ReadOnlyField(source='patient.name')


    class Meta:
        model=Appointment
        fields=['id','patient','patient_name','doctor_name','appointment_date','reason','status']
