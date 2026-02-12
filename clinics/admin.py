from django.contrib import admin
from .models import Clinic

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "email")
    search_fields = ("name", "phone", "email")
    ordering = ("id",)