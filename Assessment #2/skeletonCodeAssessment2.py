import heapq
from datetime import datetime, timedelta
import random
import statistics

class Doctor:
    def __init__(self, doctor_id, availability_blocks, tracks_status=False):
        self.doctor_id = doctor_id
        self.queue = []
        self.availability_blocks = availability_blocks  # Example: [(9, 12), (15, 18)] for shift timing
        self.tracks_status = tracks_status
        self.avg_consult_time = random.randint(5, 15)  # Average minutes per patient
        self.current_patient = None
        self.patients_seen_today = 0
        self.historic_consult_times = []
    
    def add_patient(self, patient):
        heapq.heappush(self.queue, (patient.priority, patient))
        patient.status = "waiting"
        patient.waiting_start = datetime.now()
        return len(self.queue)
    
    def next_patient(self):
        if self.queue:
            _, patient = heapq.heappop(self.queue)
            self.current_patient = patient
            if self.tracks_status:
                patient.status = "consulting"
                patient.consult_start = datetime.now()
            return patient
        return None
    
    def finish_consultation(self):
        if self.current_patient and self.tracks_status:
            self.current_patient.status = "completed"
            consult_time = (datetime.now() - self.current_patient.consult_start).seconds // 60
            self.historic_consult_times.append(consult_time)
            self.patients_seen_today += 1
            if len(self.historic_consult_times) > 10:
                self.avg_consult_time = statistics.mean(self.historic_consult_times[-10:])
            self.current_patient = None
    
    def is_available(self, current_time):
        # Convert datetime to hour
        hour = current_time.hour
        for start, end in self.availability_blocks:
            if start <= hour < end:
                return True
        return False
    
    def get_capacity(self):
        total_hours = sum(end - start for start, end in self.availability_blocks)
        return total_hours * 60 // self.avg_consult_time  # Patients per day

