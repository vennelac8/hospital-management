import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="Department", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=100, unique=True)), ("description", models.TextField(blank=True)),
        ], options={"ordering": ["name"]}),
        migrations.CreateModel(name="Doctor", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=120)), ("specialty", models.CharField(max_length=120)),
            ("phone", models.CharField(blank=True, max_length=30)), ("email", models.EmailField(blank=True, max_length=254)),
            ("is_active", models.BooleanField(default=True)),
            ("department", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="doctors", to="clinic.department")),
        ], options={"ordering": ["name"]}),
        migrations.CreateModel(name="Patient", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("full_name", models.CharField(max_length=150)), ("date_of_birth", models.DateField(blank=True, null=True)),
            ("gender", models.CharField(blank=True, choices=[("female", "Female"), ("male", "Male"), ("other", "Other"), ("prefer_not", "Prefer not to say")], max_length=12)),
            ("phone", models.CharField(blank=True, max_length=30)), ("email", models.EmailField(blank=True, max_length=254)),
            ("address", models.TextField(blank=True)), ("emergency_contact", models.CharField(blank=True, max_length=150)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
        ], options={"ordering": ["full_name"]}),
        migrations.CreateModel(name="Appointment", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("starts_at", models.DateTimeField()), ("reason", models.CharField(blank=True, max_length=180)),
            ("status", models.CharField(choices=[("scheduled", "Scheduled"), ("checked_in", "Checked in"), ("completed", "Completed"), ("cancelled", "Cancelled")], default="scheduled", max_length=12)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("doctor", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="appointments", to="clinic.doctor")),
            ("patient", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="appointments", to="clinic.patient")),
        ], options={"ordering": ["starts_at"]}),
    ]
