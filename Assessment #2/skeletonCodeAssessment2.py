import heapq
from datetime import datetime, timedelta
import random

class Doctor:
    def __init__(self, doctor_id, availability_blocks):
        self.doctor_id = doctor_id
        self.queue = []
        self.availability_blocks = availability_blocks  # Example: [(9, 12), (15, 18)] for shift timing
    
    def add_patient(self, patient):
        heapq.heappush(self.queue, (patient.priority, patient))
    
    def next_patient(self):
        if self.queue:
            return heapq.heappop(self.queue)[1]
        return None

class Patient:
    def __init__(self, patient_id, arrival_time, scheduled_time, urgency, source):
        self.patient_id = patient_id
        self.arrival_time = arrival_time
        self.scheduled_time = scheduled_time
        self.urgency = urgency
        self.source = source  # 'App', 'Walk-in', 'WhatsApp', etc.
        self.priority = self.calculate_priority()

    def calculate_priority(self):
        # Higher priority for urgent cases, walk-ins may have lower priority
        delay = max(0, (self.arrival_time - self.scheduled_time).seconds // 60)
        return self.urgency * 10 - delay

class QueueManagementSystem:
    def __init__(self):
        self.doctors = {}

    def add_doctor(self, doctor_id, availability_blocks):
        self.doctors[doctor_id] = Doctor(doctor_id, availability_blocks)

    def assign_patient(self, doctor_id, patient):
        if doctor_id in self.doctors:
            self.doctors[doctor_id].add_patient(patient)

    def estimate_wait_time(self, doctor_id):
        if doctor_id in self.doctors:
            num_patients = len(self.doctors[doctor_id].queue)
            avg_consult_time = random.randint(8, 22)  # Simulating doctor-specific consult times
            return num_patients * avg_consult_time

# Example Usage
qms = QueueManagementSystem()
qms.add_doctor(1, [(9, 12), (15, 18)])

patient1 = Patient(101, datetime.now(), datetime.now() + timedelta(minutes=15), urgency=2, source="App")
patient2 = Patient(102, datetime.now(), datetime.now() + timedelta(minutes=10), urgency=3, source="Walk-in")

qms.assign_patient(1, patient1)
qms.assign_patient(1, patient2)

print(f"Estimated wait time for Doctor 1: {qms.estimate_wait_time(1)} minutes")
def calculate_priority(self):
    delay = max(0, (self.arrival_time - self.scheduled_time).seconds // 60)
    return max(1, self.urgency * 10 - delay)  # Ensure priority is always ≥ 1
def assign_patient_smart(self, patient):
    best_doctor = min(self.doctors.values(), key=lambda d: len(d.queue), default=None)
    if best_doctor:
        best_doctor.add_patient(patient)
        print(f"Patient {patient.patient_id} assigned to Doctor {best_doctor.doctor_id}")
    else:
        print("No available doctors.")
def estimate_wait_time(self, doctor_id):
    if doctor_id in self.doctors:
        num_patients = len(self.doctors[doctor_id].queue)
        if num_patients == 0:
            return 0  # No waiting time if queue is empty
        avg_consult_time = random.randint(8, 22)
        return num_patients * avg_consult_time
    return None  # If doctor_id is invalid