class Patient:
    def __init__(self, patient_id, arrival_time, scheduled_time, urgency, source):
        self.patient_id = patient_id
        self.arrival_time = arrival_time
        self.scheduled_time = scheduled_time
        self.urgency = urgency  # 1-5 scale where 5 is most urgent
        self.source = source  # 'App', 'Walk-in', 'WhatsApp', 'IVR'
        self.status = "registered"  # registered, arrived, waiting, consulting, completed
        self.waiting_start = None
        self.consult_start = None
        self.priority = self.calculate_priority()
        self.notifications_sent = []
        
    def calculate_priority(self):
        # Balance between urgency, punctuality, and appointment type
        base_priority = self.urgency * 20
        
        # Patients who arrive close to scheduled time get priority
        if self.scheduled_time:
            time_diff = abs((self.arrival_time - self.scheduled_time).total_seconds() / 60)
            punctuality_factor = max(0, 30 - time_diff) if time_diff <= 30 else -10
            base_priority += punctuality_factor
        
        # Source-based adjustments
        source_priority = {
            'App': 5,        # Reward digital appointment
            'WhatsApp': 5,   # Reward digital appointment
            'IVR': 3,        # Standard priority
            'Walk-in': -10   # Lower priority unless urgent
        }
        
        base_priority += source_priority.get(self.source, 0)
        
        # Waiting time adjustment (recalculated when needed)
        if self.waiting_start:
            wait_time_minutes = (datetime.now() - self.waiting_start).seconds // 60
            # Gradually increase priority with wait time
            base_priority += min(wait_time_minutes // 5, 20)
        
        return base_priority
    
    def update_priority(self):
        self.priority = self.calculate_priority()
        return self.priority
    
    def waiting_time(self):
        if not self.waiting_start:
            return 0
        if self.status == "waiting":
            return (datetime.now() - self.waiting_start).seconds // 60
        return 0

class QueueManagementSystem:
    def __init__(self):
        self.doctors = {}
        self.patients = {}
        self.metrics = {
            'avg_wait_time': [],
            'patient_satisfaction': [],
            'queue_efficiency': [],
            'doctor_utilization': {}
        }
    
    def add_doctor(self, doctor_id, availability_blocks, tracks_status=False):
        self.doctors[doctor_id] = Doctor(doctor_id, availability_blocks, tracks_status)
        self.metrics['doctor_utilization'][doctor_id] = []
    
    def register_patient(self, patient_id, scheduled_time, urgency, source):
        arrival_time = datetime.now()
        patient = Patient(patient_id, arrival_time, scheduled_time, urgency, source)
        self.patients[patient_id] = patient
        return patient
    
    def check_in_patient(self, patient_id):
        if patient_id in self.patients:
            patient = self.patients[patient_id]
            patient.status = "arrived"
            patient.arrival_time = datetime.now()
            return True
        return False
    
    def find_optimal_doctor(self, patient):
        best_doctor_id = None
        shortest_wait = float('inf')
        
        current_time = datetime.now()
        
        for doctor_id, doctor in self.doctors.items():
            # Skip doctors who aren't available
            if not doctor.is_available(current_time):
                continue
                
            wait_time = self.estimate_wait_time(doctor_id)
            
            # Consider doctor's capacity and specialization (simplified here)
            if doctor.patients_seen_today < doctor.get_capacity():
                # Shorter wait time is better
                if wait_time < shortest_wait:
                    shortest_wait = wait_time
                    best_doctor_id = doctor_id
        
        return best_doctor_id
    
    def assign_patient(self, doctor_id, patient):
        if doctor_id in self.doctors:
            queue_position = self.doctors[doctor_id].add_patient(patient)
            self.notify_patient(patient.patient_id, f"You have been assigned to Doctor {doctor_id}. Your queue position is {queue_position}.")
            return queue_position
        return None
    
    def auto_assign_patient(self, patient_id):
        if patient_id in self.patients:
            patient = self.patients[patient_id]
            optimal_doctor = self.find_optimal_doctor(patient)
            
            if optimal_doctor:
                return self.assign_patient(optimal_doctor, patient)
            else:
                # No available doctors
                self.notify_patient(patient_id, "No doctors available at this time. Please wait or reschedule.")
                return None
        return None
    
    def estimate_wait_time(self, doctor_id):
        if doctor_id in self.doctors:
            doctor = self.doctors[doctor_id]
            num_patients = len(doctor.queue)
            return num_patients * doctor.avg_consult_time
        return None
    
    def notify_patient(self, patient_id, message):
        if patient_id in self.patients:
            patient = self.patients[patient_id]
            patient.notifications_sent.append((datetime.now(), message))
            # In a real system, this would send SMS, app notification, etc.
            return True
        return False
    
    def update_wait_times(self):
        for doctor_id, doctor in self.doctors.items():
            for _, patient in doctor.queue:
                wait_time = self.estimate_wait_time(doctor_id)
                if wait_time > 30:  # If wait time exceeds 30 minutes
                    self.notify_patient(patient.patient_id, 
                                       f"Your current estimated wait time is {wait_time} minutes. Would you like to reschedule?")
    
    def process_next_patient(self, doctor_id):
        if doctor_id in self.doctors:
            doctor = self.doctors[doctor_id]
            patient = doctor.next_patient()
            if patient:
                wait_time = patient.waiting_time()
                self.metrics['avg_wait_time'].append(wait_time)
                self.notify_patient(patient.patient_id, "Doctor is ready to see you now.")
                return patient
        return None
    
    def complete_consultation(self, doctor_id):
        if doctor_id in self.doctors:
            doctor = self.doctors[doctor_id]
            doctor.finish_consultation()
            # Update doctor utilization metrics
            self.metrics['doctor_utilization'][doctor_id].append(doctor.patients_seen_today)
            return True
        return False
    
    def collect_feedback(self, patient_id, satisfaction_score):
        if patient_id in self.patients:
            self.metrics['patient_satisfaction'].append(satisfaction_score)
            return True
        return False
    
    def calculate_queue_efficiency(self):
        for doctor_id, doctor in self.doctors.items():
            efficiency = doctor.patients_seen_today / doctor.get_capacity() if doctor.get_capacity() > 0 else 0
            self.metrics['queue_efficiency'].append(efficiency)
        return statistics.mean(self.metrics['queue_efficiency']) if self.metrics['queue_efficiency'] else 0
    
    def get_system_metrics(self):
        metrics = {
            'avg_wait_time': statistics.mean(self.metrics['avg_wait_time']) if self.metrics['avg_wait_time'] else 0,
            'patient_satisfaction': statistics.mean(self.metrics['patient_satisfaction']) if self.metrics['patient_satisfaction'] else 0,
            'queue_efficiency': self.calculate_queue_efficiency(),
            'doctor_utilization': {doc_id: statistics.mean(vals) if vals else 0 
                                 for doc_id, vals in self.metrics['doctor_utilization'].items()}
        }
        return metrics

# Example Usage
if __name__ == "__main__":
    # Initialize system
    qms = QueueManagementSystem()
    
    # Add doctors with different schedules and status tracking capabilities
    qms.add_doctor(1, [(9, 12), (13, 16)], tracks_status=True)
    qms.add_doctor(2, [(10, 13), (14, 17)], tracks_status=False)
    
    # Register patients from different sources
    patient1 = qms.register_patient(101, datetime.now() + timedelta(minutes=15), urgency=2, source="App")
    patient2 = qms.register_patient(102, datetime.now() + timedelta(minutes=10), urgency=4, source="Walk-in")
    patient3 = qms.register_patient(103, datetime.now() - timedelta(minutes=5), urgency=3, source="WhatsApp")
    
    # Check-in patients
    qms.check_in_patient(101)
    qms.check_in_patient(102)
    qms.check_in_patient(103)
    
    # Auto-assign patients to optimal doctors
    qms.auto_assign_patient(101)
    qms.auto_assign_patient(102)
    qms.auto_assign_patient(103)
    
    # Process patients
    patient = qms.process_next_patient(1)
    if patient:
        print(f"Doctor 1 is now seeing patient {patient.patient_id}")
        # Simulate consultation
        qms.complete_consultation(1)
    
    # Get wait time estimates
    print(f"Estimated wait time for Doctor 1: {qms.estimate_wait_time(1)} minutes")
    print(f"Estimated wait time for Doctor 2: {qms.estimate_wait_time(2)} minutes")
    
    # Collect feedback
    qms.collect_feedback(101, 4.5)  # Scale of 1-5
    
    # Get system metrics
    metrics = qms.get_system_metrics()
    print(f"System Metrics: {metrics}")
