# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 11:15:42 2025

@author: Shashank
"""

import json
import random
from googletrans import Translator

# Mock patient database with language preferences and preferred channels
patients = {
    "1001": {"name": "Rajesh", "language": "Tamil", "channel": "IVR"},
    "1002": {"name": "Anita", "language": "Hindi", "channel": "WhatsApp"},
    "1003": {"name": "Vikram", "language": "Telugu", "channel": "SMS"},
    "1004": {"name": "Joseph", "language": "Malayalam", "channel": "IVR"},
    "1005": {"name": "David", "language": "English", "channel": "WhatsApp"},
}

# Predefined multi-language messages
messages = {
    "Tamil": "உங்கள் நேரம் உறுதிசெய்யட்டு. தயவுசெய்து வருக!",
    "Telugu": "మీ నియామకం నిర్దారించబడింది. దయచేసి రాండి!",
    "Malayalam": "നിങ്ങളുടെ അപോയിണ്ട്മെന്റ് സന്ഥോഷിക്കരിച്ചുക്കയാണു. ദയാവായി വരു!",
    "Hindi": "आपका अपॉइंटमेंट कन्फर्म हो गया है। कृपया आएं!",
    "English": "Your appointment is confirmed. Please visit!"
}

translator = Translator()

def send_message(patient):
    """Simulate sending a message based on patient language and preferred channel"""
    language = patient["language"]
    message = messages.get(language, messages["English"])  # Default to English if language not found
    channel = patient["channel"]
    print(f"📩 Sending via {channel} to {patient['name']} ({language}): {message}")

# Simulating message sending to all patients
for patient in patients.values():
    send_message(patient)

# Effectiveness simulation: track confirmations
def measure_effectiveness():
    """Simulates confirmation tracking"""
    confirmed = sum(random.choices([0, 1], k=len(patients)))  # Random confirmations
    confirmation_rate = (confirmed / len(patients)) * 100
    print(f"✅ Confirmation Rate: {confirmation_rate:.2f}%")

measure_effectiveness()
