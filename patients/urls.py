from django.urls import path
from .views import PatientListCreateAPIView, PatientDetailAPIView, AppointmentListAPIView,StatsAPIView,UpcomingAppointmentsAPIView

urlpatterns = [
    path('patients/', PatientListCreateAPIView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', PatientDetailAPIView.as_view(), name='patient-detail'),
    path('appointments/', AppointmentListAPIView.as_view(), name='appointment-list'),
    path('stats/', StatsAPIView.as_view(), name='stats'),
    path('appointments/upcoming/', UpcomingAppointmentsAPIView.as_view(), name='upcoming-appointments'),
]