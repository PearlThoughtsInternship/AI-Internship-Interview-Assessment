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
    def __init__(self, num_doctors=50):
        self.doctors = {i: Doctor(i,self.generate_schedule()) for i in range(1, num_doctors + 1)}

    def generate_schedule(self):
        morning_start = random.randint(8, 10)
        evening_start = random.randint(14, 16)
        return [(morning_start,morning_start+3), (evening_start, evening_start+3)]
    
    
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
    
    # def generate_random_patient(self):
    #     patient_id = random.randint(1000, 9999)
    #     arrival_time = datetime.now()
    #     scheduled_time = arrival_time + timedelta(minutes=random.randint(-30,30))
    #     urgency = random.randint(1,5)
    #     source = random.choice(['App','Walk-in','WhatsApp','IVR'])
    #     return Patient(patient_id,arrival_time, scheduled_time, urgency, source)
    
# Example Usage
qms = QueueManagementSystem()
qms.add_doctor(1, [(9, 12), (15, 18)])

patient1 = Patient(101, datetime.now(), datetime.now() + timedelta(minutes=15), urgency=2, source="App")
patient2 = Patient(102, datetime.now(), datetime.now() + timedelta(minutes=10), urgency=3, source="Walk-in")
patient3 = Patient(103,datetime.now(),datetime.now()+timedelta(minutes=20), urgency=1,source="WhatsApp")

qms.assign_patient(1, patient1)
qms.assign_patient(1, patient2)
qms.assign_patient(1,patient3)

print(f"Estimated wait time for Doctor 1: {qms.estimate_wait_time(1)} minutes")
print(f"Patients assigned to Doctor 1:")

for priority, patient in qms.doctors[1].queue:
    print(f"Patient ID: {patient.patient_id}, Estimated Wait Time: {qms.estimate_wait_time(1)} minutes")
