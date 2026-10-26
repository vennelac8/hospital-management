from django.conf import settings
from django.db import models
from django.urls import reverse


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="doctor_record", blank=True, null=True)
    name = models.CharField(max_length=120)
    specialty = models.CharField(max_length=120)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="doctors")
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"Dr. {self.name}"


class Patient(models.Model):
    GENDER_CHOICES = [("female", "Female"), ("male", "Male"), ("other", "Other"), ("prefer_not", "Prefer not to say")]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="patient_record", blank=True, null=True)
    full_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=12, choices=GENDER_CHOICES, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse("patient-detail", args=[self.pk])


class Appointment(models.Model):
    STATUS_CHOICES = [("scheduled", "Scheduled"), ("checked_in", "Checked in"), ("completed", "Completed"), ("cancelled", "Cancelled")]
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name="appointments")
    starts_at = models.DateTimeField()
    reason = models.CharField(max_length=180, blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="scheduled")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["starts_at"]

    def __str__(self):
        return f"{self.patient} · {self.starts_at:%Y-%m-%d %H:%M}"
