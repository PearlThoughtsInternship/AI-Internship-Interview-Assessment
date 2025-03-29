import pandas as pd
import numpy as np
import xgboost as xgb
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Load appointment data
df = pd.read_csv("appointments.csv")  # Ensure this file contains scheduled_time, actual_time, doctor_id, patient_id

# Feature Engineering
df['scheduled_time'] = pd.to_datetime(df['scheduled_time'])
df['actual_time'] = pd.to_datetime(df['actual_time'])
df['delay'] = (df['actual_time'] - df['scheduled_time']).dt.total_seconds() / 60

df['hour'] = df['scheduled_time'].dt.hour
df['day_of_week'] = df['scheduled_time'].dt.dayofweek

df = df.dropna()  # Remove missing values if any

# Define features and target variable
features = ['doctor_id', 'hour', 'day_of_week']
target = 'delay'

X = df[features]
y = df[target]

# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train XGBoost Model
model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1, max_depth=5)
model.fit(X_train, y_train)

# Evaluate Model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae:.2f} minutes")

# Predict delay for future appointments
def predict_wait_time(doctor_id, scheduled_time):
    scheduled_time = datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M:%S")
    hour = scheduled_time.hour
    day_of_week = scheduled_time.weekday()
    return model.predict(np.array([[doctor_id, hour, day_of_week]]))[0]  # Predicted delay in minutes

# Example usage
predicted_delay = predict_wait_time(doctor_id=5, scheduled_time="2024-03-26 18:30:00")
print(f"Expected wait time: {predicted_delay:.2f} minutes")
