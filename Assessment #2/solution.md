# 🏥 Intelligent Queue Management System (Schedula)

This project is an intelligent queue management system built for a medical practice using Python. It simulates real-time queue handling for 50+ doctors with unpredictable patient arrivals, multiple booking channels, and varying priorities. Designed to optimize wait times and improve patient experience, the system dynamically updates queues based on urgency, arrival delays, and appointment source.

---

## 📦 Problem Breakdown

### 1. Doctor Schedules & Availability

- Each doctor has defined **availability blocks** (e.g., `(9, 12)`, `(15, 18)`).
- Real-time availability is tracked to avoid overlapping assignments and manage capacity.
- The system can be extended to include exceptions like leaves, emergencies, etc.

### 2. Patient Arrival & Appointment Handling

- The system captures both **scheduled** and **actual arrival times** for every patient.
- It calculates **arrival delays**, which impact queue priority.
- **Walk-in patients** are supported and can be integrated without prior bookings.
- **Missed appointments** (no-shows) can be flagged and rescheduled if required.

### 3. Multi-Channel Appointment Sources

- Appointments come from various sources: **App**, **IVR**, **WhatsApp**, and **Walk-ins**.
- Each patient has a `source` field which is factored into priority calculation.
- All channels feed into a **centralized queuing system**, allowing unified queue management.

### 4. Queue Optimization & Prioritization

- Patients are dynamically assigned to queues based on:
  - **Urgency score**
  - **Arrival delay**
  - **Source of appointment**
- Priority is calculated using:
  ```python
  priority = -(urgency * 10 - delay + source_bonus)
  ```
  - The **negative** value allows use of Python’s `heapq` as a **min-heap**.
  - **Tie-breaking** is handled using the patient ID to ensure stable heap behavior.

### 5. Patient Status Tracking

- Every patient in the system is tracked with a status: `"waiting"` or `"consulted"`.
- Patient status is updated automatically when they are seen by the doctor.
- A centralized `patient_log` tracks:
  - Assigned doctor
  - Arrival time
  - Booking source
  - Real-time status

---

## 📊 Required Information for Intelligent Queuing

To make smart queue decisions, the system uses:

- **Doctor’s live availability**
- **Expected consultation time** (default or estimated)
- **Patient arrival patterns**
- **Historical delay data** (optional future extension)
- **Channel-wise trends** (used in priority calculation)
- **Doctor-specific preferences** (can be plugged in)

---

## 📈 Measuring System Effectiveness

Metrics to evaluate the system include:

- ⏱️ **Average Wait Time Reduction**  
  Compare before vs. after implementation.

- 📊 **Queue Efficiency Score**  
  Track patients served per doctor per shift.

- 😊 **Patient Satisfaction**  
  Collect feedback via SMS/App post-consultation.

- 🔄 **No-show & Walk-in Handling**  
  Monitor how well the system adapts to unexpected behavior.

---

## 📱 Patient Communication Strategy

- **Real-time ETA Notifications**  
  Patients are notified of their estimated wait time.

- **Check-in Confirmations**  
  Automatic confirmation when the patient is seen.

- **Reschedule Options**  
  If delay exceeds X minutes, a message with alternatives can be sent.

---

## 🧪 Test Scenarios Covered

- On-time, early, and late arrivals
- Walk-in vs. scheduled patient comparison
- Multiple doctors with isolated queues
- Edge case: querying non-existent patient
- Doctor consulting next patient and status transition
- Real-time wait-time updates

---

## 🚀 Getting Started

1. Install Python 3.8+
2. Clone this repo and run:

```bash
python skeletonCodeAssessment2.py
```

You’ll see printed results for all tested queue scenarios.

---

## 📁 Project Structure

```
📦 Schedula Queue System
├── skeletonCodeAssessment2.py   # Main intelligent queue system logic
├── README.md                    # This file
```

---

## 🙌 Authors

Developed by VIJAY GANESH - https://www.linkedin.com/in/vijay-ganesh-071756249/ engineer as part of a real-world simulation assignment for **PearlThoughts AI Internship**.