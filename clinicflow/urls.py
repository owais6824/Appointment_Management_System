from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import home
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/appointments/', include('appointments.urls')),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Swagger schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    # Swagger UI
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui",),

    # Redoc
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc",),
]
