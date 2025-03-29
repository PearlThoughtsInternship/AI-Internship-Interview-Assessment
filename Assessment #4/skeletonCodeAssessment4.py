import random
from gtts import gTTS  # Google Text-to-Speech for IVR
import os

# Sample patient database with language and preferred communication channel
patients = [
    {"id": 1, "name": "Ravi Kumar", "language": "Tamil", "channel": "SMS"},
    {"id": 2, "name": "Ananya Rao", "language": "Telugu", "channel": "WhatsApp"},
    {"id": 3, "name": "Joseph Mathew", "language": "Malayalam", "channel": "IVR"},
    {"id": 4, "name": "Rahul Sharma", "language": "Hindi", "channel": "SMS"},
    {"id": 5, "name": "David Thomas", "language": "English", "channel": "WhatsApp"},
]

# Predefined multi-language messages
messages = {
    "Tamil": "உங்கள் நேரம் உறுதிசெய்யப்பட்டது. தயவுசெய்து வருக!",
    "Telugu": "మీ నియామకం నిర్ధారించబడింది. దయచేసి రండి!",
    "Malayalam": "നിങ്ങളുടെ അപോയിന്റ്മെന്റ് സ്ഥിരീകരിച്ചിരിക്കുന്നു. ദയവായി വരൂ!",
    "Hindi": "आपका अपॉइंटमेंट कन्फर्म हो गया है। कृपया आएं!",
    "English": "Your appointment is confirmed. Please visit!"
}

def send_message(patient):
    """Simulate sending a message based on patient language and preferred channel"""
    language = patient["language"]
    message = messages.get(language, messages["English"])  # Default to English if language not found
    channel = patient["channel"]
    
    if channel == "IVR":
        generate_voice_message(message, patient)
    else:
        print(f"Sending via {channel} to {patient['name']} ({language}): {message}")

def generate_voice_message(message, patient):
    """Convert text message to speech for IVR"""
    tts = gTTS(text=message, lang='ta' if patient["language"] == "Tamil" else 'en')
    filename = f"ivr_message_{patient['id']}.mp3"
    tts.save(filename)
    print(f"📞 IVR call to {patient['name']} in {patient['language']} - Playing {filename}")

# Simulating message sending to all patients
for patient in patients:
    send_message(patient)

def measure_effectiveness():
    """Track confirmations and perform A/B testing"""
    confirmed = sum(random.choices([0, 1], k=len(patients)))  # Simulating confirmations
    confirmation_rate = (confirmed / len(patients)) * 100
    print(f"Confirmation Rate: {confirmation_rate:.2f}%")
    return confirmation_rate

# Measure effectiveness
measure_effectiveness()
