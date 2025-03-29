import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Load data
df = pd.read_csv("appointments.csv")

# Convert time columns to datetime format
df['scheduled_time'] = pd.to_datetime(df['scheduled_time'])
df['actual_time'] = pd.to_datetime(df['actual_time'])

# Feature Engineering
df['delay_minutes'] = (df['actual_time'] - df['scheduled_time']).dt.total_seconds() / 60  # Delay in minutes
df['hour_of_day'] = df['scheduled_time'].dt.hour  # Hour of the appointment
df['day_of_week'] = df['scheduled_time'].dt.dayofweek  # Day of the week (0=Monday, 6=Sunday)

# Select features and target
features = ['hour_of_day', 'day_of_week', 'doctor_id']
target = 'delay_minutes'

# Handle missing values
df = df.dropna()
X = df[features]
y = df[target]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate Model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae:.2f} minutes")

# Predict wait time for new appointment
new_appointment = pd.DataFrame({
    'hour_of_day': [18],  # Example: 6 PM appointment
    'day_of_week': [4],  # Example: Friday
    'doctor_id': [2]  # Example: Doctor 2
})

predicted_wait_time = model.predict(new_appointment)[0]
print(f"Expected wait time: {predicted_wait_time:.2f} minutes")