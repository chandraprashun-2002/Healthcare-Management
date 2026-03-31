from django.db import models

class Patient(models.Model):
    BLOOD_GROUP_CHOICES =[
        ('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('AB+','AB+'),('AB-','AB-'),
        ('O+','O+'),('O-','O-'),
    ]
    name=models.CharField(max_length=100)
    age=models.PositiveIntegerField()
    gender=models.CharField(max_length=10,choices=[('Male','Male'),('Female','Female'),('Other','Other')])
    contact_number=models.CharField(max_length=15)
    blood_group=models.CharField(max_length=3,choices=BLOOD_GROUP_CHOICES)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.blood_group})"

class Appointment(models.Model):
    
    STATUS_CHOICES =[
        ('Pending','Pending'),
        ('Confirmed','Confirmed'),
        ('Cancelled','Cancelled'),
    ]
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='appointments')
    doctor_name=models.CharField(max_length=100)
    appointment_date=models.DateTimeField()
    reason=models.TextField()
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='Pending')

    def __str__(self):
        return f"{self.doctor_name}-{self.patient.name} ({self.appointment_date.date()})"