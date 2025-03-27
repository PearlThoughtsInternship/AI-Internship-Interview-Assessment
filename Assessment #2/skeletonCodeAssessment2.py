import heapq
from datetime import datetime, timedelta
import random
import time
from collections import deque

class Doctor:
    def __init__(self, name, schedule_blocks):
        self.name = name
        self.schedule_blocks = schedule_blocks  # List of time slots
        self.patients_queue = deque()
        self.status_tracking = {}  # {patient_id: status}
    
    def add_patient(self, patient):
        self.patients_queue.append(patient)
        self.status_tracking[patient.patient_id] = "Waiting"
    
    def consult_patient(self):
        if self.patients_queue:
            patient = self.patients_queue.popleft()
            self.status_tracking[patient.patient_id] = "Consulted"
            return patient
        return None

class Patient:
    def __init__(self, patient_id, name, arrival_time, appointment_time, booking_channel):
        self.patient_id = patient_id
        self.name = name
        self.arrival_time = arrival_time
        self.appointment_time = appointment_time
        self.booking_channel = booking_channel
        self.status = "Not Arrived"

class QueueManagementSystem:
    def __init__(self, doctors):
        self.doctors = {doctor.name: doctor for doctor in doctors}
        self.waiting_list = []  # List of patients waiting
        self.historical_data = []  # Store past patient wait times
    
    def patient_check_in(self, patient_name, doctor_name, arrival_time, booking_channel):
        if doctor_name in self.doctors:
            patient = Patient(len(self.historical_data) + 1, patient_name, arrival_time, None, booking_channel)
            self.waiting_list.append(patient)
            self.doctors[doctor_name].add_patient(patient)
            patient.status = "Waiting"
            print(f"{patient.name} checked in for Dr. {doctor_name} at {arrival_time}")
        else:
            print("Doctor not found.")
    
    def assign_patients_to_doctors(self):
        for doctor in self.doctors.values():
            while len(doctor.patients_queue) < 5 and self.waiting_list:
                patient = self.waiting_list.pop(0)
                doctor.add_patient(patient)
                print(f"Assigned {patient.name} to Dr. {doctor.name}")
    
    def track_and_update_status(self):
        for doctor in self.doctors.values():
            if doctor.patients_queue:
                consulted_patient = doctor.consult_patient()
                if consulted_patient:
                    print(f"Dr. {doctor.name} has consulted {consulted_patient.name}.")
                    self.historical_data.append((consulted_patient.name, time.time() - consulted_patient.arrival_time))
    
    def estimate_wait_time(self, doctor_name):
        if doctor_name in self.doctors:
            return len(self.doctors[doctor_name].patients_queue) * 10  # Approx 10 mins per patient
        return -1
    
    def notify_patients(self):
        for doctor in self.doctors.values():
            for patient in doctor.patients_queue:
                wait_time = self.estimate_wait_time(doctor.name)
                print(f"Notification: {patient.name}, your estimated wait time for Dr. {doctor.name} is {wait_time} minutes.")
    
    def measure_system_effectiveness(self):
        avg_wait_time = sum(wait for _, wait in self.historical_data) / len(self.historical_data) if self.historical_data else 0
        efficiency_score = sum(len(doctor.patients_queue) for doctor in self.doctors.values()) / len(self.doctors)
        print(f"Average Wait Time: {avg_wait_time:.2f} minutes")
        print(f"Queue Efficiency Score: {efficiency_score:.2f}")

# Example Usage
doctors = [Doctor(f"Dr. {i}", ["Morning", "Afternoon"]) for i in range(1, 6)]
qms = QueueManagementSystem(doctors)

qms.patient_check_in("Alice", "Dr. 1", time.time(), "App")
qms.patient_check_in("Bob", "Dr. 2", time.time(), "WhatsApp")
qms.assign_patients_to_doctors()
qms.track_and_update_status()
qms.notify_patients()
qms.measure_system_effectiveness()
