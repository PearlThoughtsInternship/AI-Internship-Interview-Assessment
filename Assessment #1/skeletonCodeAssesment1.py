import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

# Load appointment data
df = pd.read_csv("D:/AI-Internship-Interview-Assessment---PealThoughts/Assessment #1/appointments.csv")  # Contains scheduled_time, actual_time, doctor_id, patient_id

# Feature Engineering
df['scheduled_time'] = pd.to_datetime(df['scheduled_time'])
df['actual_time'] = pd.to_datetime(df['actual_time'])
df['actual_end_time'] = pd.to_datetime(df['actual_end_time'])
df['arrival_time'] = pd.to_datetime(df['arrival_time'])

df['delay'] = (pd.to_datetime(df['actual_time']) - pd.to_datetime(df['scheduled_time'])).dt.total_seconds() / 60
df['consultation_duration'] = (df['actual_end_time'] - df['actual_time']).dt.total_seconds() / 60
df['early_arrival'] = (df['scheduled_time'] - df['arrival_time']).dt.total_seconds() /60
df['hour'] = pd.to_datetime(df['scheduled_time']).dt.hour
df['day_of_week'] = pd.to_datetime(df['scheduled_time']).dt.dayofweek
df['peak_hour'] = df['hour'].between(17, 20).astype(int)

# Define features and target variable
# features = ['doctor_id', 'hour', 'day_of_week']
features = ['doctor_id', 'hour', 'day_of_week', 'peak_hour', 'consultation_duration', 'early_arrival']
target = 'delay'

# Train AI Model
X = df[features]
y = df[target]

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Predict delay for future appointments
def predict_wait_time(doctor_id, scheduled_time, consultation_duration, early_arrival):
    hour = scheduled_time.hour
    day_of_week = scheduled_time.weekday()
    peak_hour = 1 if 17 <= hour <= 20 else 0
    input_data = pd.DataFrame([[doctor_id, hour, day_of_week, peak_hour, consultation_duration, early_arrival]], 
                              columns=features)
    return model.predict(input_data)[0]

# Optimize slot allocation and load balancing
def optimize_slots(current_time, queue, doctors):
    assignments = []
    for patient in queue:
        min_delay = float('inf')
        best_doctor = None
        for doctor in doctors:
            delay = predict_wait_time(
                doctor['id'], 
                patient['scheduled_time'], 
                doctor['avg_consultation_duration'], 
                patient['early_arrival']
            )
            if delay < min_delay:
                min_delay = delay
                best_doctor = doctor['id']
        assignments.append({
            'patient_id': patient['patient_id'],
            'doctor_id': best_doctor,
            'predicted_delay': min_delay,
            'scheduled_time': patient['scheduled_time']
        })
        send_sms(patient['patient_id'], min_delay)
    return assignments

# Addede an SMS Notification
def send_sms(patient_id, wait_time):
    print(f"SMS to patient {patient_id}: Your estimated wait time is {wait_time:.2f} minutes.")

# Simulate peak-hour scenario
def simulate_peak_hour(df, current_date=datetime(2025, 3, 26)):
    # Filter for peak hours (5-8 PM) on the given date
    peak_df = df[(df['scheduled_time'].dt.date == current_date.date()) & 
                 (df['scheduled_time'].dt.hour.between(17, 20))]
    
    # Calculate average consultation duration per doctor
    doctors = df.groupby('doctor_id')['consultation_duration'].mean().reset_index()
    doctors = [{'id': row['doctor_id'], 'avg_consultation_duration': row['consultation_duration']} 
               for _, row in doctors.iterrows()]
    
    # Create queue with early arrivals
    queue = [{'patient_id': row['patient_id'], 
              'scheduled_time': row['scheduled_time'], 
              'early_arrival': row['early_arrival']} 
             for _, row in peak_df.iterrows()]
    
    # Optimize slots
    current_time = datetime(current_date.year, current_date.month, current_date.day, 17, 0)
    assignments = optimize_slots(current_time, queue, doctors)
    
    # Calculate average wait time
    avg_wait_time = np.mean([a['predicted_delay'] for a in assignments]) if assignments else 0
    return assignments, avg_wait_time


def main():
    # Simulate peak hour and get assignments
    assignments, avg_wait_time = simulate_peak_hour(df)
    
    # Output results
    print("\nPeak Hour Assignments:")
    for assignment in assignments:
        print(f"Patient {assignment['patient_id']} assigned to Doctor {assignment['doctor_id']} "
              f"at {assignment['scheduled_time']} with predicted delay {assignment['predicted_delay']:.2f} mins")
    print(f"\nAverage predicted wait time: {avg_wait_time:.2f} minutes")
    
    # Check if 30% reduction achieved (from 40 minutes baseline)
    baseline_wait = 40
    target_wait = baseline_wait * 0.7
    reduction_percent = (baseline_wait - avg_wait_time) / baseline_wait * 100
    print(f"Wait time reduction: {reduction_percent:.2f}% (Target: >= 30%)")

# Example usage
# predicted_delay = predict_wait_time(doctor_id=5, scheduled_time=datetime(2024, 3, 26, 18, 30))
# print(f"Expected wait time: {predicted_delay:.2f} minutes")
if __name__ == "__main__":
    main()