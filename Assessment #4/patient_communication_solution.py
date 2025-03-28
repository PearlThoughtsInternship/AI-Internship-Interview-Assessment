import random
from gtts import gTTS
import os
import platform

# Enhanced patient database with age for better targeting
patients = [
    {"id": 1, "name": "Ravi Kumar", "language": "Tamil", "channel": "SMS", "age": 65},
    {"id": 2, "name": "Ananya Rao", "language": "Telugu", "channel": "WhatsApp", "age": 30},
    {"id": 3, "name": "Joseph Mathew", "language": "Malayalam", "channel": "IVR", "age": 70},
    {"id": 4, "name": "Rahul Sharma", "language": "Hindi", "channel": "SMS", "age": 45},
    {"id": 5, "name": "David Thomas", "language": "English", "channel": "WhatsApp", "age": 35},
]

# Predefined multi-language messages with IVR support for elderly patients
messages = {
    "Tamil": {"standard": "உங்கள் நேரம் உறுதிசெய்யப்பட்டது. தயவுசெய்து வருக!",
              "elderly": "உங்கள் நேரம் உறுதிசெய்யப்பட்டது.",
              "ivr": "உங்கள் அப்பாயின்ட்மென்ட் உறுதியாக உள்ளது. தயவுசெய்து வருக."},
    "Telugu": {"standard": "మీ నియామకం నిర్ధారించబడింది. దయచేసి రండి!", "elderly": "మీ నియామకం నిర్ధారించబడింది.",
               "ivr": "మీ అపాయింట్‌మెంట్ కన్ఫర్మ్ చేయబడింది. దయచేసి హాజరుకండి."},
    "Malayalam": {"standard": "നിങ്ങളുടെ അപോയിന്റ്മെന്റ് സ്ഥിരീകരിച്ചിരിക്കുന്നു. ദയവായി വരൂ!",
                  "elderly": "നിങ്ങളുടെ അപോയിന്റ്മെന്റ് സ്ഥിരീകരിച്ചു.",
                  "ivr": "നിങ്ങളുടെ അപോയിന്റ്മെന്റ് സ്ഥിരീകരിച്ചിരിക്കുന്നു. ദയവായി എത്തുക."},
    "Hindi": {"standard": "आपका अपॉइंटमेंट कन्फर्म हो गया है। कृपया आएं!", "elderly": "अपॉइंटमेंट कन्फर्म हो गया।",
              "ivr": "आपका अपॉइंटमेंट पक्का हो गया है। कृपया समय पर आएं।"},
    "English": {"standard": "Your appointment is confirmed. Please visit!", "elderly": "Your appointment is confirmed.",
                "ivr": "Your appointment is confirmed. Please arrive on time."}
}


# Function to play audio messages
def play_audio(file):
    system_name = platform.system()
    if system_name == "Windows":
        os.system(f"start {file}")
    elif system_name == "Darwin":  # macOS
        os.system(f"afplay {file}")
    elif system_name == "Linux":
        os.system(f"mpg123 {file}")
    else:
        print(f"⚠️ Cannot play audio on {system_name}")


# Function to send messages based on patient preferences
def send_message(patient):
    """Simulate sending a message based on patient language, channel, and age."""
    language = patient["language"]
    age = patient["age"]
    channel = patient["channel"]

    # Choose message type based on channel
    if channel == "IVR":
        message_type = "ivr"
    else:
        message_type = "elderly" if age > 60 else "standard"

    message = messages.get(language, messages["English"])[message_type]

    print(f"📩 Sending via {channel} to {patient['name']} ({language}, Age {age}): {message}")

    # If channel is IVR, convert text to speech and simulate a voice call
    if channel == "IVR":
        tts = gTTS(text=message,
                   lang="ta" if language == "Tamil" else "te" if language == "Telugu" else "ml" if language == "Malayalam" else "hi" if language == "Hindi" else "en")
        audio_file = f"ivr_message_{patient['id']}.mp3"
        tts.save(audio_file)
        print(f"🔊 Playing IVR message for {patient['name']}... (Saved as {audio_file})")
        play_audio(audio_file)


# Send messages to all patients
for patient in patients:
    send_message(patient)


# Effectiveness measurement
def measure_effectiveness(before_rate=35):
    """Simulates confirmation tracking and A/B testing."""
    confirmed = sum(random.choices([0, 1], k=len(patients)))  # Random confirmations
    confirmation_rate = (confirmed / len(patients)) * 100
    improvement = confirmation_rate - before_rate

    print(f"\n✅ Confirmation Rate (After Multi-Language Support): {confirmation_rate:.2f}%")
    print(f"📊 Improvement: {improvement:.2f}% compared to previous 35% rate")

    # A/B Testing result simulation
    group_a = sum(random.choices([0, 1], k=len(patients) // 2))  # Control group
    group_b = sum(random.choices([0, 1], k=len(patients) // 2))  # New system group
    print(f"📈 A/B Test - Control Group Confirmation Rate: {group_a / (len(patients) // 2) * 100:.2f}%")
    print(f"📈 A/B Test - New System Confirmation Rate: {group_b / (len(patients) // 2) * 100:.2f}%")


# Patient Satisfaction Survey Simulation
def collect_feedback():
    """Simulates patient feedback on language clarity and ease of use."""
    feedback_scores = [random.randint(1, 5) for _ in range(len(patients))]  # Scores from 1 (bad) to 5 (excellent)
    avg_score = sum(feedback_scores) / len(feedback_scores)
    print(f"📝 Patient Satisfaction Survey - Average Score: {avg_score:.2f}/5")


measure_effectiveness()
collect_feedback()
