import random

patients = [
    {"id": 1, "name": "Ravi Kumar", "language": "Tamil", "channel": "SMS"},
    {"id": 2, "name": "Ananya Rao", "language": "Telugu", "channel": "WhatsApp"},
    {"id": 3, "name": "Joseph Mathew", "language": "Malayalam", "channel": "IVR"},
    {"id": 4, "name": "Rahul Sharma", "language": "Hindi", "channel": "SMS"},
    {"id": 5, "name": "David Thomas", "language": "English", "channel": "WhatsApp"},
]

messages = {
    "Tamil": "உங்கள் நேரம் உறுதிசெய்யப்பட்டது. தயவுசெய்து வருக!",
    "Telugu": "మీ నియామకం నిర్ధారించబడింది. దయచేసి రండి!",
    "Malayalam": "നിങ്ങളുടെ അപോയിന്റ്മെന്റ് സ്ഥിരീകരിച്ചിരിക്കുന്നു. ദയവായി വരൂ!",
    "Hindi": "आपका अपॉइंटमेंट कन्फर्म हो गया है। कृपया आएं!",
    "English": "Your appointment is confirmed. Please visit!"
}

personalized_messages = {
    "Tamil": "உங்கள் மருத்துவ appointment உறுதிசெய்யப்பட்டுள்ளது. தயவுசெய்து வருக!",
    "Telugu": "మీ ఆరోగ్య appointment నిర్ధారించబడింది. దయచేసి రాండి!",
    "Malayalam": "നിങ്ങളുടെ മെഡിക്കൽ appointment സ്ഥിരീകരിച്ചിട്ടുണ്ട്. ദയവായി വരൂ!",
    "Hindi": "आपका चिकित्सा appointment कन्फर्म हो गया है। कृपया आएं!",
    "English": "Your medical appointment is confirmed. Please visit!"
}

def send_message(patient):
    """Simulate sending a message based on patient language and preferred channel"""
    language = patient["language"]
    message = messages.get(language, messages["English"])  
    channel = patient["channel"]
    
    if language in personalized_messages:
        message = personalized_messages[language]
    
    if channel == "SMS":
        print(f"📩 Sending SMS to {patient['name']} ({language}): {message}")
    elif channel == "WhatsApp":
        print(f"📱 Sending WhatsApp message to {patient['name']} ({language}): {message}")
    elif channel == "IVR":
        print(f"📞 Sending IVR call to {patient['name']} ({language}): {message}")
    else:
        print(f"❗ Invalid channel for {patient['name']}")

for patient in patients:
    send_message(patient)

def measure_effectiveness():
    """Simulates confirmation tracking based on random chance and sends feedback requests"""
    confirmed = sum(random.choices([0, 1], k=len(patients)))  
    confirmation_rate = (confirmed / len(patients)) * 100
    print(f"✅ Confirmation Rate: {confirmation_rate:.2f}%")

    sms_patients = [patient for patient in patients if patient['channel'] == 'SMS']
    whatsapp_patients = [patient for patient in patients if patient['channel'] == 'WhatsApp']
    
    sms_confirmed = sum(random.choices([0, 1], k=len(sms_patients)))
    whatsapp_confirmed = sum(random.choices([0, 1], k=len(whatsapp_patients)))
    
    print(f"📊 SMS Confirmation Rate: {(sms_confirmed / len(sms_patients)) * 100:.2f}%")
    print(f"📊 WhatsApp Confirmation Rate: {(whatsapp_confirmed / len(whatsapp_patients)) * 100:.2f}%")

measure_effectiveness()
