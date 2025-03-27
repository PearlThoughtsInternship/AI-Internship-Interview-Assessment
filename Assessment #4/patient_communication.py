import random
import time
from googletrans import Translator
from gtts import gTTS
import os
import sys

# Ensure UTF-8 encoding for compatibility
sys.stdout.reconfigure(encoding='utf-8')

# Sample patient database with language and preferred communication channel
patients = [
    {"id": 1, "name": "Ravi Kumar", "language": "Tamil", "channel": "SMS"},
    {"id": 2, "name": "Ananya Rao", "language": "Telugu", "channel": "WhatsApp"},
    {"id": 3, "name": "Joseph Mathew", "language": "Malayalam", "channel": "IVR"},
    {"id": 4, "name": "Rahul Sharma", "language": "Hindi", "channel": "SMS"},
    {"id": 5, "name": "David Thomas", "language": "English", "channel": "WhatsApp"},
]

# Default message in English
default_message = "Your appointment is confirmed. Please visit!"

# AI-based translator
translator = Translator()

def translate_message(language, message):
    """Translate the message into the patient's preferred language."""
    if language.lower() == "english":
        return message  # No translation needed
    try:
        translated_text = translator.translate(message, dest=language.lower()).text
        return translated_text
    except Exception:
        return message  # Fallback to English if translation fails

def send_message(patient):
    """Simulate sending messages based on patient language and preferred channel."""
    language = patient["language"]
    channel = patient["channel"]
    translated_message = translate_message(language, default_message)

    if channel == "IVR":
        text_to_speech(translated_message, language)
    else:
        print(f"Sending via {channel} to {patient['name']} ({language}): {translated_message}")

def text_to_speech(message, language):
    """Convert text message to speech for IVR calls."""
    print(f"IVR Call initiated for {language} speaker: {message}")
    tts = gTTS(text=message, lang="ta" if language.lower() == "tamil" else "en")
    filename = f"ivr_{language}.mp3"
    tts.save(filename)
    os.system(f"start {filename}")  # Play the IVR message (Windows)

def measure_effectiveness():
    """Simulate confirmation tracking and A/B testing."""
    confirmed = sum(random.choices([0, 1], k=len(patients)))  # Simulated confirmations
    confirmation_rate = (confirmed / len(patients)) * 100
    print(f"Confirmation Rate: {confirmation_rate:.2f}%")

    # Simulating A/B testing
    channels = ["SMS", "WhatsApp", "IVR"]
    channel_success = {ch: random.randint(50, 90) for ch in channels}  # Random effectiveness scores
    best_channel = max(channel_success, key=channel_success.get)
    
    print("\nA/B Testing Results:")
    for ch, rate in channel_success.items():
        print(f"   - {ch}: {rate}% success rate")
    
    print(f"Best performing channel: {best_channel}")

def collect_feedback():
    """Simulate patient satisfaction surveys."""
    feedback = random.choices(["Excellent", "Good", "Neutral", "Poor"], weights=[50, 30, 15, 5], k=len(patients))
    satisfaction_score = (feedback.count("Excellent") * 5 + feedback.count("Good") * 4 +
                          feedback.count("Neutral") * 3 + feedback.count("Poor") * 1) / len(patients)
    print(f"Patient Satisfaction Score: {satisfaction_score:.2f}/5")

# Run the system
print("Multi-Language Patient Communication System Running...\n")

# Simulating message sending
for patient in patients:
    send_message(patient)
    time.sleep(1)  # Simulate a delay

# Measure effectiveness
measure_effectiveness()

# Collect feedback
collect_feedback()
