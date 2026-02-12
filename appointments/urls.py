from django.urls import path
from .views import AvailabileSlotsAPIView, BookAppointmentAPIView

urlpatterns = [
    path('available-slots/', AvailabileSlotsAPIView.as_view(), name='available-slots'),
    path('book/', BookAppointmentAPIView.as_view(), name='book-appointment'),
]