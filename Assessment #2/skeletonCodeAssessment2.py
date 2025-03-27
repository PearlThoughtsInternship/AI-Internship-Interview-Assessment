import heapq
from datetime import datetime, timedelta
import random

class Doctor:
    def __init__(self, doctor_id, availability_blocks):
        self.doctor_id = doctor_id
        self.queue = []
        self.availability_blocks = availability_blocks  # Example: [(9, 12), (15, 18)] for shift timing
        self.schedule = {}  # To track doctor availability dynamically
    
    def add_patient(self, patient):
        # Check if the patient arrives during available hours
        if self.is_available(patient.scheduled_time):
            heapq.heappush(self.queue, (patient.priority, patient))
        else:
            print(f"Doctor {self.doctor_id} is not available at the scheduled time.")
    
    def next_patient(self):
        if self.queue:
            return heapq.heappop(self.queue)[1]
        return None
    
    def is_available(self, scheduled_time):
        # Check if the doctor's availability overlaps with the patient's scheduled time
        for start, end in self.availability_blocks:
            availability_start = scheduled_time.replace(hour=start, minute=0, second=0)
            availability_end = scheduled_time.replace(hour=end, minute=0, second=0)
            if availability_start <= scheduled_time <= availability_end:
                return True
        return False

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
        return 0

    def handle_walkins(self, doctor_id, patient):
        # Special handling for walk-ins (may have lower priority)
        patient.urgency = 1  # Walk-ins get a default urgency of 1
        self.assign_patient(doctor_id, patient)

# Example Usage
qms = QueueManagementSystem()
qms.add_doctor(1, [(9, 12), (15, 18)])  # Doctor 1 is available from 9-12 and 15-18

# Simulate patients
patient1 = Patient(101, datetime.now(), datetime.now() + timedelta(minutes=15), urgency=2, source="App")
patient2 = Patient(102, datetime.now(), datetime.now() + timedelta(minutes=10), urgency=3, source="Walk-in")

# Assign patients to the doctor
qms.assign_patient(1, patient1)
qms.handle_walkins(1, patient2)

# Check the estimated wait time for Doctor 1
print(f"Estimated wait time for Doctor 1: {qms.estimate_wait_time(1)} minutes")

# Test to see the next patient
next_patient = qms.doctors[1].next_patient()
if next_patient:
    print(f"Next patient for Doctor 1: {next_patient.patient_id}")
else:
    print("No patients in the queue for Doctor 1.")

