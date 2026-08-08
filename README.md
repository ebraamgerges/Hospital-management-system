# Hospital Booking System

A simple hospital booking/management system built with Python (OOP), with a small Flask API layer.

## Team

5-person team project:
- **Member 1 — Core Models**: Patient, Doctor, Department
- **Member 2 — Scheduling Engine (Ebraam Gerges)**: Appointment, Schedule
- **Member 3 — Admin & Access**: Auth, Admin
- **Member 4 — JSON Persistence**: Notification, FileStorage
- **Member 5 — UI & Integration**: main.py, MenuUI

## Project Structure

```
.
├── main1.py               # Core classes: patient, doctor, department, appointment,
│                           # regular_appointment, emergency_appointment, Schedule,
│                           # Auth, FileStorage, MedicalReport, main() CLI flow
├── api.py                 # Flask API exposing patients, patient history, and doctors
├── doctors_data.csv        # Seed data for doctors
├── patients_data.json      # Persisted patient records
├── appointments_data.json  # Persisted appointments
├── reports_data.json       # Persisted medical visit reports
└── package-lock.json       # Frontend dependency lock file (lucide-react/react)
```

## Requirements

```bash
pip install flask flask-cors
```

## Running the CLI app

```bash
python main1.py
```

Walks through: patient registration → doctor selection → diagnosis →
available appointment times → booking (regular/emergency) → saving a
medical report (JSON + text file).

## Running the API

```bash
python api.py
```

Endpoints:
- `GET /api/patients/<patient_id>` — fetch a patient by ID
- `GET /api/patients/<patient_id>/history` — fetch a patient's visit history
- `GET /api/doctors` — list all doctors

## Notes

- Data is persisted to local JSON files (`patients_data.json`,
  `appointments_data.json`, `reports_data.json`) via the `FileStorage` class.
- Doctors are seeded from `doctors_data.csv`.
