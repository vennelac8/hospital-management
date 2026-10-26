from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admin-dashboard/", views.dashboard, name="dashboard"),
    path("patient/", views.patient_dashboard, name="patient-dashboard"),
    path("doctor/", views.doctor_dashboard, name="doctor-dashboard"),
    path("doctor/appointments/<int:pk>/status/<str:status>/", views.doctor_appointment_status, name="doctor-appointment-status"),
    path("patients/", views.patient_list, name="patient-list"),
    path("patients/new/", views.patient_form, name="patient-create"),
    path("patients/<int:pk>/", views.patient_detail, name="patient-detail"),
    path("patients/<int:pk>/edit/", views.patient_form, name="patient-update"),
    path("patients/<int:pk>/delete/", views.patient_delete, name="patient-delete"),
    path("doctors/", views.doctor_list, name="doctor-list"),
    path("doctors/new/", views.doctor_form, name="doctor-create"),
    path("doctors/<int:pk>/edit/", views.doctor_form, name="doctor-update"),
    path("departments/", views.department_list, name="department-list"),
    path("departments/new/", views.department_form, name="department-create"),
    path("appointments/", views.appointment_list, name="appointment-list"),
    path("appointments/new/", views.appointment_create, name="appointment-create"),
    path("appointments/<int:pk>/status/<str:status>/", views.appointment_status, name="appointment-status"),
]
