import heapq
from datetime import datetime, timedelta
import random

class Doctor:
    def __init__(self, doctor_id, availability_blocks,accepts_walkins=False):
        self.doctor_id = doctor_id
        self.queue = []
        self.availability_blocks = availability_blocks  # Example: [(9, 12), (15, 18)] for shift timing
        self.accepts_walkins = accepts_walkins  # True/False
        self.avg_consult_time = random.randint(8, 22)  # Fixed per doctor
    
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
        base_priority = self.urgency * 10  # Lower = better
        
        # Penalize late arrivals
        if self.scheduled_time:
            delay = max(0, (self.arrival_time - self.scheduled_time).seconds // 60)
            base_priority += delay
        
        # Channel-specific adjustments
        if self.source == "Walk-in" and self.urgency > 1:  
            base_priority += 15  # Heavy penalty for non-urgent walk-ins
        elif self.source == "IVR":
            base_priority += 5  # Small penalty for IVR bookings
        
        return base_priority

class QueueManagementSystem:
    def __init__(self):
        self.doctors = {}

    def add_doctor(self, doctor_id, availability_blocks,accepts_walkins=False):
        self.doctors[doctor_id] = Doctor(doctor_id, availability_blocks,accepts_walkins)

    def is_doctor_available(self, doctor, patient_arrival_time):
      # Strip seconds & microseconds
      patient_time = patient_arrival_time.replace(second=0, microsecond=0)
      for start, end in doctor.availability_blocks:
            start_time = datetime.combine(patient_arrival_time.date(), time(start, 0))
            end_time = datetime.combine(patient_arrival_time.date(), time(end, 0))
            if start_time <= patient_arrival_time <= end_time:
                return True
      return False

    def does_doctor_accept_walkins(self, doctor):
        return doctor.accepts_walkins

    def assign_patient(self, patient):
        # Step 1: Find available doctors at the patient's arrival time
        available_doctors = [
            d for d in self.doctors.values() 
            if self.is_doctor_available(d, patient.arrival_time)
        ]

        if not available_doctors:
            raise ValueError("No available doctors for the patient's timeslot")

        # Step 2: Find the best doctor based on queue length + compatibility
        def doctor_score(doctor):
            channel_penalty = 0
            if patient.source == "Walk_in" and not self.does_doctor_accept_walkins(doctor):
                channel_penalty = float('inf')  # Disqualify if doctor doesn't take walk-ins
            return len(doctor.queue) + channel_penalty

        best_doctor = min(available_doctors, key=doctor_score)
        best_doctor.add_patient(patient)

    def estimate_wait_time(self, doctor_id):
        if doctor_id in self.doctors:
            num_patients = len(self.doctors[doctor_id].queue)
            return num_patients * self.doctors[doctor_id].avg_consult_time  # Use fixed value_time
        return None

# Example Usage
qms = QueueManagementSystem()
qms.add_doctor(1, [(8, 11), (15, 18)],accepts_walkins=True)
qms.add_doctor(2, [(8, 11), (15, 18)],accepts_walkins=False)

current_time = datetime.now().replace(hour=8, minute=46, second=0, microsecond=0)
patient1 = Patient(101, current_time, current_time + timedelta(minutes=15), urgency=2, source="App")
patient2 = Patient(102, current_time, current_time + timedelta(minutes=10), urgency=3, source="Walk-in")

qms.assign_patient(patient1)
qms.assign_patient(patient2)

print(f"Estimated wait time for Doctor 1: {qms.estimate_wait_time(1)} minutes")
