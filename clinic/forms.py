from django import forms
from .models import Appointment, Department, Doctor, Patient


class DateInput(forms.DateInput):
    input_type = "date"


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["full_name", "date_of_birth", "gender", "phone", "email", "address", "emergency_contact"]
        widgets = {"date_of_birth": DateInput(), "address": forms.Textarea(attrs={"rows": 3})}


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ["name", "specialty", "department", "phone", "email", "is_active"]


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class AppointmentForm(forms.ModelForm):
    starts_at = forms.DateTimeField(input_formats=["%Y-%m-%dT%H:%M"], widget=DateTimeInput())

    class Meta:
        model = Appointment
        fields = ["patient", "doctor", "starts_at", "reason", "status"]
