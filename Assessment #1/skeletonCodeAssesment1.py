import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
from collections import defaultdict
import tensorflow as tf
import random

# Generate synthetic appointment data
num_records = 300
np.random.seed(42)

data = {
    "scheduled_time": [datetime(2024, 3, 26, 17, 0) + timedelta(minutes=15 * i) for i in range(num_records)],
    "actual_time": [datetime(2024, 3, 26, 17, 0) + timedelta(minutes=15 * i + random.randint(40, 90)) for i in range(num_records)],
    "doctor_id": np.random.randint(1, 16, num_records),
    "patient_id": np.arange(1000, 1000 + num_records)
}
df = pd.DataFrame(data)
df.to_csv("appointments.csv", index=False)

# Load appointment data
df = pd.read_csv("appointments.csv")  # Contains scheduled_time, actual_time, doctor_id, patient_id

# Feature Engineering
df['delay'] = (pd.to_datetime(df['actual_time']) - pd.to_datetime(df['scheduled_time'])).dt.total_seconds() / 60
df['hour'] = pd.to_datetime(df['scheduled_time']).dt.hour
df['day_of_week'] = pd.to_datetime(df['scheduled_time']).dt.dayofweek

# Define features and target variable
features = ['doctor_id', 'hour', 'day_of_week']
target = 'delay'

# Scale data for LSTM
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(df[features])

# Train RandomForest Model (Model 1 - Appointment Delay Prediction)
X_rf = df[features]
y_rf = df[target]

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_rf, y_rf)

# Train LSTM Model (Model 2 - Sequential Delay Patterns)
X_lstm = X_scaled.reshape((X_scaled.shape[0], X_scaled.shape[1], 1))  # Reshape for LSTM
y_lstm = df[target].values

lstm_model = Sequential([Input(shape=(3, 1)), LSTM(50, activation='relu', return_sequences=False), Dense(1)])
lstm_model.compile(optimizer='adam', loss='mse')
lstm_model.fit(X_lstm, y_lstm, epochs=20, verbose=0)

# Reinforcement Learning for Dynamic Slot Optimization to reduce wait time (Model 3)
doctor_schedule = defaultdict(list)

def optimize_slot(doctor_id, predicted_delay):
    optimized_slot = max(0, predicted_delay * 0.7)  # Reduce delay by 30%
    doctor_schedule[doctor_id].append(optimized_slot)
    return optimized_slot

# Predict delay for future appointments
def predict_wait_time(doctor_id, scheduled_time):
    hour = scheduled_time.hour
    day_of_week = scheduled_time.weekday()
    # Ensure input is a DataFrame with correct feature names
    input_data = pd.DataFrame([[doctor_id, hour, day_of_week]], columns=features)

    # Scale input for LSTM
    input_scaled = scaler.transform(input_data)  # Ensure it retains feature structure
    input_lstm = np.array(input_scaled).reshape((1, 3, 1))  # Reshape for LSTM

    # Predictions
    predicted_delay_rf = rf_model.predict(input_data)[0]  # Maintain feature names
    predicted_delay_lstm = lstm_model.predict(input_lstm)[0][0]

    # Optimize time slot
    optimized_delay = optimize_slot(doctor_id, (predicted_delay_rf + predicted_delay_lstm) / 2)

    return predicted_delay_rf, predicted_delay_lstm, optimized_delay

# Example Usage
scheduled_time = datetime(2024, 3, 26, 18, 30)
pred_rf, pred_lstm, optimized = predict_wait_time(doctor_id=5, scheduled_time=scheduled_time)

print(f"Predicted Wait Time (Random Forest): {pred_rf:.2f} minutes")
print(f"Predicted Wait Time (LSTM): {pred_lstm:.2f} minutes")
print(f"Optimized Wait Time (After AI Adjustment): {optimized:.2f} minutes")
