from django.urls import path
from .views import AvailabileSlotsAPIView, BookAppointmentAPIView
from .views import CancelAppointmentAPIView

urlpatterns = [
    path('available-slots/', AvailabileSlotsAPIView.as_view(), name='available-slots'),
    path('book/', BookAppointmentAPIView.as_view(), name='book-appointment'),
    path('cancel/<int:pk>/', CancelAppointmentAPIView.as_view()),
]