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
        self.status = "Arrived"  # Default status upon creation

    def calculate_priority(self):
        # Higher priority for urgent cases, walk-ins may have lower priority
        delay = max(0, (self.arrival_time - self.scheduled_time).seconds // 60)
        return self.urgency * 10 - delay

    def update_status(self, new_status):
        self.status = new_status

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
        return None
    
    def check_in_patient(self, patient_id):
        for doctor in self.doctors.values():
            for patient in doctor.queue:
                if patient[1].patient_id == patient_id:
                    patient[1].update_status("Waiting")
                    print(f"Patient {patient_id} has checked in and is now waiting.")
                    return
        print(f"Patient {patient_id} not found in the queue.")

    def confirm_check_in(self, patient_id):
        print(f"Confirmation sent to Patient {patient_id} that the doctor is ready.")

# Example Usage
if __name__ == "__main__":
    qms = QueueManagementSystem()
    qms.add_doctor(1, [(9, 12), (15, 18)])

    patient1 = Patient(101, datetime.now(), datetime.now() + timedelta(minutes=15), urgency=2, source="App")
    patient2 = Patient(102, datetime.now(), datetime.now() + timedelta(minutes=10), urgency=3, source="Walk-in")

    qms.assign_patient(1, patient1)
    qms.assign_patient(1, patient2)

    print(f"Estimated wait time for Doctor 1: {qms.estimate_wait_time(1)} minutes")

    # Check-In Example
    qms.check_in_patient(101)

    # Assuming patient 101 is next, confirm check-in
    qms.confirm_check_in(101)