import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from solution import ChannelOptimizer, patients, message_templates, CommunicationManager

class TestMultiLanguageCommunication(unittest.TestCase):
    def setUp(self):
        self.channel_optimizer = ChannelOptimizer()
        self.test_patient = {
            "id": 1,
            "name": "Test Patient",
            "language": "Tamil",
            "age": 65,
            "channel": "SMS",
            "preferred_channels": ["SMS", "IVR", "WhatsApp"]
        }

    def test_message_template_completeness(self):
        """Verify all languages have complete message templates"""
        languages = {patient["language"] for patient in patients}
        message_types = message_templates.keys()
        
        for lang in languages:
            for msg_type in message_types:
                self.assertIn(lang, message_templates[msg_type],
                             f"Missing {lang} template for {msg_type}")
                self.assertIn("standard", message_templates[msg_type][lang],
                             f"Missing standard template for {lang} in {msg_type}")
                self.assertIn("elderly", message_templates[msg_type][lang],
                             f"Missing elderly template for {lang} in {msg_type}")

    def test_channel_optimization(self):
        """Test channel selection optimization based on patient demographics"""
        # Test elderly patient channel preference
        elderly_patient = self.test_patient.copy()
        elderly_patient["age"] = 75
        channel = self.channel_optimizer.get_optimal_channel(elderly_patient, "appointment_confirmation")
        self.assertEqual(channel, "IVR", "Elderly patients should prefer IVR")

        # Test younger patient channel preference
        young_patient = self.test_patient.copy()
        young_patient["age"] = 25
        channel = self.channel_optimizer.get_optimal_channel(young_patient, "appointment_confirmation")
        self.assertEqual(channel, "WhatsApp", "Younger patients should prefer WhatsApp")

    def test_message_effectiveness(self):
        """Test message effectiveness tracking and A/B testing"""
        # Simulate message success rates
        for _ in range(10):
            self.channel_optimizer.update_engagement_history(
                self.test_patient["id"],
                "SMS",
                "appointment_confirmation",
                True
            )

        success_rate = self.channel_optimizer.get_channel_success_rate(
            self.test_patient["id"],
            "SMS"
        )
        self.assertGreaterEqual(success_rate, 0.7,
                               "Message effectiveness below threshold")

    @patch('solution.datetime')
    def test_wait_time_reduction(self, mock_datetime):
        """Test wait time communication optimization"""
        mock_datetime.now.return_value = datetime(2024, 3, 26, 10, 0)
        
        # Test wait time message generation
        wait_time = 30
        message = message_templates["wait_time"]["Tamil"]["elderly"].format(
            wait_time=wait_time
        )
        self.assertIn(str(wait_time), message,
                      "Wait time not properly formatted in message")

    def test_language_fallback(self):
        """Test fallback to English for unsupported languages"""
        unsupported_lang_patient = self.test_patient.copy()
        unsupported_lang_patient["language"] = "French"
        
        # Should fall back to English templates
        channel = self.channel_optimizer.get_optimal_channel(
            unsupported_lang_patient,
            "appointment_confirmation"
        )
        self.assertIsNotNone(channel, "Channel selection failed for unsupported language")

    def test_message_personalization(self):
        """Test message personalization based on patient profile"""
        # Test elderly patient message format
        elderly_patient = self.test_patient.copy()
        elderly_patient['age'] = 75
        
        # Initialize communication manager
        comm_manager = CommunicationManager()
        
        # Send test message
        result = comm_manager.send_message(
            elderly_patient,
            'appointment_confirmation',
            date='2024-03-27',
            time='10:00 AM'
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['channel'], 'IVR')
        self.assertIn('மருத்துவ சந்திப்பு', result['message'])

    def test_performance_monitoring(self):
        """Test performance monitoring system"""
        comm_manager = CommunicationManager()
        
        # Send multiple test messages
        for patient in patients[:3]:
            comm_manager.send_message(
                patient,
                'wait_time',
                wait_time=15
            )
        
        # Get performance metrics
        metrics = comm_manager.get_system_performance()
        
        self.assertIn('delivery_success_rate', metrics)
        self.assertIn('patient_response_rate', metrics)
        self.assertIn('channel_usage', metrics)
        self.assertIn('language_usage', metrics)

    def test_sentiment_analysis(self):
        """Test sentiment analysis functionality"""
        comm_manager = CommunicationManager()
        
        # Test positive response
        response_data = comm_manager.process_response(
            self.test_patient['id'],
            'Yes, thank you for the reminder',
            datetime.now()
        )
        self.assertGreater(response_data['sentiment_score'], 0)
        
        # Test negative response
        response_data = comm_manager.process_response(
            self.test_patient['id'],
            'No, I cannot make it',
            datetime.now()
        )
        self.assertLess(response_data['sentiment_score'], 0)

if __name__ == '__main__':
    unittest.main()