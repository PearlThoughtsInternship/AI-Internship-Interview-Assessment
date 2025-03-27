import random
from googletrans import Translator  # Import translation library

# Function to translate messages based on patient language preference
def translate_message(message, lang):
    translator = Translator()
    return translator.translate(message, dest=lang).text

# Function to send SMS notifications
def send_sms(patient, message):
    translated_msg = translate_message(message, patient['language'])
    print(f"SMS sent to {patient['name']} ({patient['language']}): {translated_msg}")

# Function to send WhatsApp messages
def send_whatsapp(patient, message):
    translated_msg = translate_message(message, patient['language'])
    print(f"WhatsApp message sent to {patient['name']} ({patient['language']}): {translated_msg}")

# Function to make IVR calls
def send_ivr(patient, message):
    translated_msg = translate_message(message, patient['language'])
    print(f"IVR Call made to {patient['name']} ({patient['language']}): {translated_msg}")

# Function to decide which communication channel to use
def choose_channel(patient):
    if patient['age'] > 60:
        return "IVR"  # Elderly patients prefer voice calls
    elif patient['prefers_whatsapp']:
        return "WhatsApp"  # Younger patients prefer WhatsApp
    else:
        return "SMS"  # Default option

# Function to send appointment reminders based on preferred channel
def send_appointment_reminder(patient):
    message = "Reminder: You have an appointment tomorrow at Apollo Clinic."
    channel = choose_channel(patient)
    
    if channel == "SMS":
        send_sms(patient, message)
    elif channel == "WhatsApp":
        send_whatsapp(patient, message)
    else:
        send_ivr(patient, message)

# Simulating patient confirmation responses
def track_confirmation():
    return random.choice([True, False])  # Randomly simulate patient response

# Function to measure system effectiveness
def measure_effectiveness(patients):
    confirmations = sum(track_confirmation() for _ in patients)
    total_patients = len(patients)
    confirmation_rate = (confirmations / total_patients) * 100
    print(f"Confirmation Rate: {confirmation_rate:.2f}%")
    return confirmation_rate

# Example Patient Data
patients = [
    {"name": "Arun", "age": 65, "language": "ta", "prefers_whatsapp": False},
    {"name": "Suresh", "age": 32, "language": "te", "prefers_whatsapp": True},
    {"name": "Deepa", "age": 48, "language": "ml", "prefers_whatsapp": False},
    {"name": "Priya", "age": 39, "language": "hi", "prefers_whatsapp": True},
    {"name": "Karthik", "age": 56, "language": "en", "prefers_whatsapp": False},
    {"name": "Meena", "age": 29, "language": "ta", "prefers_whatsapp": True},
    {"name": "Vikram", "age": 45, "language": "te", "prefers_whatsapp": False},
    {"name": "Ananya", "age": 50, "language": "ml", "prefers_whatsapp": True},
    {"name": "Rahul", "age": 41, "language": "hi", "prefers_whatsapp": False},
    {"name": "Elizabeth", "age": 58, "language": "en", "prefers_whatsapp": True},
]

# Sending appointment reminders to all patients
for patient in patients:
    send_appointment_reminder(patient)

# Measuring and displaying confirmation rate
measure_effectiveness(patients)
