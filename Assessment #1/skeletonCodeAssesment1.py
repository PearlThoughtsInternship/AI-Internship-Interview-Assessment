import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

df = pd.read_csv("appointments.csv")  
df['scheduled_time'] = pd.to_datetime(df['scheduled_time'])
df['actual_time'] = pd.to_datetime(df['actual_time'])
df['delay'] = (df['actual_time'] - df['scheduled_time']).dt.total_seconds() / 60 
df['hour'] = df['scheduled_time'].dt.hour
df['day_of_week'] = df['scheduled_time'].dt.dayofweek

features = ['doctor_id', 'hour', 'day_of_week']
target = 'delay'

X = df[features]
y = df[target]

model = RandomForestRegressor()
model.fit(X, y)

def predict_wait_time(doctor_id, scheduled_time):
    """
    Predict the expected delay for a given doctor and scheduled appointment time.
    """
    hour = scheduled_time.hour
    day_of_week = scheduled_time.weekday()
    
    predicted_delay = model.predict([[doctor_id, hour, day_of_week]])[0]
    
    return predicted_delay

def allocate_slot(doctor_id, scheduled_time, predicted_delay):
    """
    Adjust the appointment time by considering predicted delay.
    """
    adjusted_time = scheduled_time + timedelta(minutes=predicted_delay)
    return adjusted_time

def handle_early_arrival(scheduled_time, arrival_time, predicted_delay):
    """
    Handle early arrivals by adjusting the patient's expected start time.
    If the patient arrives early and a slot is available, they can be seen sooner.
    """
    early_arrival_threshold = timedelta(minutes=20)
    if arrival_time < scheduled_time - early_arrival_threshold:
        return allocate_slot(doctor_id=1, scheduled_time=scheduled_time, predicted_delay=-predicted_delay)  
    else:
        return scheduled_time

scheduled_time = datetime(2024, 3, 26, 18, 30)  
arrival_time = datetime(2024, 3, 26, 18, 0)  


predicted_delay = predict_wait_time(doctor_id=5, scheduled_time=scheduled_time)
print(f"Predicted delay for Dr. 5 at {scheduled_time}: {predicted_delay:.2f} minutes")

adjusted_time = allocate_slot(doctor_id=5, scheduled_time=scheduled_time, predicted_delay=predicted_delay)
print(f"Original time: {scheduled_time}, Adjusted time: {adjusted_time}")

adjusted_early_arrival_time = handle_early_arrival(scheduled_time, arrival_time, predicted_delay)
print(f"Original time: {scheduled_time}, Early arrival adjusted time: {adjusted_early_arrival_time}")
