import django.conf
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clinic", "0001_initial"),
        migrations.swappable_dependency(django.conf.settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="user",
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="doctor_record", to=django.conf.settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="patient",
            name="user",
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="patient_record", to=django.conf.settings.AUTH_USER_MODEL),
        ),
    ]
