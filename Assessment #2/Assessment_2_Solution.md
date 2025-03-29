# Assessment 2: Scenario-Based Assessment

## Problem Statement
Schedula needs to implement an Intelligent Queue Management system for a medical practice with the following characteristics:
- 50 doctors with varied scheduling patterns
- Each doctor sees 30-50 patients daily in 3-hour blocks
- Patients arrive unpredictably, often not at their scheduled times
- Appointments come from multiple channels (IVR, app, WhatsApp)
- Walk-in patients need to be accommodated
- Some doctors track patient status (arrived, waiting, consulted), but not all

## 1. Problem Breakdown

### Logical Components & Steps

#### **Doctor Schedules & Availability**
- **Track Individual Doctor Schedules**: Develop a database to hold each doctor's schedule, taking into account their unique availability.
- **Real-Time Updates**: Ensure that the system reflects real-time availability and dynamically updates as patients check-in or appointments change.

#### **Patient Arrival & Appointment Handling**
- **Scheduled vs. Actual Arrival Times**: Implement a system to log scheduled appointment times alongside actual patient arrivals.
- **Walking Patients**: Create a method for handling walk-in patients, integrating them into the queue while minimizing disruption to the schedule.
- **Missed Appointments**: Establish a protocol for rescheduling patients who miss their appointments.

#### **Multi-Channel Appointment Sources**
- **Appointment Integration**: Create a central system that integrates appointments from IVR, app, WhatsApp, and walk-in bookings for unified management.

#### **Queue Optimization & Prioritization**
- **Dynamic Queue Assignment**: Assign patients to doctors based on real-time queue lengths, urgency of visit (e.g., emergent cases), and doctor availability.
- **Utilize Historical Data**: Analyze past patient flow data to make informed adjustments during peak hours.

#### **Patient Status Tracking**
- **Real-Time Updates**: Implement a status tracking feature to provide updates for patients marked as "arrived," "waiting," or "consulted."

## 2. Required Information for Intelligent Queuing
- **Doctor's Live Schedule & Consultation Durations**: Data on how long each doctor spends with patients per appointment type.
- **Real-Time Patient Check-In & Arrival Patterns**: Logging mechanism for tracking check-ins and arrival times.
- **Historical Appointment Data**: Access to past records to identify peak times and assist in forecasting.
- **Channel-Wise Booking Trends**: Insight into which channels are most popular for appointments.
- **Doctor-Specific Queue Preferences**: Collecting data on each doctor's preference regarding how many walk-ins they can handle.

## 3. Measuring System Effectiveness
- **Average Wait Time Reduction**: Measure wait times before and after implementing the new system to assess improvement.
- **Queue Efficiency Score**: Validate efficiency through metrics such as patients served per doctor per time block.
- **Patient Satisfaction Metrics**: Use surveys or feedback forms sent via the app or SMS to gather insights from patients about their experience.
- **No-Show & Walk-In Handling**: Track the system's success in managing unexpected patient arrivals and missed appointments.

## 4. Patient Communication Strategy
- **Real-Time ETA Updates**: Provide patients with estimated wait times through SMS or app notifications.
- **Rescheduling Option**: If a patient's wait time exceeds a certain threshold (e.g., 20 minutes), provide options to reschedule their visit.
- **Check-in Confirmation**: Implement an automated message that notifies patients when the doctor is ready for them.

## Loom Video Demonstration
You can view the video demonstration of my assessment [here](https://www.loom.com/share/d48e8cde826a4d3c871a5f8c7d9d1c54?sid=841ffe67-3d5f-45f9-b4a7-bffae656184c).