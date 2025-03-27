import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
from datetime import datetime, timedelta
import random

# --- 1. Data Simulation (Replace with actual data) ---
def simulate_data(num_records=1000):
    data = []
    for _ in range(num_records):
        doctor_id = random.randint(1, 15)
        scheduled_time = datetime(2023, 1, 1, 17, 0) + timedelta(minutes=random.randint(0, 180)) # 5pm-8pm window
        actual_time = scheduled_time + timedelta(minutes=random.randint(-30, 90)) # Actual time can be early or late
        consultation_duration = random.randint(8, 22)
        data.append([doctor_id, scheduled_time, actual_time, consultation_duration])
    return pd.DataFrame(data, columns=['doctor_id', 'scheduled_time', 'actual_time', 'consultation_duration'])

df = simulate_data()
df['delay'] = (df['actual_time'] - df['scheduled_time']).dt.total_seconds() / 60.0

# --- 2. Feature Engineering ---
df['scheduled_hour'] = df['scheduled_time'].dt.hour
df['scheduled_minute'] = df['scheduled_time'].dt.minute
df['scheduled_time_minutes'] = df['scheduled_hour'] * 60 + df['scheduled_minute']

# --- 3. Predictive Model (Random Forest for Delay Prediction) ---
features = ['doctor_id', 'scheduled_time_minutes', 'consultation_duration']
target = 'delay'

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae}")

# --- 4. LSTM for Patient Arrival Forecasting (Simplified) ---
arrival_data = df['scheduled_time'].dt.hour.value_counts().sort_index().values.reshape(-1, 1)

def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - time_step - 1):
        a = dataset[i:(i + time_step), 0]
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])
    return np.array(dataX), np.array(dataY)

#time check
time_step = 1
X_arrival, y_arrival = create_dataset(arrival_data, time_step)
X_arrival = X_arrival.reshape(X_arrival.shape[0], X_arrival.shape[1], 1)

arrival_model = Sequential()
arrival_model.add(LSTM(50, return_sequences=True, input_shape=(X_arrival.shape[1], 1)))
arrival_model.add(LSTM(50, return_sequences=True))
arrival_model.add(LSTM(50))
arrival_model.add(Dense(1))
arrival_model.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=0.001))
arrival_model.fit(X_arrival, y_arrival, epochs=100, batch_size=1, verbose=0)

# --- 5. Dynamic Slot Allocation & Handling Early Arrivals ---
def optimize_schedule(scheduled_time, doctor_id, consultation_duration, current_time):
    features = pd.DataFrame([[doctor_id, (scheduled_time.hour * 60 + scheduled_time.minute), consultation_duration]], columns=['doctor_id', 'scheduled_time_minutes', 'consultation_duration'])
    predicted_delay = model.predict(features)[0]
    adjusted_time = scheduled_time + timedelta(minutes=predicted_delay)
    return adjusted_time

def handle_early_arrival(patient_arrival_time, scheduled_time, current_queue, doctor_id, consultation_duration, current_time):
    if patient_arrival_time < scheduled_time:
        adjusted_scheduled_time = optimize_schedule(scheduled_time, doctor_id, consultation_duration, current_time)
        if patient_arrival_time + timedelta(minutes=consultation_duration) < adjusted_scheduled_time:
            current_queue.insert(0, (patient_arrival_time, doctor_id, consultation_duration)) # High priority
            return "Early arrival accommodated."
        else:
            return "Early arrival, but wait time may be longer."
    return "Patient arrived on time or late"

# --- 6. Patient Communication (Example) ---
def send_sms_notification(patient_arrival_time, scheduled_time, doctor_id, consultation_duration, current_time):
    adjusted_time = optimize_schedule(scheduled_time, doctor_id, consultation_duration, current_time)
    wait_time = (adjusted_time - patient_arrival_time).total_seconds() / 60.0
    print(f"SMS: Estimated wait time: {wait_time:.0f} minutes.")

# --- User Input & Example Usage ---

def get_user_input():
    arrival_hour = int(input("Enter patient arrival hour (24-hour format): "))
    arrival_minute = int(input("Enter patient arrival minute: "))
    scheduled_hour = int(input("Enter scheduled appointment hour (24-hour format): "))
    scheduled_minute = int(input("Enter scheduled appointment minute: "))
    doctor_id = int(input("Enter doctor ID (1-15): "))
    consultation_duration = int(input("Enter consultation duration (minutes): "))

    patient_arrival_time = datetime(2023, 1, 1, arrival_hour, arrival_minute)
    scheduled_time = datetime(2023, 1, 1, scheduled_hour, scheduled_minute)
    current_time = datetime.now()
    return patient_arrival_time, scheduled_time, doctor_id, consultation_duration, current_time

patient_arrival_time, scheduled_time, doctor_id, consultation_duration, current_time = get_user_input()
current_queue = []

print(handle_early_arrival(patient_arrival_time, scheduled_time, current_queue, doctor_id, consultation_duration, current_time))
send_sms_notification(patient_arrival_time, scheduled_time, doctor_id, consultation_duration, current_time)