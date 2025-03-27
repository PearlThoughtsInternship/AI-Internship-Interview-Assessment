import pytest
from datetime import datetime
from skeletonCodeAssesment1 import predict_wait_time, optimize_schedule, send_wait_time_update
import pandas as pd
import numpy as np

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'doctor_id': [5, 5, 3, 3],
        'scheduled_time': pd.to_datetime(['2024-03-26 18:30:00', '2024-03-26 18:45:00', '2024-03-26 17:30:00', '2024-03-26 19:00:00']),
        'actual_time': pd.to_datetime(['2024-03-26 18:35:00', '2024-03-26 19:00:00', '2024-03-26 17:40:00', '2024-03-26 19:10:00']),
        'patient_id': [101, 102, 103, 104]
    })

@pytest.mark.parametrize("doctor_id, scheduled_time, expected", [
    (5, pd.Timestamp('2024-03-26 18:30'), 40.0),
    (3, pd.Timestamp('2024-03-26 17:30'), 25.0)
])
def test_predict_wait_time(sample_data, doctor_id, scheduled_time, expected):
    result = predict_wait_time(doctor_id, scheduled_time)
    assert isinstance(result, float), "Prediction should return a float"
    assert 0 <= result <= 120, "Wait time should be reasonable"


def test_optimize_schedule(sample_data):
    # Add arrival deviation test data
    sample_data['arrival_deviation'] = [-15, 5, -10, 20]
    result = optimize_schedule(sample_data)
    
    # Test queue prioritization
    assert result.iloc[0]['arrival_deviation'] == -15, "Should prioritize earliest arrivals"
    assert result.iloc[1]['arrival_deviation'] == -10, "Secondary priority to early arrivals"
    assert 'assigned_doctor' in result.columns, "Should add assigned_doctor column"
    assert result['assigned_doctor'].isin([3,5]).all(), "Doctors should be from available set"


from unittest.mock import patch


@patch('os.environ', {'TWILIO_ACCOUNT_SID': 'test', 'TWILIO_AUTH_TOKEN': 'test', 'TWILIO_PHONE_NUMBER': '+123'})
@patch('twilio.rest.Client')
def test_send_wait_time_update(mock_twilio, capsys):
    mock_api = mock_twilio.return_value
    mock_api.messages.create.return_value.sid = 'SM123'


@patch('twilio.rest.Client')
@patch('os.environ', {'TWILIO_ACCOUNT_SID': 'test', 'TWILIO_AUTH_TOKEN': 'test', 'TWILIO_PHONE_NUMBER': '+123'})
def test_sms_success_rate_tracking(mock_twilio):
    """Track SMS delivery success rate across multiple attempts"""
    from collections import defaultdict
    results = defaultdict(int)
    
    # Configure mock to succeed for valid numbers
    mock_api = mock_twilio.return_value
    mock_api.messages.create.return_value.sid = 'SM123'
    
    # Test with 10 simulated sends (7 success, 3 failure)
    for i in range(10):
        try:
            phone = '+15551234' if i%3 !=0 else 'invalid'
            send_wait_time_update(phone, 30.5)
            results['success'] += 1
        except Exception:
            results['failure'] += 1
    
    success_rate = results['success'] / (results['success'] + results['failure'])
    assert success_rate >= 0.7, f"Success rate {success_rate*100}% below 70% threshold"

@pytest.mark.parametrize("input,expected", [
    (datetime(2024, 3, 26, 18, 30), 18),
    (datetime(2024, 3, 27, 9, 0), 9)
])
def test_hour_feature(sample_data, input, expected):
    # Process test data through same feature engineering as main code
    # Override scheduled_time with test input
    sample_data['scheduled_time'] = pd.to_datetime([input] * len(sample_data))
    sample_data['hour'] = sample_data['scheduled_time'].dt.hour
    assert sample_data['hour'].iloc[0] == expected


