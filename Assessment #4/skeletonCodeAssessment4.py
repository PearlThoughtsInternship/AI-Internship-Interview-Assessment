import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

class AIPatientCommunicationSystem:
    def __init__(self):
        # Enhanced patient database with comprehensive patient profiles
        self.patients = [
            {
                "id": 1, 
                "name": "Ravi Kumar", 
                "language": "Tamil", 
                "age": 68,  # Elderly patient
                "preferred_channels": ["IVR", "SMS"],
                "communication_preference": "simple",
                "past_interactions": {
                    "total_appointments": 5,
                    "missed_appointments": 2,
                    "communication_effectiveness": 0.6
                },
                "medical_conditions": ["Diabetes"],
                "preferred_contact_time": "morning"
            },
            {
                "id": 2, 
                "name": "Ananya Rao", 
                "language": "Telugu", 
                "age": 35,
                "preferred_channels": ["WhatsApp", "SMS"],
                "communication_preference": "detailed",
                "past_interactions": {
                    "total_appointments": 3,
                    "missed_appointments": 0,
                    "communication_effectiveness": 0.9
                },
                "medical_conditions": ["Hypertension"],
                "preferred_contact_time": "evening"
            },
            {
                "id": 3, 
                "name": "Joseph Mathew", 
                "language": "Malayalam", 
                "age": 72,  # Elderly patient
                "preferred_channels": ["IVR", "WhatsApp"],
                "communication_preference": "simple",
                "past_interactions": {
                    "total_appointments": 4,
                    "missed_appointments": 1,
                    "communication_effectiveness": 0.7
                },
                "medical_conditions": ["Heart Condition"],
                "preferred_contact_time": "afternoon"
            },
            {
                "id": 4, 
                "name": "Rahul Sharma", 
                "language": "Hindi", 
                "age": 45,
                "preferred_channels": ["SMS", "WhatsApp"],
                "communication_preference": "standard",
                "past_interactions": {
                    "total_appointments": 6,
                    "missed_appointments": 1,
                    "communication_effectiveness": 0.8
                },
                "medical_conditions": ["Arthritis"],
                "preferred_contact_time": "morning"
            },
            {
                "id": 5, 
                "name": "David Thomas", 
                "language": "English", 
                "age": 40,
                "preferred_channels": ["WhatsApp", "SMS"],
                "communication_preference": "detailed",
                "past_interactions": {
                    "total_appointments": 3,
                    "missed_appointments": 0,
                    "communication_effectiveness": 0.9
                },
                "medical_conditions": [],
                "preferred_contact_time": "evening"
            }
        ]

        # Comprehensive message templates with NLP-like adaptations
        self.message_templates = {
            "appointment_confirmation": {
                "Tamil": {
                    "simple": "உங்கள் நேரம் உறுதிசெய்யப்பட்டது. தயவுசெய்து வருக!",
                    "detailed": "உங்கள் மருத்துவ நேரம் {date} அன்று {time} மணிக்கு உறுதிசெய்யப்பட்டுள்ளது. தயவுசெய்து சரியான நேரத்தில் வாருங்கள்."
                },
                "Telugu": {
                    "simple": "మీ అపాయిన్మెంట్ నిర్ధారించబడింది.",
                    "detailed": "మీ వైద్య నేరం {date}న {time}కు నిర్ధారించబడింది. కచ్చితంగా సమయానికి రండి."
                },
                "Malayalam": {
                    "simple": "നിങ്ങളുടെ അപ്പോയിൻറ്മെന്റ് സ്ഥിരീകരിച്ചിരിക്കുന്നു.",
                    "detailed": "നിങ്ങളുടെ വൈദ്യ അപ്പോയിൻറ്മെന്റ് {date}ന് {time}ന് സ്ഥിരീകരിച്ചിരിക്കുന്നു. സമയനിഷ്ഠയോടെ വരൂ."
                },
                "Hindi": {
                    "simple": "आपका अपॉइंटमेंट कन्फर्म हो गया है।",
                    "detailed": "आपका चिकित्सा अपॉइंटमेंट {date} को {time} बजे निश्चित हुआ है। कृपया समय पर आएं।"
                },
                "English": {
                    "simple": "Your appointment is confirmed. Please visit!",
                    "detailed": "Your medical appointment is confirmed for {date} at {time}. Please arrive 15 minutes early."
                }
            }
        }

        # A/B Testing Framework
        self.ab_test_results = {
            "language_effectiveness": {},
            "channel_effectiveness": {},
            "message_complexity_impact": {}
        }

        # New NLP and Adaptive Formatting Module
        self.nlp_module = {
            "language_translations": {
                "Tamil": {
                    "hello": "வணக்கம்",
                    "appointment": "நேரம்",
                    "reminder": "நினைவூட்டல்"
                },
                "Telugu": {
                    "hello": "నమస్కారం",
                    "appointment": "నేరం",
                    "reminder": "రిమైండర్"
                },
                "Malayalam": {
                    "hello": "നമസ്കാരം",
                    "appointment": "അപ്പോയിൻറ്മെന്റ്",
                    "reminder": "ഓർമ്മപ്പെടുത്തൽ"
                },
                "Hindi": {
                    "hello": "नमस्ते",
                    "appointment": "अपॉइंटमेंट",
                    "reminder": "याद दिलाना"
                }
            },
            "text_simplification": {
                "complexity_map": {
                    "simple": {
                        "max_words": 10,
                        "sentence_structure": "short_and_clear"
                    },
                    "detailed": {
                        "max_words": 20,
                        "sentence_structure": "descriptive"
                    }
                }
            }
        }

        # Patient Satisfaction Survey Module
        self.satisfaction_surveys = {
            "survey_questions": [
                {
                    "id": "language_clarity",
                    "question": "How clear was the communication in your language?",
                    "type": "rating",
                    "scale": range(1, 6)  # 1-5 rating
                },
                {
                    "id": "message_ease",
                    "question": "How easy was it to understand the message?",
                    "type": "rating",
                    "scale": range(1, 6)
                },
                {
                    "id": "channel_preference",
                    "question": "Which communication channel do you prefer?",
                    "type": "multiple_choice",
                    "options": ["SMS", "WhatsApp", "IVR", "Email"]
                }
            ],
            "survey_results": []
        }

    def select_optimal_channel(self, patient: Dict[str, Any]) -> str:
        """
        Intelligent channel selection algorithm
        """
        # Prioritize channels based on age and past interactions
        if patient['age'] > 65:
            return 'IVR'
        
        # Default to first preferred channel
        return patient['preferred_channels'][0]

    def translate_text(self, text: str, language: str) -> str:
        """
        NLP-based text translation with fallback for English
        """
        # If language is English, return the original text
        if language == 'English':
            return text
        
        # Basic translation logic using predefined translations
        try:
            for key, translation in self.nlp_module['language_translations'][language].items():
                text = text.replace(key, translation)
            return text
        except KeyError:
            # Fallback to original text if language not found
            print(f"Warning: No translation found for language {language}")
            return text

    def generate_voice_message(self, text: str, language: str) -> str:
        """
        Simulate Voice AI conversion for IVR
        """
        # Simulate text-to-speech conversion with language-specific marker
        translated_text = self.translate_text(text, language)
        return f"[{language} Voice-TTS]: {translated_text}"

    def adaptive_text_formatting(self, text: str, patient: Dict[str, Any]) -> str:
        """
        Adaptive text formatting based on patient age and preferences
        """
        # Simplify text for elderly patients
        if patient['age'] > 65:
            # Reduce complexity for elderly patients
            words = text.split()
            simplified_text = ' '.join(words[:10])  # Limit to first 10 words
            
            # Add visual adaptations (larger font indicator)
            return f"🔊 [LARGE FONT] {simplified_text}"
        
        return text

    def generate_personalized_message(self, patient: Dict[str, Any], 
                                      message_type: str, 
                                      additional_info: Dict[str, str] = None) -> str:
        """
        AI-Enhanced Message Generation with NLP-like Adaptations
        """
        language = patient.get('language', 'English')
        age = patient.get('age', 40)
        
        # Select message complexity based on age and communication preference
        complexity = 'simple' if age > 65 else patient.get('communication_preference', 'standard')
        
        # Retrieve template
        template = self.message_templates.get(message_type, {}).get(language, {})
        
        # Handle nested complexity
        if isinstance(template, dict):
            template = template.get(complexity, list(template.values())[0])
        
        # Format message with additional info
        if additional_info:
            try:
                template = template.format(**additional_info)
            except KeyError:
                pass
        
        # Apply NLP and adaptive formatting
        translated_template = self.translate_text(template, language)
        adaptive_template = self.adaptive_text_formatting(translated_template, patient)
        
        # If using IVR for elderly patients, generate voice message
        if patient['age'] > 65 and 'IVR' in patient.get('preferred_channels', []):
            return self.generate_voice_message(adaptive_template, language)
        
        return adaptive_template

    def generate_satisfaction_survey(self, patient: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a personalized satisfaction survey for a patient
        """
        survey_response = {
            "patient_id": patient['id'],
            "patient_name": patient['name'],
            "language": patient['language'],
            "survey_date": datetime.now().strftime("%Y-%m-%d"),
            "responses": {}
        }

        # Simulate survey responses based on patient characteristics
        for question in self.satisfaction_surveys["survey_questions"]:
            if question['type'] == 'rating':
                # Use patient's communication effectiveness as a bias
                effectiveness = patient['past_interactions']['communication_effectiveness']
                base_rating = int(effectiveness * 5)  # Convert effectiveness to 1-5 scale
                
                # Add some randomness
                rating = max(1, min(5, base_rating + random.randint(-1, 1)))
                survey_response['responses'][question['id']] = rating
            
            elif question['type'] == 'multiple_choice':
                # Prefer the patient's first preferred channel
                survey_response['responses'][question['id']] = patient['preferred_channels'][0]

        return survey_response

    def analyze_satisfaction_surveys(self):
        """
        Analyze patient satisfaction survey results
        """
        # Simulate generating surveys for all patients
        for patient in self.patients:
            survey_response = self.generate_satisfaction_survey(patient)
            self.satisfaction_surveys['survey_results'].append(survey_response)

        # Analyze survey results
        survey_analysis = {
            "overall_language_clarity": {},
            "overall_message_ease": {},
            "channel_preferences": {},
            "language_satisfaction": {}
        }

        # Aggregate results
        for survey in self.satisfaction_surveys['survey_results']:
            language = survey['language']
            
            # Language Clarity Analysis
            if 'language_clarity' in survey['responses']:
                survey_analysis['overall_language_clarity'][language] = survey_analysis['overall_language_clarity'].get(language, []) + [survey['responses']['language_clarity']]
            
            # Message Ease Analysis
            if 'message_ease' in survey['responses']:
                survey_analysis['overall_message_ease'][language] = survey_analysis['overall_message_ease'].get(language, []) + [survey['responses']['message_ease']]
            
            # Channel Preferences
            if 'channel_preference' in survey['responses']:
                channel = survey['responses']['channel_preference']
                survey_analysis['channel_preferences'][channel] = survey_analysis['channel_preferences'].get(channel, 0) + 1

        # Calculate average ratings
        for language in survey_analysis['overall_language_clarity']:
            ratings = survey_analysis['overall_language_clarity'][language]
            survey_analysis['overall_language_clarity'][language] = sum(ratings) / len(ratings)

        for language in survey_analysis['overall_message_ease']:
            ratings = survey_analysis['overall_message_ease'][language]
            survey_analysis['overall_message_ease'][language] = sum(ratings) / len(ratings)

        # Save analysis to file
        with open('patient_satisfaction_analysis.json', 'w') as f:
            json.dump(survey_analysis, f, indent=4)

        # Print analysis
        print("\n📊 Patient Satisfaction Survey Analysis:")
        print("Language Clarity Ratings:", survey_analysis['overall_language_clarity'])
        print("Message Ease Ratings:", survey_analysis['overall_message_ease'])
        print("Channel Preferences:", survey_analysis['channel_preferences'])

        return survey_analysis

    def simulate_communication_effectiveness(self):
        """
        Comprehensive Effectiveness Measurement
        """
        results = {
            "total_patients": len(self.patients),
            "confirmed_patients": 0,
            "channel_performance": {},
            "language_performance": {},
            "age_group_performance": {
                "elderly": {"total": 0, "confirmed": 0},
                "adult": {"total": 0, "confirmed": 0}
            }
        }

        for patient in self.patients:
            # Select optimal communication channel
            channel = self.select_optimal_channel(patient)
            
            # Generate personalized message
            message = self.generate_personalized_message(
                patient, 
                'appointment_confirmation', 
                {
                    "date": datetime.now().strftime("%d-%m-%Y"),
                    "time": "10:00 AM"
                }
            )
            
            # Simulate patient confirmation
            confirmation_likelihood = patient['past_interactions']['communication_effectiveness']
            confirmed = random.random() < confirmation_likelihood
            
            # Update results
            if confirmed:
                results["confirmed_patients"] += 1
            
            # Track channel performance
            results["channel_performance"][channel] = results["channel_performance"].get(channel, 0) + (1 if confirmed else 0)
            
            # Track language performance
            results["language_performance"][patient['language']] = results["language_performance"].get(patient['language'], 0) + (1 if confirmed else 0)
            
            # Track age group performance
            age_group = "elderly" if patient['age'] > 65 else "adult"
            results["age_group_performance"][age_group]["total"] += 1
            if confirmed:
                results["age_group_performance"][age_group]["confirmed"] += 1
            
            # Print communication details
            print(f"📩 {patient['name']} ({patient['language']}) - {channel} Channel")
            print(f"   Message: {message}")
            print(f"   Confirmation Status: {'Confirmed' if confirmed else 'Not Confirmed'}\n")
        
        # Calculate confirmation rates
        confirmation_rate = (results["confirmed_patients"] / results["total_patients"]) * 100
        print(f"✅ Overall Confirmation Rate: {confirmation_rate:.2f}%")
        
        # Print detailed performance metrics
        print("\n🔍 Performance Metrics:")
        print("Channel Performance:", results["channel_performance"])
        print("Language Performance:", results["language_performance"])
        print("Age Group Performance:", results["age_group_performance"])
        
        # Conduct satisfaction survey analysis
        satisfaction_results = self.analyze_satisfaction_surveys()
        
        # Combine results
        results['satisfaction_survey'] = satisfaction_results
        
        # Save results to a JSON file for further analysis
        with open('communication_effectiveness_report.json', 'w') as f:
            json.dump(results, f, indent=4)
        
        return results

# Run the communication system
communication_system = AIPatientCommunicationSystem()
communication_system.simulate_communication_effectiveness()