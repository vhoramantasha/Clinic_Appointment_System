# Clinic Appointment System

A clean, modern web application developed with Python and Django for a small clinic to manage doctors, patients, and booked appointments.

---

## Features & Modules

### 1. Dashboard
- Displays **Total Doctors**
- Displays **Total Patients**
- Displays **Today's Appointment Count**
- Quick-action shortcuts and an interactive list of today's scheduled appointments.

### 2. Doctors Module
- **Add a new doctor**: Register doctor details (Name, Specialization, Phone, Email).
- **List all doctors with specialization**: Clean table showing all registered doctors and specializations.
- **Edit/update doctor details**: Modify doctor information with pre-populated form fields.
- **Delete a doctor**: Safe deletion flow with confirmation modal/screen.

### 3. Patients Module
- **Register a new patient**: Register patient details (Name, Age, Gender, Phone, Address).
- **List all patients**: Overview of all registered patients in the clinic.
- **Edit/update patient details**: Modify patient information at any time.

### 4. Appointments Module
- **Book an appointment**: Select a doctor, select a patient, choose appointment date, time, and initial status.
- **List all appointments**: Displays appointment date, time, doctor name (with specialization), and patient name (with phone).
- **Filter appointments**: Filter by doctor, by patient, or by date with real-time dropdowns and date pickers.
- **Cancel/update appointment status**: Modify status between *Scheduled*, *Completed*, and *Cancelled*, or quickly cancel an appointment.

---

## Project Structure

```text
LLM_Project_1/
├── clinic_system/            # Project configuration
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL routing
│   ├── wsgi.py
│   └── asgi.py
├── clinic/                   # Clinic core application
│   ├── models.py             # Doctor, Patient, Appointment models
│   ├── views.py              # Dashboard, Doctors, Patients, Appointments views
│   ├── forms.py              # Forms with Bootstrap validation
│   ├── urls.py               # App URL routes
│   ├── admin.py              # Django admin registration
│   ├── tests.py              # Comprehensive test suite (15 unit tests)
│   └── templates/clinic/     # Clean, responsive HTML templates (Bootstrap 5)
│       ├── base.html
│       ├── dashboard.html
│       ├── doctor_list.html
│       ├── doctor_form.html
│       ├── doctor_confirm_delete.html
│       ├── patient_list.html
│       ├── patient_form.html
│       ├── appointment_list.html
│       ├── appointment_form.html
│       └── appointment_status_update.html
├── populate_sample_data.py   # Script to populate initial demo data
├── requirements.txt          # Python dependencies
├── manage.py                 # Django CLI management script
└── db.sqlite3                # SQLite database
```

---

## Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Apply Database Migrations (Already executed)
```bash
python manage.py migrate
```

### 3. Load Sample Data (Optional)
To populate realistic sample doctors, patients, and appointments:
```bash
python populate_sample_data.py
```

### 4. Run the Development Server
```bash
python manage.py runserver
```
Then open your browser and navigate to:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### 5. Run the Automated Tests
Run the 15 automated test cases verifying all modules:
```bash
python manage.py test
```

