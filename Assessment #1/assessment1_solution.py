import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from datetime import datetime, timedelta

# Load appointment data
df = pd.read_csv("appointments.csv")  # Scheduled vs. actual, doctor_id, patient_id

# Add delay and time-based features
df['scheduled_time'] = pd.to_datetime(df['scheduled_time'])
df['actual_time'] = pd.to_datetime(df['actual_time'])
df['delay'] = (df['actual_time'] - df['scheduled_time']).dt.total_seconds() / 60
df['hour'] = df['scheduled_time'].dt.hour
df['day_of_week'] = df['scheduled_time'].dt.dayofweek

# ML features
features = ['doctor_id', 'hour', 'day_of_week']
target = 'delay'
X = df[features]
y = df[target]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error on test set: {mae:.2f} minutes")

def predict_wait_time(doctor_id, scheduled_time):
    hour = scheduled_time.hour
    day_of_week = scheduled_time.weekday()
    return model.predict([[doctor_id, hour, day_of_week]])[0]

def handle_early_arrival(doctor_id, scheduled_time, arrival_time):
    predicted_delay = predict_wait_time(doctor_id, scheduled_time)
    early_by = (scheduled_time - arrival_time).total_seconds() / 60
    adjusted_wait = max(predicted_delay - early_by, 0)
    return adjusted_wait

def adjust_slot(doctor_id, scheduled_time):
    delay = predict_wait_time(doctor_id, scheduled_time)
    if delay > 30:
        return scheduled_time + timedelta(minutes=delay)
    return scheduled_time

# Example usage
example_time = datetime(2024, 3, 26, 18, 30)
arrival = example_time - timedelta(minutes=20)
doctor_id = 5

predicted = predict_wait_time(doctor_id, example_time)
adjusted = adjust_slot(doctor_id, example_time)
early_wait = handle_early_arrival(doctor_id, example_time, arrival)

print(f"Predicted delay: {predicted:.2f} mins")
print(f"Adjusted slot time: {adjusted.strftime('%H:%M')}")
print(f"Wait time if patient arrives early: {early_wait:.2f} mins")