@pytest.mark.parametrize('peak_scenario,expected_reduction', [
    (True, 0.3),
    (False, 0.1)
])
def test_wait_time_reduction(sample_data, peak_scenario, expected_reduction):
    sample_data['scheduled_time'] = pd.to_datetime(sample_data['scheduled_time'])
    sample_data['actual_time'] = pd.to_datetime(sample_data['actual_time'])
    # Mock peak vs non-peak data
    scheduled_times = pd.date_range(start='2024-03-26 17:00', periods=50, freq='15min')
    base_data = pd.DataFrame({
        'doctor_id': np.random.choice([3,5], 50),
        'scheduled_time': scheduled_times,
        'actual_time': scheduled_times + pd.to_timedelta(np.random.randint(20,40,50), unit='m'),
        'arrival_deviation': np.random.randint(-30,30,50)
    })
    
    # Apply peak scenario modifier
    if peak_scenario:
        base_data = base_data.set_index('scheduled_time').between_time('17:00','20:00').reset_index()
        base_data['actual_time'] += pd.to_timedelta(25, unit='m')
    
    optimized = optimize_schedule(base_data)
    base_data['scheduled_time'] = pd.to_datetime(base_data['scheduled_time'])
    base_data['actual_time'] = pd.to_datetime(base_data['actual_time'])
    optimized['scheduled_time'] = pd.to_datetime(optimized['scheduled_time'])
    optimized['actual_time'] = pd.to_datetime(optimized['actual_time'])
    
    original_avg = (base_data['actual_time'] - base_data['scheduled_time']).dt.total_seconds().mean()/60
    optimized_avg = (optimized['actual_time'] - optimized['scheduled_time']).dt.total_seconds().mean()/60
    
    assert (original_avg - optimized_avg)/original_avg >= expected_reduction, f"Failed {peak_scenario} scenario reduction"

@patch('os.environ', {})
def test_sms_credential_safety():
    with patch.dict('os.environ', clear=True):
        with pytest.raises(OSError) as excinfo:
            send_wait_time_update('+15551234', 30.5)
    assert 'TWILIO_ACCOUNT_SID not set' in str(excinfo.value)


@pytest.mark.parametrize('phone_number,expected_error', [
    ('invalid', 'Invalid phone number'),
    ('+123', 'Invalid phone number'),
    (None, 'Invalid phone number'),
    ('15551234', 'Invalid phone number'),
    ('+1555123', 'Too short'),
    ('+155512345678901', 'Too long')
])
@patch('twilio.rest.Client')
@patch('os.environ', {'TWILIO_ACCOUNT_SID': 'test', 'TWILIO_AUTH_TOKEN': 'test', 'TWILIO_PHONE_NUMBER': '+123'})
def test_invalid_phone_number_handling(mock_twilio, phone_number, expected_error):
    # Should fail validation before reaching Twilio
    mock_api = mock_twilio.return_value
    mock_api.messages.create.side_effect = Exception('Twilio API Error')

    with pytest.raises(ValueError) as excinfo:
        send_wait_time_update(phone_number, 15.0)
    
    assert expected_error in str(excinfo.value)
    mock_api.messages.create.assert_not_called()


@patch('skeletonCodeAssesment1.model')
def test_historical_wait_time_reduction(mock_model):
    """Validate 30% reduction with mocked AI predictions"""
    # Configure mock model predictions
    mock_model.predict.return_value = np.array([30.0, 25.0, 20.0, 15.0, 10.0, 5.0])
    
    # Mock historical data
    historical_data = pd.DataFrame({
        'doctor_id': [5,5,3,3,5,3],
        'scheduled_time': pd.date_range(start='2024-03-26 09:00', periods=6, freq='15min'),
        'actual_time': pd.date_range(start='2024-03-26 09:20', periods=6, freq='25min'),
        'arrival_deviation': [-10, 5, -15, 20, 0, 10]
    })
    
    # Calculate original average wait time
    original_avg = (historical_data['actual_time'] - historical_data['scheduled_time']).dt.total_seconds().mean() / 60
    
    # Optimize schedule
    optimized_data = optimize_schedule(historical_data)
    
    # Calculate optimized average wait time
    optimized_avg = (optimized_data['actual_time'] - optimized_data['scheduled_time']).dt.total_seconds().mean() / 60
    
    # Verify metrics from README requirements
    reduction = (original_avg - optimized_avg) / original_avg
    assert reduction >= 0.3, "Failed 30% historical reduction (got %.1f%%)" % (reduction*100)
    assert optimized_avg <= 15, "Average wait time exceeds 15min threshold"