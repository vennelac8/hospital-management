from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import AppointmentForm, DepartmentForm, DoctorForm, PatientForm
from .models import Appointment, Department, Doctor, Patient


def staff_required(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), "login")
        if not request.user.is_staff:
            return render(request, "403.html", status=403)
        return view(request, *args, **kwargs)
    return wrapped


def role_record(user, relation):
    try:
        return getattr(user, relation)
    except (AttributeError, Patient.DoesNotExist, Doctor.DoesNotExist):
        return None


@login_required
def home(request):
    if request.user.is_staff:
        return redirect("dashboard")
    if role_record(request.user, "doctor_record"):
        return redirect("doctor-dashboard")
    if role_record(request.user, "patient_record"):
        return redirect("patient-dashboard")
    return render(request, "403.html", status=403)


@staff_required
def dashboard(request):
    today = timezone.localdate()
    appointments = Appointment.objects.select_related("patient", "doctor", "doctor__department")
    return render(request, "clinic/dashboard.html", {
        "today": today, "patient_count": Patient.objects.count(), "doctor_count": Doctor.objects.filter(is_active=True).count(),
        "department_count": Department.objects.count(), "today_count": appointments.filter(starts_at__date=today).exclude(status="cancelled").count(),
        "appointments": appointments.filter(starts_at__date=today).exclude(status="cancelled")[:8],
    })


@login_required
def patient_dashboard(request):
    patient = role_record(request.user, "patient_record")
    if not patient:
        return render(request, "403.html", status=403)
    today = timezone.localdate()
    appointments = patient.appointments.select_related("doctor", "doctor__department")
    return render(request, "clinic/patient_dashboard.html", {
        "patient": patient, "today": today,
        "upcoming": appointments.filter(starts_at__gte=timezone.now()).exclude(status="cancelled"),
        "past": appointments.filter(starts_at__lt=timezone.now()).order_by("-starts_at")[:5],
    })


@login_required
def doctor_dashboard(request):
    doctor = role_record(request.user, "doctor_record")
    if not doctor or not doctor.is_active:
        return render(request, "403.html", status=403)
    today = timezone.localdate()
    appointments = doctor.appointments.select_related("patient", "doctor__department")
    return render(request, "clinic/doctor_dashboard.html", {
        "doctor": doctor, "today": today,
        "appointments": appointments.filter(starts_at__gte=timezone.now()).exclude(status="cancelled")[:20],
        "today_count": appointments.filter(starts_at__date=today).exclude(status="cancelled").count(),
    })


@login_required
@require_POST
def doctor_appointment_status(request, pk, status):
    doctor = role_record(request.user, "doctor_record")
    if not doctor:
        return render(request, "403.html", status=403)
    appointment = get_object_or_404(Appointment, pk=pk, doctor=doctor)
    if status not in {"checked_in", "completed"}:
        return render(request, "403.html", status=403)
    if (status == "checked_in" and appointment.status != "scheduled") or (status == "completed" and appointment.status != "checked_in"):
        messages.error(request, "Update the appointment status in order: scheduled, checked in, then completed.")
        return redirect("doctor-dashboard")
    appointment.status = status
    appointment.save(update_fields=["status"])
    messages.success(request, f"Appointment marked {appointment.get_status_display().lower()}.")
    return redirect("doctor-dashboard")


@staff_required
def patient_list(request):
    query = request.GET.get("q", "").strip()
    patients = Patient.objects.all()
    if query:
        patients = patients.filter(Q(full_name__icontains=query) | Q(phone__icontains=query) | Q(email__icontains=query))
    return render(request, "clinic/patient_list.html", {"patients": patients, "query": query})


@staff_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, "clinic/patient_detail.html", {"patient": patient, "appointments": patient.appointments.select_related("doctor", "doctor__department")})


@staff_required
def patient_form(request, pk=None):
    patient = get_object_or_404(Patient, pk=pk) if pk else None
    form = PatientForm(request.POST or None, instance=patient)
    if form.is_valid():
        saved = form.save()
        messages.success(request, "Patient record saved.")
        return redirect(saved)
    return render(request, "clinic/form_page.html", {"form": form, "title": "Edit patient" if patient else "Register patient", "back_url": patient.get_absolute_url() if patient else "patient-list"})


@staff_required
@require_POST
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if patient.appointments.exists():
        messages.error(request, "This patient has appointment records and cannot be deleted. Keep the record for history.")
    else:
        patient.delete()
        messages.success(request, "Patient record deleted.")
    return redirect("patient-list")


@staff_required
def doctor_list(request):
    doctors = Doctor.objects.select_related("department")
    return render(request, "clinic/doctor_list.html", {"doctors": doctors})


@staff_required
def doctor_form(request, pk=None):
    doctor = get_object_or_404(Doctor, pk=pk) if pk else None
    form = DoctorForm(request.POST or None, instance=doctor)
    if form.is_valid():
        form.save()
        messages.success(request, "Doctor record saved.")
        return redirect("doctor-list")
    return render(request, "clinic/form_page.html", {"form": form, "title": "Edit doctor" if doctor else "Add doctor", "back_url": "doctor-list"})


@staff_required
def department_list(request):
    departments = Department.objects.prefetch_related("doctors")
    return render(request, "clinic/department_list.html", {"departments": departments})


@staff_required
def department_form(request):
    form = DepartmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Department added.")
        return redirect("department-list")
    return render(request, "clinic/form_page.html", {"form": form, "title": "Add department", "back_url": "department-list"})


@staff_required
def appointment_list(request):
    appointments = Appointment.objects.select_related("patient", "doctor", "doctor__department")
    day = request.GET.get("date", "")
    if day:
        appointments = appointments.filter(starts_at__date=day)
    return render(request, "clinic/appointment_list.html", {"appointments": appointments, "day": day})


@staff_required
def appointment_create(request):
    form = AppointmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Appointment scheduled.")
        return redirect("appointment-list")
    return render(request, "clinic/form_page.html", {"form": form, "title": "Schedule appointment", "back_url": "appointment-list"})


@staff_required
@require_POST
def appointment_status(request, pk, status):
    appointment = get_object_or_404(Appointment, pk=pk)
    allowed = dict(Appointment.STATUS_CHOICES)
    if status in allowed:
        appointment.status = status
        appointment.save(update_fields=["status"])
        messages.success(request, f"Appointment marked {allowed[status].lower()}.")
    return redirect(request.POST.get("next") or "appointment-list")
