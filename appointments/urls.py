from django.urls import path
from .views import AvailabileSlotsAPIView, BookAppointmentAPIView, DoctorAvailabilityCalendarAPIView
from .views import CancelAppointmentAPIView, PatientAppointmentHistoryAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('available-slots/', AvailabileSlotsAPIView.as_view(), name='available-slots'),
    path('book/', BookAppointmentAPIView.as_view(), name='book-appointment'),
    path('cancel/<int:pk>/', CancelAppointmentAPIView.as_view()),
    path("patient/history/", PatientAppointmentHistoryAPIView.as_view(), name="patient-history"),
    path("doctor/calendar/", DoctorAvailabilityCalendarAPIView.as_view(), name="doctor-availability_calendar"),
]