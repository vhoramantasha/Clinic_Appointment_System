import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinic_system.settings')
django.setup()

from clinic.models import Doctor, Patient, Appointment
from django.utils import timezone


def seed_data():
    print("Clearing old data...")
    Appointment.objects.all().delete()
    Doctor.objects.all().delete()
    Patient.objects.all().delete()

    print("Adding doctors...")
    doc1 = Doctor.objects.create(
        name="Sarah Jenkins",
        specialization="Cardiology",
        phone="+1 555-0101",
        email="dr.jenkins@clinic.com"
    )
    doc2 = Doctor.objects.create(
        name="Marcus Vance",
        specialization="Pediatrics",
        phone="+1 555-0102",
        email="dr.vance@clinic.com"
    )
    doc3 = Doctor.objects.create(
        name="Elena Rostova",
        specialization="Dermatology",
        phone="+1 555-0103",
        email="dr.rostova@clinic.com"
    )
    doc4 = Doctor.objects.create(
        name="David Kim",
        specialization="General Medicine",
        phone="+1 555-0104",
        email="dr.kim@clinic.com"
    )

    print("Registering patients...")
    p1 = Patient.objects.create(
        name="Emma Watson",
        age=29,
        gender="Female",
        phone="+1 555-0201",
        address="102 Elm St, Springfield"
    )
    p2 = Patient.objects.create(
        name="James Miller",
        age=45,
        gender="Male",
        phone="+1 555-0202",
        address="454 Pine Ave, Springfield"
    )
    p3 = Patient.objects.create(
        name="Sophia Martinez",
        age=12,
        gender="Female",
        phone="+1 555-0203",
        address="789 Maple Rd, Springfield"
    )
    p4 = Patient.objects.create(
        name="Robert Taylor",
        age=63,
        gender="Male",
        phone="+1 555-0204",
        address="321 Oak Dr, Springfield"
    )

    today = timezone.localdate()
    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)

    print("Creating sample appointments...")
    # Today's appointments
    Appointment.objects.create(
        doctor=doc1,
        patient=p2,
        appointment_date=today,
        appointment_time=datetime.time(9, 30),
        status="Scheduled"
    )
    Appointment.objects.create(
        doctor=doc2,
        patient=p3,
        appointment_date=today,
        appointment_time=datetime.time(11, 0),
        status="Scheduled"
    )
    Appointment.objects.create(
        doctor=doc4,
        patient=p1,
        appointment_date=today,
        appointment_time=datetime.time(14, 15),
        status="Completed"
    )

    # Tomorrow's appointment
    Appointment.objects.create(
        doctor=doc3,
        patient=p1,
        appointment_date=tomorrow,
        appointment_time=datetime.time(10, 0),
        status="Scheduled"
    )

    # Past appointment
    Appointment.objects.create(
        doctor=doc1,
        patient=p4,
        appointment_date=yesterday,
        appointment_time=datetime.time(16, 0),
        status="Completed"
    )

    print(f"Sample data loaded successfully!")
    print(f"Total Doctors: {Doctor.objects.count()}")
    print(f"Total Patients: {Patient.objects.count()}")
    print(f"Total Appointments: {Appointment.objects.count()}")
    print(f"Today's Appointments: {Appointment.objects.filter(appointment_date=today).count()}")


if __name__ == '__main__':
    seed_data()

