import random
import matplotlib.pyplot as plt

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

# Probabilities for confirmation based on language
confirmation_probabilities = {
    "Tamil": 0.4,
    "Telugu": 0.2,
    "Malayalam": 0.1,
    "Hindi": 0.2,
    "English": 0.1
}

def send_message(patient):
    """Simulate sending a message based on patient language and preferred channel"""
    language = patient["language"]
    message = messages.get(language, messages["English"])  # Default to English if language not found
    channel = patient["channel"]
    print(f"📩 Sending via {channel} to {patient['name']} ({language}): {message}")

# Simulating message sending to all patients
for patient in patients:
    send_message(patient)

# Effectiveness simulation: track confirmations
def measure_effectiveness():
    """Simulates confirmation tracking based on language probability and visualizes it"""
    confirmations = [
        1 if random.random() < confirmation_probabilities[patient["language"]] else 0
        for patient in patients
    ]

    confirmed_count = sum(confirmations)
    confirmation_rate = (confirmed_count / len(patients)) * 100

    print(f"✅ Confirmation Rate: {confirmation_rate:.2f}%")

    # Visualization
    names = [p["name"] for p in patients]
    colors = ['green' if c else 'red' for c in confirmations]

    plt.bar(names, confirmations, color=colors)
    plt.xlabel("Patients")
    plt.ylabel("Confirmation (1 = Yes, 0 = No)")
    plt.title("Appointment Confirmations Based on Language Preference")
    plt.ylim(0, 1)
    plt.show()

measure_effectiveness()
