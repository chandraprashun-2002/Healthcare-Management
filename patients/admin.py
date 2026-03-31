from django.contrib import admin
from .models import Patient,Appointment

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display=('name', 'age', 'blood_group', 'contact_number', 'created_at')
    search_field=('name', 'contact_number')
    list_filter=('blood_group', 'gender')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display=('patient', 'doctor_name', 'appointment_date', 'status')
    search_field=('doctor_name', 'patient__name')
    list_filter=('status', 'appointment_date')
    date_hierarchy='appointment_date'
