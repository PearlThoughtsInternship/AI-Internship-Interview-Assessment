import random

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
    "Tamil": ["உங்கள் நேரம் உறுதிசெய்யப்பட்டது.", "நீங்கள் வருமாறு!"],
    "Telugu": ["మీ అపాయింట్మెంట్ నిర్ధారించబడింది.", "దయచేసి రండి!"],
    "Malayalam": ["നിങ്ങളുടെ അപോയിന്റ്മെന്റ് സ്ഥിരീകരിച്ചു.", "ദയവായി വരൂ!"],
    "Hindi": ["आपका अपॉइंटमेंट कन्फर्म हो गया है।", "कृपया आएं!"],
    "English": ["Your appointment is confirmed.", "Please visit!"]
}

def send_message(patient, test_variant=0):
    """Simulate sending a message based on patient language, preferred channel, and A/B testing"""
    language = patient["language"]
    message_variants = messages.get(language, messages["English"])
    message = message_variants[test_variant]  # Use A/B testing variant

    channel = patient["channel"]
    
    if channel == "IVR":
        print(f"📞 Calling {patient['name']} ({language}): '{message}' [IVR]")
    else:
        print(f"📩 Sending via {channel} to {patient['name']} ({language}): '{message}'")

# Simulating A/B testing
print("\n--- Sending A/B Test Messages ---")
for patient in patients:
    variant = random.choice([0, 1])  # Randomly pick a test variant
    send_message(patient, variant)

# Effectiveness simulation: track confirmations by channel
def measure_effectiveness():
    """Simulates confirmation tracking for different channels"""
    confirmations = { "SMS": 0, "WhatsApp": 0, "IVR": 0 }
    total_per_channel = { "SMS": 0, "WhatsApp": 0, "IVR": 0 }

    for patient in patients:
        channel = patient["channel"]
        total_per_channel[channel] += 1
        confirmations[channel] += random.choice([0, 1])  # Random confirmation

    print("\n--- Effectiveness Report ---")
    for channel, total in total_per_channel.items():
        rate = (confirmations[channel] / total) * 100 if total else 0
        print(f"✅ {channel} Confirmation Rate: {rate:.2f}%")

measure_effectiveness()
