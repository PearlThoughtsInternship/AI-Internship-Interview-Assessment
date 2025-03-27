# Assessment 1 

**Managing Peak Hour Patient Flow at Urban Multi-Specialty Clinic**

Context: Jayanagar Specialty Clinic in Bangalore sees 300+ patients daily with peak congestion between 5-8pm when working professionals arrive. The 15 specialists have varying consultation patterns.

# Problem Outline:

* Situation: The clinic reports 40-minute average wait times during evening hours, with some patients waiting up to 90 minutes
* Data Available:
  * 3 months of appointment records showing scheduled vs. actual times
  * Doctor-wise average consultation durations (ranging from 8-22 minutes)
  * Peak vs. non-peak hour patient distribution (75% of patients prefer evening slots)

# Evaluation Task:

* Design an AI approach that could reduce evening wait times by at least 30%
* Suggest 3 specific prediction features that would be most valuable
* Explain how the system should handle the common scenario of patients arriving 20-30 minutes before their appointment expecting to be seen earlier

# Expected Solution Elements:

* Predictive load balancing across available doctors
* Time-slot optimization based on consultation patterns
* Patient communication strategy for realistic wait time

**Twilio SMS Integration Setup:**
1. Obtain TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN from Twilio console
2. Set environment variables:
```bash
export TWILIO_ACCOUNT_SID='your_account_sid'
export TWILIO_AUTH_TOKEN='your_auth_token'
export TWILIO_PHONE_NUMBER='+1234567890'
```
3. System will automatically use these credentials for SMS notifications

# Expected Solution Format :

1. Proposed AI Solution Overview
   Briefly explain how AI will optimize peak-hour patient flow.

   Mention key techniques such as predictive load balancing, time-slot optimization, and patient communication strategies.

2. Key AI Features & Predictive Model Inputs
   Appointment delay prediction → Train a model using past data to predict delays based on doctor schedules.

   Dynamic slot allocation → Adjust booking times based on real-time doctor availability.

   Patient Arrival Forecasting → Predict early arrivals and optimize queues.

3. AI Model & Data Processing Pipeline
    Data Collection: Structure of input data (past appointments, doctor schedules, patient arrival patterns).

    Feature Engineering: What data points are used for training?

    Model Selection: Suggested algorithms (e.g., Decision Trees, LSTM, or Reinforcement Learning).

    Real-time Predictions: How the system will continuously update slot allocations.

4. Handling Early Arrivals
    Queue Prioritization: Dynamically adjust the queue for patients who arrive early without disrupting other appointments.

    SMS Notifications: Notify patients of real-time estimated wait times.

5. Expected Outcome
    Predictive scheduling reduces wait time by at least 30%.

    Even distribution of workload across doctors.

    Improved patient experience through transparency in wait times.



## Instructions:
1. Clone this repository.
3. Raise a Pull Request (PR) with your solution.
4. Record a video explaining your solution.
5. Attach the video link in the submission form.
6. Submit the PR link in the submission form.