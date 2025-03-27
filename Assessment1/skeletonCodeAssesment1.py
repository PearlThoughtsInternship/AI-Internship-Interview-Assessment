import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

# Load appointment data
df = pd.read_csv("appointments.csv")  # Contains scheduled_time, actual_time, doctor_id, patient_id

# Feature Engineering
df['scheduled_time'] = pd.to_datetime(df['scheduled_time'])
df['actual_time'] = pd.to_datetime(df['actual_time'])
df['delay'] = (df['actual_time'] - df['scheduled_time']).dt.total_seconds() / 60
df['hour'] = df['scheduled_time'].dt.hour
df['day_of_week'] = df['scheduled_time'].dt.dayofweek
df['doctor_avg_duration'] = df.groupby('doctor_id')['delay'].transform('mean')
df['patients_ahead'] = df.groupby(['doctor_id', 'scheduled_time'])['patient_id'].cumcount()

def predict_wait_time(doctor_id, scheduled_time):
    """Predicts wait time for a given doctor and scheduled appointment time."""
    hour = scheduled_time.hour
    day_of_week = scheduled_time.weekday()
    patients_ahead = len(df[(df['doctor_id'] == doctor_id) & (df['scheduled_time'] <= scheduled_time)])
    avg_duration = df[df['doctor_id'] == doctor_id]['doctor_avg_duration'].mean()
    
    return model.predict([[doctor_id, hour, day_of_week, patients_ahead, avg_duration]])[0]

# Define features and target variable
features = ['doctor_id', 'hour', 'day_of_week', 'patients_ahead', 'doctor_avg_duration']
target = 'delay'

# Train AI Model
X = df[features]
y = df[target]

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Dynamic slot allocation

def optimize_time_slot(patient_id, preferred_time):
    """Suggests an optimized time slot based on current congestion."""
    doctor_availability = df.groupby('doctor_id')['delay'].mean().idxmin()
    adjusted_time = preferred_time + timedelta(minutes=5) if predict_wait_time(doctor_availability, preferred_time) > 30 else preferred_time
    return doctor_availability, adjusted_time

# Example usage
scheduled_time = datetime(2024, 3, 26, 18, 30)
predicted_delay = predict_wait_time(doctor_id=5, scheduled_time=scheduled_time)
print(f"Expected wait time: {predicted_delay:.2f} minutes")

optimized_doctor, optimized_time = optimize_time_slot(patient_id=101, preferred_time=scheduled_time)
print(f"Suggested doctor: {optimized_doctor}, Adjusted Time: {optimized_time}")
