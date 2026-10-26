from django.contrib import admin
from .models import Appointment, Department, Doctor, Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "phone", "email", "date_of_birth")
    search_fields = ("full_name", "phone", "email")


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "specialty", "department", "is_active")
    list_filter = ("department", "is_active")
    search_fields = ("name", "specialty")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("starts_at", "patient", "doctor", "status")
    list_filter = ("status", "doctor")
    search_fields = ("patient__full_name", "doctor__name")
