import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

# Load appointment data (Ensure this CSV file has the proper structure)
df = pd.read_csv("appointments.csv")  # Contains scheduled_time, actual_time, doctor_id, patient_id

# Feature Engineering
df['scheduled_time'] = pd.to_datetime(df['scheduled_time'])
df['actual_time'] = pd.to_datetime(df['actual_time'])
df['delay'] = (df['actual_time'] - df['scheduled_time']).dt.total_seconds() / 60  # Delay in minutes
df['hour'] = df['scheduled_time'].dt.hour
df['day_of_week'] = df['scheduled_time'].dt.dayofweek

# Define features and target variable
features = ['doctor_id', 'hour', 'day_of_week']
target = 'delay'

# Train AI Model
X = df[features]
y = df[target]

# Initialize the RandomForestRegressor model
model = RandomForestRegressor()
model.fit(X, y)

# Predict delay for future appointments
def predict_wait_time(doctor_id, scheduled_time):
    """
    Predict the expected delay for a given doctor and scheduled appointment time.
    """
    hour = scheduled_time.hour
    day_of_week = scheduled_time.weekday()
    
    # Make the prediction
    predicted_delay = model.predict([[doctor_id, hour, day_of_week]])[0]
    
    return predicted_delay

# Dynamic Slot Allocation Function
def allocate_slot(doctor_id, scheduled_time, predicted_delay):
    """
    Adjust the appointment time by considering predicted delay.
    """
    adjusted_time = scheduled_time + timedelta(minutes=predicted_delay)
    return adjusted_time

# Handling Early Arrivals
def handle_early_arrival(scheduled_time, arrival_time, predicted_delay):
    """
    Handle early arrivals by adjusting the patient's expected start time.
    If the patient arrives early and a slot is available, they can be seen sooner.
    """
    # Check if the patient arrives early (e.g., 20 minutes before the scheduled time)
    early_arrival_threshold = timedelta(minutes=20)
    if arrival_time < scheduled_time - early_arrival_threshold:
        # If there's a predicted delay, see if the patient can be moved up
        return allocate_slot(doctor_id=1, scheduled_time=scheduled_time, predicted_delay=-predicted_delay)  # Adjust early
    else:
        # Return the original scheduled time
        return scheduled_time

# Example usage
scheduled_time = datetime(2024, 3, 26, 18, 30)  # Example scheduled time
arrival_time = datetime(2024, 3, 26, 18, 0)  # Example early arrival time (20 minutes before scheduled time)

# Predict the delay for a particular doctor and time
predicted_delay = predict_wait_time(doctor_id=5, scheduled_time=scheduled_time)
print(f"Predicted delay for Dr. 5 at {scheduled_time}: {predicted_delay:.2f} minutes")

# Allocate a new slot based on the predicted delay
adjusted_time = allocate_slot(doctor_id=5, scheduled_time=scheduled_time, predicted_delay=predicted_delay)
print(f"Original time: {scheduled_time}, Adjusted time: {adjusted_time}")

# Handle early arrival and adjust time if necessary
adjusted_early_arrival_time = handle_early_arrival(scheduled_time, arrival_time, predicted_delay)
print(f"Original time: {scheduled_time}, Early arrival adjusted time: {adjusted_early_arrival_time}")
