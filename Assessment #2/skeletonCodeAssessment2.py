import heapq
from datetime import datetime, timedelta
import random

class Doctor:
    def __init__(self, doctor_id, availability_blocks):
        self.doctor_id = doctor_id
        self.queue = []
        self.availability_blocks = availability_blocks  
    
    def add_patient(self, patient):
        heapq.heappush(self.queue, (patient.priority, patient))
    
    def next_patient(self):
        if self.queue:
            return heapq.heappop(self.queue)[1]
        return None
    
    def is_available(self, current_time):
        for start, end in self.availability_blocks:
            if start <= current_time.hour < end:
                return True
        return False

class Patient:
    def __init__(self, patient_id, arrival_time, scheduled_time, urgency, source):
        self.patient_id = patient_id
        self.arrival_time = arrival_time
        self.scheduled_time = scheduled_time
        self.urgency = urgency
        self.source = source  
        self.priority = self.calculate_priority()

    def calculate_priority(self):
        delay = max(0, (self.arrival_time - self.scheduled_time).seconds // 60)
        source_priority = 5 if self.source == 'App' else 1  
        return self.urgency * 10 - delay + source_priority

class QueueManagementSystem:
    def __init__(self):
        self.doctors = {}

    def add_doctor(self, doctor_id, availability_blocks):
        self.doctors[doctor_id] = Doctor(doctor_id, availability_blocks)

    def assign_patient(self, doctor_id, patient):
        if doctor_id in self.doctors and self.doctors[doctor_id].is_available(datetime.now()):
            self.doctors[doctor_id].add_patient(patient)

    def estimate_wait_time(self, doctor_id):
        if doctor_id in self.doctors:
            num_patients = len(self.doctors[doctor_id].queue)
            avg_consult_time = random.randint(8, 22)  
            return num_patients * avg_consult_time

qms = QueueManagementSystem()
qms.add_doctor(1, [(9, 12), (15, 18)])

patient1 = Patient(101, datetime.now(), datetime.now() + timedelta(minutes=15), urgency=2, source="App")
patient2 = Patient(102, datetime.now(), datetime.now() + timedelta(minutes=10), urgency=3, source="Walk-in")

qms.assign_patient(1, patient1)
qms.assign_patient(1, patient2)

print(f"Estimated wait time for Doctor 1: {qms.estimate_wait_time(1)} minutes")
