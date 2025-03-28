import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta
import os

# Ensure file exists
file_path = "appointments.csv"
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File '{file_path}' not found. Ensure the dataset exists.")

# Load appointment data
df = pd.read_csv(file_path)

# Ensure required columns exist
required_columns = {"scheduled_time", "actual_time", "doctor_id"}
if not required_columns.issubset(df.columns):
    raise ValueError(f"Missing required columns. Ensure {required_columns} exist in the dataset.")

# Convert times to datetime format
df['scheduled_time'] = pd.to_datetime(df['scheduled_time'], errors='coerce')
df['actual_time'] = pd.to_datetime(df['actual_time'], errors='coerce')

# Drop rows with missing values in critical columns
df = df.dropna(subset=['scheduled_time', 'actual_time', 'doctor_id'])

# Compute delay in minutes
df['delay'] = (df['actual_time'] - df['scheduled_time']).dt.total_seconds() / 60

# Feature Engineering
df['hour'] = df['scheduled_time'].dt.hour
df['day_of_week'] = df['scheduled_time'].dt.dayofweek

# Ensure target variable has no NaNs
df = df.dropna(subset=['delay'])

# Define features and target variable
features = ['doctor_id', 'hour', 'day_of_week']
target = 'delay'

X = df[features]
y = df[target]

# Train AI Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Predict delay for future appointments
def predict_wait_time(doctor_id, scheduled_time):
    hour = scheduled_time.hour
    day_of_week = scheduled_time.weekday()
    prediction = model.predict(np.array([[doctor_id, hour, day_of_week]]))  # Ensure input is a NumPy array
    return prediction[0]  # Predicted delay in minutes

# Example usage
predicted_delay = predict_wait_time(doctor_id=5, scheduled_time=datetime(2024, 3, 26, 18, 30))
print(f"Expected wait time: {predicted_delay:.2f} minutes")

predicted_delay = predict_wait_time(doctor_id=5, scheduled_time=datetime(2024, 3, 26, 18, 30))
print(f"Expected wait time: {predicted_delay:.2f} minutes")
