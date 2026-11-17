from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import datetime
from .models import Doctor, Patient, Appointment


class ClinicSystemTests(TestCase):
    def setUp(self):
        # Create initial test doctor
        self.doctor1 = Doctor.objects.create(
            name="Alice Smith",
            specialization="Cardiology",
            phone="1234567890",
            email="alice@clinic.com"
        )
        self.doctor2 = Doctor.objects.create(
            name="Bob Jones",
            specialization="Dermatology",
            phone="0987654321",
            email="bob@clinic.com"
        )

        # Create initial test patient
        self.patient1 = Patient.objects.create(
            name="Charlie Brown",
            age=30,
            gender="Male",
            phone="1122334455",
            address="123 Main St"
        )
        self.patient2 = Patient.objects.create(
            name="Diana Prince",
            age=28,
            gender="Female",
            phone="9988776655",
            address="456 Elm St"
        )

        # Create today's appointment
        self.today = timezone.localdate()
        self.appointment1 = Appointment.objects.create(
            doctor=self.doctor1,
            patient=self.patient1,
            appointment_date=self.today,
            appointment_time=datetime.time(10, 0),
            status="Scheduled"
        )

    # ------------------- Doctors Module Tests -------------------
    def test_list_all_doctors_with_specialization(self):
        response = self.client.get(reverse('doctor_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Smith")
        self.assertContains(response, "Cardiology")
        self.assertContains(response, "Bob Jones")
        self.assertContains(response, "Dermatology")

    def test_add_new_doctor(self):
        response = self.client.post(reverse('doctor_create'), {
            'name': 'Carol White',
            'specialization': 'Pediatrics',
            'phone': '5556667777',
            'email': 'carol@clinic.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Doctor.objects.filter(name='Carol White', specialization='Pediatrics').exists())

    def test_edit_update_doctor_details(self):
        response = self.client.post(reverse('doctor_update', args=[self.doctor1.pk]), {
            'name': 'Alice Smith Updated',
            'specialization': 'Cardiology & Electrophysiology',
            'phone': '1234567890',
            'email': 'alice.new@clinic.com'
        })
        self.assertEqual(response.status_code, 302)
        self.doctor1.refresh_from_db()
        self.assertEqual(self.doctor1.name, 'Alice Smith Updated')
        self.assertEqual(self.doctor1.specialization, 'Cardiology & Electrophysiology')

    def test_delete_doctor(self):
        response = self.client.post(reverse('doctor_delete', args=[self.doctor2.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Doctor.objects.filter(pk=self.doctor2.pk).exists())

    # ------------------- Patients Module Tests -------------------
    def test_list_all_patients(self):
        response = self.client.get(reverse('patient_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Charlie Brown")
        self.assertContains(response, "Diana Prince")

    def test_register_new_patient(self):
        response = self.client.post(reverse('patient_create'), {
            'name': 'Eve Adams',
            'age': 40,
            'gender': 'Female',
            'phone': '4443332211',
            'address': '789 Oak Ave'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Patient.objects.filter(name='Eve Adams').exists())

    def test_edit_update_patient_details(self):
        response = self.client.post(reverse('patient_update', args=[self.patient1.pk]), {
            'name': 'Charlie Brown Jr.',
            'age': 31,
            'gender': 'Male',
            'phone': '1122334455',
            'address': 'New Address 99'
        })
        self.assertEqual(response.status_code, 302)
        self.patient1.refresh_from_db()
        self.assertEqual(self.patient1.name, 'Charlie Brown Jr.')
        self.assertEqual(self.patient1.age, 31)

    # ------------------- Appointments Module Tests -------------------
    def test_book_appointment(self):
        tomorrow = self.today + datetime.timedelta(days=1)
        response = self.client.post(reverse('appointment_book'), {
            'doctor': self.doctor2.id,
            'patient': self.patient2.id,
            'appointment_date': tomorrow.strftime('%Y-%m-%d'),
            'appointment_time': '14:30',
            'status': 'Scheduled'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Appointment.objects.filter(
            doctor=self.doctor2,
            patient=self.patient2,
            appointment_date=tomorrow
        ).exists())

    def test_list_appointments_with_doctor_and_patient_name(self):
        response = self.client.get(reverse('appointment_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.doctor1.name)
        self.assertContains(response, self.patient1.name)

    def test_update_appointment_status(self):
        response = self.client.post(reverse('appointment_update_status', args=[self.appointment1.pk]), {
            'status': 'Completed'
        })
        self.assertEqual(response.status_code, 302)
        self.appointment1.refresh_from_db()
        self.assertEqual(self.appointment1.status, 'Completed')

    def test_cancel_appointment(self):
        response = self.client.post(reverse('appointment_cancel', args=[self.appointment1.pk]))
        self.assertEqual(response.status_code, 302)
        self.appointment1.refresh_from_db()
        self.assertEqual(self.appointment1.status, 'Cancelled')

    def test_filter_appointments_by_doctor(self):
        # Create second appointment with doctor 2
        tomorrow = self.today + datetime.timedelta(days=1)
        appt2 = Appointment.objects.create(
            doctor=self.doctor2,
            patient=self.patient2,
            appointment_date=tomorrow,
            appointment_time=datetime.time(11, 0),
            status="Scheduled"
        )
        # Filter by doctor 1
        response = self.client.get(reverse('appointment_list') + f'?doctor={self.doctor1.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.appointment1, response.context['appointments'])
        self.assertNotIn(appt2, response.context['appointments'])

    def test_filter_appointments_by_patient(self):
        # Create second appointment with patient 2
        tomorrow = self.today + datetime.timedelta(days=1)
        appt2 = Appointment.objects.create(
            doctor=self.doctor2,
            patient=self.patient2,
            appointment_date=tomorrow,
            appointment_time=datetime.time(11, 0),
            status="Scheduled"
        )
        # Filter by patient 1
        response = self.client.get(reverse('appointment_list') + f'?patient={self.patient1.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.appointment1, response.context['appointments'])
        self.assertNotIn(appt2, response.context['appointments'])

    def test_filter_appointments_by_date(self):
        # Create second appointment with tomorrow's date
        tomorrow = self.today + datetime.timedelta(days=1)
        appt2 = Appointment.objects.create(
            doctor=self.doctor2,
            patient=self.patient2,
            appointment_date=tomorrow,
            appointment_time=datetime.time(11, 0),
            status="Scheduled"
        )
        # Filter by today's date
        response = self.client.get(reverse('appointment_list') + f'?date={self.today.strftime("%Y-%m-%d")}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.appointment1, response.context['appointments'])
        self.assertNotIn(appt2, response.context['appointments'])

    # ------------------- Dashboard Tests -------------------
    def test_dashboard_metrics(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_doctors'], 2)
        self.assertEqual(response.context['total_patients'], 2)
        self.assertEqual(response.context['today_appointments_count'], 1)
        # Check text rendered on page
        self.assertContains(response, "Total Doctors")
        self.assertContains(response, "Total Patients")
        self.assertContains(response, "Today's Appointments")
