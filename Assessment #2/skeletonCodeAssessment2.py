import heapq
from datetime import datetime, timedelta
import random

class Doctor:
    def __init__(self, doctor_id, availability_blocks):
        self.doctor_id = doctor_id
        self.queue = []  # Elements are (priority, patient_id, patient)
        self.availability_blocks = availability_blocks  # Example: [(9, 12), (15, 18)]
        self.status_tracking = {}  # patient_id -> status ("waiting", "consulted")

    def add_patient(self, patient):
        # Include patient.patient_id as a tie-breaker to avoid comparing Patient objects directly.
        heapq.heappush(self.queue, (patient.priority, patient.patient_id, patient))
        self.status_tracking[patient.patient_id] = "waiting"

    def next_patient(self):
        if self.queue:
            _, _, patient = heapq.heappop(self.queue)
            self.status_tracking[patient.patient_id] = "consulted"
            return patient
        return None

    def get_waiting_patients(self):
        return [patient.patient_id for _, _, patient in self.queue]

class Patient:
    def __init__(self, patient_id, arrival_time, scheduled_time, urgency, source):
        self.patient_id = patient_id
        self.arrival_time = arrival_time
        self.scheduled_time = scheduled_time
        self.urgency = urgency
        self.source = source  # 'App', 'Walk-in', 'WhatsApp', etc.
        self.priority = self.calculate_priority()

    def calculate_priority(self):
        # Calculate delay in minutes, if any
        delay = max(0, int((self.arrival_time - self.scheduled_time).total_seconds() // 60))
        # Walk-ins have slightly lower priority (hence lower bonus) than other channels
        source_priority = 1 if self.source == "Walk-in" else 2
        # Multiply urgency to emphasize critical cases; negative for min-heap ordering
        return -(self.urgency * 10 - delay + source_priority)

class QueueManagementSystem:
    def __init__(self):
        self.doctors = {}
        self.patient_log = {}  # Track all patients with details

    def add_doctor(self, doctor_id, availability_blocks):
        self.doctors[doctor_id] = Doctor(doctor_id, availability_blocks)

    def assign_patient(self, doctor_id, patient):
        if doctor_id in self.doctors:
            self.doctors[doctor_id].add_patient(patient)
            self.patient_log[patient.patient_id] = {
                "doctor_id": doctor_id,
                "status": "waiting",
                "arrival_time": patient.arrival_time,
                "source": patient.source
            }

    def update_patient_status(self, doctor_id, patient_id, new_status):
        if doctor_id in self.doctors:
            self.doctors[doctor_id].status_tracking[patient_id] = new_status
            if patient_id in self.patient_log:
                self.patient_log[patient_id]["status"] = new_status

    def estimate_wait_time(self, doctor_id):
        if doctor_id in self.doctors:
            num_patients = len(self.doctors[doctor_id].queue)
            avg_consult_time = 15  # Default average consult time per patient in minutes
            return num_patients * avg_consult_time
        return 0

    def notify_patient(self, patient_id):
        if patient_id in self.patient_log:
            status = self.patient_log[patient_id]["status"]
            eta = self.estimate_wait_time(self.patient_log[patient_id]["doctor_id"])
            return f"Patient {patient_id}: Status: {status}, Estimated Wait Time: {eta} minutes"
        return "Patient not found"


# --- Scenario Testing ---
if __name__ == '__main__':
    # Initialize the Queue Management System and add two doctors
    qms = QueueManagementSystem()
    qms.add_doctor(1, [(9, 12), (15, 18)])
    qms.add_doctor(2, [(10, 13), (16, 19)])

    now = datetime.now()

    # Scenario 1: Patient arrives exactly on time
    patient_on_time = Patient(201, now, now, urgency=3, source="App")
    qms.assign_patient(1, patient_on_time)
    print("Scenario 1: Patient arrives on time")
    print(qms.notify_patient(201))

    # Scenario 2: Patient arrives early (before scheduled time)
    patient_early = Patient(202, now, now + timedelta(minutes=20), urgency=3, source="App")
    qms.assign_patient(1, patient_early)
    print("\nScenario 2: Patient arrives early")
    print(qms.notify_patient(202))

    # Scenario 3: Patient arrives late (delayed arrival)
    patient_late = Patient(203, now + timedelta(minutes=15), now, urgency=3, source="WhatsApp")
    qms.assign_patient(1, patient_late)
    print("\nScenario 3: Patient arrives late (delayed)")
    print(qms.notify_patient(203))

    # Scenario 4: Comparing Walk-in vs App booking for priority differences
    patient_walkin = Patient(204, now, now + timedelta(minutes=5), urgency=4, source="Walk-in")
    patient_app = Patient(205, now, now + timedelta(minutes=5), urgency=4, source="App")
    qms.assign_patient(1, patient_walkin)
    qms.assign_patient(1, patient_app)
    print("\nScenario 4: Walk-in vs App booking")
    print(qms.notify_patient(204))
    print(qms.notify_patient(205))

    # Scenario 5: Estimating wait time for Doctor 1 with multiple patients waiting
    wait_time_doc1 = qms.estimate_wait_time(1)
    print("\nScenario 5: Estimated wait time for Doctor 1")
    print(f"Doctor 1 wait time: {wait_time_doc1} minutes")

    # Scenario 6: Processing the next patient in Doctor 1's queue
    next_patient = qms.doctors[1].next_patient()
    if next_patient:
        qms.update_patient_status(1, next_patient.patient_id, "consulted")
        print("\nScenario 6: Doctor sees next patient")
        print(f"Processed patient {next_patient.patient_id}")
        print(qms.notify_patient(next_patient.patient_id))
    else:
        print("\nScenario 6: No patients in queue to process.")

    # Scenario 7: Query for a non-existent patient (edge case)
    print("\nScenario 7: Query non-existent patient")
    print(qms.notify_patient(999))

    # Scenario 8: Handling a patient assignment for Doctor 2
    patient_doc2 = Patient(301, now, now + timedelta(minutes=10), urgency=2, source="App")
    qms.assign_patient(2, patient_doc2)
    print("\nScenario 8: Doctor 2 patient assignment")
    print(qms.notify_patient(301))
    wait_time_doc2 = qms.estimate_wait_time(2)
    print(f"Doctor 2 wait time: {wait_time_doc2} minutes")
