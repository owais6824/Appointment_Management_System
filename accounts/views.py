from django.shortcuts import render
from rest_framework.views import APIView
from appointments.throttling import LoginRateThrottle


class LoginView(APIView):
    throttle_classes = [LoginRateThrottle]
    
    def post(self, request):
        ...
