from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Patient,Appointment
from .serializers import PatientSerializer,AppointmentSerializer
from django.utils import timezone 
from datetime import timedelta
from django.db.models import Count
from .permissions import IsStaffOrReadOnly
from rest_framework.permissions import IsAuthenticated

class PatientListCreateAPIView(APIView):
    permission_classes=[IsAuthenticated,IsStaffOrReadOnly]
    def get(self, request):
        queryset = Patient.objects.all()

        search_query=request.query_params.get('search')
        if search_query:
            queryset=queryset.filter(name__icontains=search_query)
        serializer = PatientSerializer(queryset, many=True)
        return Response({
            "success": True,
            "message": "Patients retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Patient created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "success": False,
            "message": "Validation failed",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        


class StatsAPIView(APIView):
    def get(self,request):
        total_patients=Patient.objects.count()
        total_appointments=Appointment.objects.count()

        status_counts=Appointment.objects.values('status').annotate(count=Count('status'))

        status_dict ={item['status']:item['count'] for item in status_counts}


        return Response({
            "success": True,
            "message": "Stats retrieved successfully",
            "data": {
                "total_patients": total_patients,
                "total_appointments": total_appointments,
                "appointment_by_status": status_dict
            }
        })




class PatientDetailAPIView(APIView):
    permission_classes = [IsStaffOrReadOnly]
    def get(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk)
            serializer = PatientSerializer(patient)
            return Response({
                "success": True,
                "message": "Patient found",
                "data": serializer.data
            })
        except Patient.DoesNotExist:
            return Response({
                "success": False,
                "message": "Patient record not found",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk)
            patient.delete()
            return Response({
                "success": True,
                "message": "Patient deleted successfully",
                "data": None
            }, status=status.HTTP_204_NO_CONTENT)
        except Patient.DoesNotExist:
            return Response({
                "success": False,
                "message": "Cannot delete: Patient not found",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

class AppointmentListAPIView(APIView):
    def get(self, request):
        queryset = Appointment.objects.all()
        status_param = request.query_params.get('status')
        patient_id_param = request.query_params.get('patient_id')

        if status_param:
            queryset = queryset.filter(status=status_param)
        
        if patient_id_param:
            queryset = queryset.filter(patient_id=patient_id_param)

        serializer = AppointmentSerializer(queryset, many=True)
        return Response({
            "success": True,
            "message": "Appointments retrieved successfully",
            "data": serializer.data
        })


class UpcomingAppointmentsAPIView(APIView):
    def get(self,request):
        now=timezone.now()
        one_week_later=now+timedelta(days=7)


        upcoming=Appointment.objects.filter(
            appointment_date__range=(now,one_week_later)
        ).order_by('appointment_date')


        serializer=AppointmentSerializer(upcoming,many=True)
        return Response({
            "success": True,
            "message": "Upcoming appointments retrieved successfully",
            "data": serializer.data
        })
