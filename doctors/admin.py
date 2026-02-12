from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_name",
        "clinic",
        "specialization",
        "available_from",
        "available_to",
    )

    search_fields = (
        "user__first_name",
        "user__last_name",
        "clinic__name",
        "specialization",
    )

    list_filter = (
        "clinic",
        "specialization",
    )

    ordering = ("id",)

    # -------- Custom Display Fields --------

    def get_name(self, obj):
        return obj.user.get_full_name()

    get_name.short_description = "Doctor Name"
