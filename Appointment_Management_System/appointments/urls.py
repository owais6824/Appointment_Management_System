from django.urls import path
from .views import AvailabileSlotsAPIView, BookAppointmentAPIView
from .views import CancelAppointmentAPIView, PatientAppointmentHistoryAPIView

urlpatterns = [
    path('available-slots/', AvailabileSlotsAPIView.as_view(), name='available-slots'),
    path('book/', BookAppointmentAPIView.as_view(), name='book-appointment'),
    path('cancel/<int:pk>/', CancelAppointmentAPIView.as_view()),
    path('patient/history', PatientAppointmentHistoryAPIView.as_view(), name='patient-history'),
]