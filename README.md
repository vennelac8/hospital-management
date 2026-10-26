# CarePoint — Hospital Management System

A Django starter for coordinating basic hospital operations. It includes a staff login, overview dashboard, patient directory, doctor and department records, appointment scheduling, appointment status updates, and a Django admin site. SQLite is configured for local development.

## Run on Windows (Command Prompt)

```cmd
cd /d "C:\Users\thoka\OneDrive\Documents\New project\hospital_management"
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ and sign in with the superuser account you created. The admin workspace is at http://127.0.0.1:8000/admin/.

## Main areas

- **Overview:** daily appointment summary and quick actions
- **Patients:** register, search, view, and edit patient contact records
- **Doctors:** add doctors and assign them to departments
- **Departments:** organize care teams
- **Appointments:** schedule visits and mark them checked in or completed
- **Admin:** manage all records through Django admin

## Set up patient and doctor portal accounts

Only staff accounts can use the admin workspace. From `/admin/`, create a regular user under **Authentication and Authorization → Users**. Then create a Patient or Doctor record and select that user in its **User** field. A user linked to a patient record goes to the patient portal; a user linked to a doctor record goes to the doctor portal. Keep **Staff status** off for patient and doctor accounts. The initial superuser uses the admin portal.

## Local development only

This starter is intended for learning and local prototyping. Do not enter real patient information or deploy it for hospital use as-is. Before any real deployment, the hospital would need a security and privacy review, role-based access, audit logging, secure hosting and backups, tested recovery, and controls appropriate to its requirements. Replace the development secret key, turn off debug mode, configure trusted hosts, and use a production database before deployment.
