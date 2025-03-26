import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

# Load appointment data
df = pd.read_csv("appointments.csv")  # Contains scheduled_time, actual_time, doctor_id, patient_id

# Feature Engineering
df['delay'] = (pd.to_datetime(df['actual_time']) - pd.to_datetime(df['scheduled_time'])).dt.total_seconds() / 60
df['hour'] = pd.to_datetime(df['scheduled_time']).dt.hour
df['day_of_week'] = pd.to_datetime(df['scheduled_time']).dt.dayofweek

# Define features and target variable
features = ['doctor_id', 'hour', 'day_of_week']
target = 'delay'

# Train AI Model
X = df[features]
y = df[target]

model = RandomForestRegressor()
model.fit(X, y)

# Predict delay for future appointments
def predict_wait_time(doctor_id, scheduled_time):
    hour = scheduled_time.hour
    day_of_week = scheduled_time.weekday()
    return model.predict([[doctor_id, hour, day_of_week]])[0]  # Predicted delay in minutes

# Example usage
predicted_delay = predict_wait_time(doctor_id=5, scheduled_time=datetime(2024, 3, 26, 18, 30))
print(f"Expected wait time: {predicted_delay:.2f} minutes")
