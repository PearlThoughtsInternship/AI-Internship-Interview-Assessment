import heapq
from datetime import datetime, timedelta
import random
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

class Doctor:
    """
    Represents a doctor with a queue of patients.

    Attributes:
        doctor_id (int): The unique identifier for the doctor.
        availability_blocks (list): List of time blocks when the doctor is available.
    """
    def __init__(self, doctor_id, availability_blocks):
        self.doctor_id = doctor_id
        self.queue = []
        self.availability_blocks = availability_blocks  # Example: [(9, 12), (15, 18)]
    
    def add_patient(self, patient):
        """Adds a patient to the doctor's queue."""
        heapq.heappush(self.queue, (patient.priority, patient))
    
    def next_patient(self):
        """Returns the next patient in the queue, if available."""
        if self.queue:
            return heapq.heappop(self.queue)[1]
        return None

class Patient:
    """
    Represents a patient with attributes for managing their queue position.

    Attributes:
        patient_id (int): The unique identifier for the patient.
        arrival_time (datetime): The time the patient arrived.
        scheduled_time (datetime): The time the patient is scheduled for consultation.
        urgency (int): The urgency level of the patient's case.
        source (str): The source of the patient's appointment (e.g., 'App', 'Walk-in').
    """
    def __init__(self, patient_id, arrival_time, scheduled_time, urgency, source):
        if urgency < 1 or urgency > 5:
            raise ValueError("Urgency must be between 1 and 5.")
        self.patient_id = patient_id
        self.arrival_time = arrival_time
        self.scheduled_time = scheduled_time
        self.urgency = urgency
        self.source = source  # 'App', 'Walk-in', 'WhatsApp', etc.
        self.priority = self.calculate_priority()

    def calculate_priority(self):
        """Calculates the priority of the patient based on urgency and delay."""
        delay = max(0, (self.arrival_time - self.scheduled_time).seconds // 60)
        return self.urgency * 10 - delay

class QueueManagementSystem:
    """
    Manages the queue of patients for multiple doctors.

    Attributes:
        doctors (dict): A dictionary mapping doctor IDs to Doctor objects.
    """
    def __init__(self):
        self.doctors = {}

    def add_doctor(self, doctor_id, availability_blocks):
        """Adds a doctor to the system."""
        self.doctors[doctor_id] = Doctor(doctor_id, availability_blocks)

    def assign_patient(self, doctor_id, patient):
        """Assigns a patient to a specific doctor."""
        if doctor_id in self.doctors:
            self.doctors[doctor_id].add_patient(patient)
        else:
            logging.error(f"Doctor {doctor_id} not found.")

    def estimate_wait_time(self, doctor_id):
        """Estimates the wait time for a specific doctor."""
        if doctor_id in self.doctors:
            num_patients = len(self.doctors[doctor_id].queue)
            avg_consult_time = random.randint(8, 22)  # Simulating consult times
            return num_patients * avg_consult_time
        return None

    def process_next_patient(self, doctor_id):
        """Processes the next patient in the queue for a specific doctor."""
        if doctor_id in self.doctors:
            patient = self.doctors[doctor_id].next_patient()
            if patient:
                print(f"Doctor {doctor_id} is now consulting Patient {patient.patient_id}.")
            else:
                print(f"No patients in the queue for Doctor {doctor_id}.")
        else:
            print(f"Doctor {doctor_id} not found.")

# Example Usage
if __name__ == "__main__":
    qms = QueueManagementSystem()
    qms.add_doctor(1, [(9, 12), (15, 18)])

    # Simulating patient arrivals
    patient1 = Patient(101, datetime.now(), datetime.now() + timedelta(minutes=15), urgency=2, source="App")
    patient2 = Patient(102, datetime.now(), datetime.now() + timedelta(minutes=10), urgency=3, source="Walk-in")

    qms.assign_patient(1, patient1)
    qms.assign_patient(1, patient2)

    print(f"Estimated wait time for Doctor 1: {qms.estimate_wait_time(1)} minutes")

    # Process the next patient
    qms.process_next_patient(1)
    print(f"Estimated wait time for Doctor 1 after processing: {qms.estimate_wait_time(1)} minutes")
