from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Doctor, Patient, Appointment
from .forms import DoctorForm, PatientForm, AppointmentForm, AppointmentStatusForm


# Dashboard
def dashboard_view(request):
    today = timezone.localdate()
    total_doctors = Doctor.objects.count()
    total_patients = Patient.objects.count()
    today_appointments_count = Appointment.objects.filter(appointment_date=today).count()
    
    # Today's appointments for quick view on dashboard
    today_appointments = Appointment.objects.select_related('doctor', 'patient').filter(appointment_date=today).order_by('appointment_time')

    context = {
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'today_appointments_count': today_appointments_count,
        'today_appointments': today_appointments,
        'today': today,
    }
    return render(request, 'clinic/dashboard.html', context)


# Doctors Module
def doctor_list(request):
    doctors = Doctor.objects.all().order_by('name')
    return render(request, 'clinic/doctor_list.html', {'doctors': doctors})


def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save()
            messages.success(request, f"Doctor Dr. {doctor.name} added successfully!")
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    return render(request, 'clinic/doctor_form.html', {'form': form, 'title': 'Add New Doctor'})


def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, f"Doctor Dr. {doctor.name} details updated successfully!")
            return redirect('doctor_list')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'clinic/doctor_form.html', {'form': form, 'title': 'Edit Doctor Details', 'doctor': doctor})


def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor_name = doctor.name
        doctor.delete()
        messages.success(request, f"Doctor Dr. {doctor_name} was deleted successfully.")
        return redirect('doctor_list')
    return render(request, 'clinic/doctor_confirm_delete.html', {'doctor': doctor})


# Patients Module
def patient_list(request):
    patients = Patient.objects.all().order_by('name')
    return render(request, 'clinic/patient_list.html', {'patients': patients})


def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f"Patient {patient.name} registered successfully!")
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'clinic/patient_form.html', {'form': form, 'title': 'Register New Patient'})


def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, f"Patient {patient.name} details updated successfully!")
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'clinic/patient_form.html', {'form': form, 'title': 'Edit Patient Details', 'patient': patient})


# Appointments Module
def appointment_book(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            messages.success(request, f"Appointment booked successfully for {appointment.patient.name} with Dr. {appointment.doctor.name} on {appointment.appointment_date}!")
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'clinic/appointment_form.html', {'form': form, 'title': 'Book an Appointment'})


def appointment_list(request):
    appointments = Appointment.objects.select_related('doctor', 'patient').all()

    doctor_filter = request.GET.get('doctor', '').strip()
    patient_filter = request.GET.get('patient', '').strip()
    date_filter = request.GET.get('date', '').strip()

    if doctor_filter:
        appointments = appointments.filter(doctor_id=doctor_filter)
    if patient_filter:
        appointments = appointments.filter(patient_id=patient_filter)
    if date_filter:
        appointments = appointments.filter(appointment_date=date_filter)

    doctors = Doctor.objects.all().order_by('name')
    patients = Patient.objects.all().order_by('name')

    context = {
        'appointments': appointments,
        'doctors': doctors,
        'patients': patients,
        'selected_doctor': doctor_filter,
        'selected_patient': patient_filter,
        'selected_date': date_filter,
    }
    return render(request, 'clinic/appointment_list.html', context)


def appointment_update_status(request, pk):
    appointment = get_object_or_404(Appointment.objects.select_related('doctor', 'patient'), pk=pk)
    if request.method == 'POST':
        form = AppointmentStatusForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, f"Appointment status updated to '{appointment.status}' successfully!")
            return redirect('appointment_list')
    else:
        form = AppointmentStatusForm(instance=appointment)
    return render(request, 'clinic/appointment_status_update.html', {'form': form, 'appointment': appointment})


def appointment_cancel(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.status = 'Cancelled'
        appointment.save()
        messages.success(request, f"Appointment on {appointment.appointment_date} has been marked as Cancelled.")
    return redirect('appointment_list')
