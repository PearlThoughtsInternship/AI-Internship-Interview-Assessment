import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import TimeSeriesSplit, train_test_split
from datetime import datetime, timedelta
import json
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load appointment data with fallback
try:
    df = pd.read_csv("appointments.csv")
except FileNotFoundError:
    # Generate sample data if file not found
    print("No appointments.csv found - generating sample data")
    date_range = pd.date_range(start='2024-01-01', end='2024-03-31', freq='15min')
    sample_data = {
        'scheduled_time': date_range,
        'actual_time': date_range + pd.to_timedelta(np.random.randint(0, 45, len(date_range)), unit='min'),
        'doctor_id': np.random.randint(1, 16, len(date_range)),
        'patient_id': np.random.randint(1000, 9999, len(date_range))
    }
    df = pd.DataFrame(sample_data)
    df['delay'] = (pd.to_datetime(df['actual_time']) - pd.to_datetime(df['scheduled_time'])).dt.total_seconds() / 60
    df['consultation_duration'] = df.groupby('doctor_id')['delay'].transform('mean')
    df['patients_in_queue'] = df.groupby(['doctor_id', pd.Grouper(key='scheduled_time', freq='h')]).cumcount()
    df.to_csv("appointments.csv", index=False)

# Feature Engineering
df['delay'] = (pd.to_datetime(df['actual_time']) - pd.to_datetime(df['scheduled_time'])).dt.total_seconds() / 60
df['hour'] = pd.to_datetime(df['scheduled_time']).dt.hour
df['day_of_week'] = pd.to_datetime(df['scheduled_time']).dt.dayofweek

# Enhanced Feature Engineering
df = df.sort_values('scheduled_time')
df['consultation_duration'] = df.groupby('doctor_id')['delay'].transform('mean')  # Doctor-specific patterns
df['patients_in_queue'] = df.groupby(['doctor_id', pd.Grouper(key='scheduled_time', freq='h')]).cumcount()

# Updated features including congestion metrics
features = ['doctor_id', 'hour', 'day_of_week', 'consultation_duration', 'patients_in_queue']
target = 'delay'

# Time-aware cross-validation
tscv = TimeSeriesSplit(n_splits=5)
model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)  # Handles temporal effects better

# Real-time update mechanism
class ClinicScheduler:
    def __init__(self, model):
        self.model = model
        self.real_time_data = pd.DataFrame(columns=features + [target])
    
    def update_with_live_data(self, new_data):
        """Update model with real-time appointments"""
        self.real_time_data = pd.concat([self.real_time_data, new_data])
        self.model.partial_fit(new_data[features], new_data[target])

# Dynamic slot allocation        
def suggest_optimal_doctor(scheduled_time):
    """Predicts best doctor based on current load"""
    hour = scheduled_time.hour
    day_of_week = scheduled_time.weekday()
    predictions = []
    
    for doctor_id in range(1, 16):  # 15 specialists
        current_load = df[df['doctor_id'] == doctor_id].tail(10)  # Last 10 appointments
        consultation_duration = current_load['delay'].mean()
        patients_in_queue = len(current_load)
        
        predictions.append(
            model.predict([[doctor_id, hour, day_of_week, consultation_duration, patients_in_queue]])[0]
        )
    
    return np.argmin(predictions) + 1  # Return doctor ID with shortest predicted wait

# SMS integration placeholder
def send_sms_update(patient_id, estimated_wait):
    """Integrate with SMS API"""
    message = f"Estimated wait: {estimated_wait:.0f} mins. Text 'R' to reschedule."
    # Implementation would connect to SMS gateway
    return True

# Continuous learning implementation
def update_model_with_new_data(new_appointments):
    """Daily model update with new data"""
    global model
    new_data = process_new_appointments(new_appointments)  # Would include real arrival times
    model.fit(X.append(new_data[features]), y.append(new_data[target]))

# Train AI Model
X = df[features]
y = df[target]

model.fit(X, y)

# Predict delay for future appointments
def predict_wait_time(doctor_id, scheduled_time, consultation_duration, patients_in_queue):
    hour = scheduled_time.hour
    day_of_week = scheduled_time.weekday()
    return model.predict([[doctor_id, hour, day_of_week, consultation_duration, patients_in_queue]])[0]

# Example usage
predicted_delay = predict_wait_time(
    doctor_id=5,
    scheduled_time=datetime(2024, 3, 26, 18, 30),
    consultation_duration=df[df['doctor_id'] == 5]['delay'].mean(),  # Get doctor's historical average
    patients_in_queue=df[(df['doctor_id'] == 5) & (df['scheduled_time'].dt.hour == 18)].shape[0]  # Current hour's queue
)
print(f"Expected wait time: {predicted_delay:.2f} minutes")

# Evaluation metrics
def evaluate_model():
    # Time-based split
    train, test = train_test_split(df, test_size=0.2, shuffle=False)
    model.fit(train[features], train[target])
    preds = model.predict(test[features])
    
    print(f"MAE: {mean_absolute_error(test[target], preds)}")
    print(f"RMSE: {mean_squared_error(test[target], preds)**0.5}")
    print(f"Peak Hour Improvement: {(preds[test['hour'].between(17,20)].mean() - test[target].mean()) / test[target].mean() * 100}%")
